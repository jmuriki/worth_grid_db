import re

from pathlib import Path

from django.core.management.base import BaseCommand

from interfaces.models import (
    InterfaceSubCatalog,
    Interface,
    Role,
    Function,
    Story,
    StoryContext,
    StartPoint,
    StoryAcceptor,
)


RE_INTERFACE = re.compile(r'^##.*?Интерфейс\s*"(?P<title>[^"]+)"', re.MULTILINE)
RE_USER_TYPE = re.compile(r'^##\s+👤\s+(?P<role>.+)$', re.MULTILINE)
RE_FUNCTION = re.compile(r'^###\s+𝑓\s+(?P<job>.+)$', re.MULTILINE)
RE_STORY = re.compile(r'^####\s+✔\s+(?P<title>.+)$', re.MULTILINE)


class Command(BaseCommand):
    help = 'Импортирует все .md файлы интерфейсов в БД'

    def add_arguments(self, parser):
        parser.add_argument(
            'root_path',
            type=str,
            nargs='?',
            default="/Users/admin108/Library/Mobile Documents/com~apple~CloudDocs/Documents/PROGRAMMING/DEVMAN/ReviewGym/WorthGrid/ЦЕННОСТНАЯ СЕТКА/2. ИНТЕРФЕЙСЫ",
            help='Абсолютный путь к корневой папке ИНТЕРФЕЙСЫ',
        )

    def handle(self, *args, **options):
        root = Path(options['root_path'])
        md_files = list(root.rglob('*.md'))
        self.stdout.write(f'Найдено файлов: {len(md_files)}')

        for md_path in md_files:

            with open(md_path, 'r', encoding='utf-8') as file:
                text = file.read().splitlines()

            interface_subcatalog_name = md_path.parent.name
            subcatalog, _ = InterfaceSubCatalog.objects.get_or_create(title=interface_subcatalog_name)
            
            interface = None
            role = None
            function = None
            story = None
            is_context = None
            is_start = None
            is_success = None
            is_refusal = None

            for line in text:
                if not interface:
                    interface_md_title = RE_INTERFACE.search(line)
                    if not interface_md_title:
                        continue
                    interface_subtitle = interface_md_title.group('title')
                    interface_title = md_path.stem
                    interface, _ = Interface.objects.get_or_create(title=interface_title, subtitle=interface_subtitle)
                    interface.subcatalogs.add(subcatalog)

                md_role = RE_USER_TYPE.search(line)
                if md_role:
                    role, _ = Role.objects.get_or_create(interface=interface, title=md_role.group('role'))

                md_function = RE_FUNCTION.search(line)
                if md_function:
                    function_job = md_function.group('job').strip()
                    function, _ = Function.objects.get_or_create(role=role, job=function_job)

                md_story = RE_STORY.search(line)
                if md_story:
                    story_title = md_story.group('title').strip()
                    story, _ = Story.objects.get_or_create(
                        title=story_title,
                        function=function,
                        got_wanted=True,
                    )

                if 'Ситуация' in line:
                    is_context = True
                    continue
                if is_context and len(line) > 3:
                    StoryContext.objects.get_or_create(story=story, text=line.lstrip('>- [ ] '))
                elif is_context and len(line) < 3:
                    is_context = None

                if 'Старт' in line:
                    is_start = True
                    continue
                if is_start and len(line) > 3:
                    StartPoint.objects.get_or_create(story=story, text=line.lstrip('>- [ ] '))
                elif is_start and len(line) < 3:
                    is_start = None

                if 'Успех' in line:
                    is_success = True
                    story.got_wanted = True
                    story.save()
                    continue
                if is_success and len(line) > 3:
                    StoryAcceptor.objects.get_or_create(story=story, text=line.lstrip('>- [ ] '))
                elif is_success and len(line) < 3:
                    is_success = None

                if 'Отказ' in line:
                    is_refusal = True
                    story.got_wanted = False
                    story.save()
                    continue
                if is_refusal and len(line) > 3:
                    StoryAcceptor.objects.get_or_create(story=story, text=line.lstrip('>- [ ] '))
                elif is_refusal and len(line) < 3:
                    is_refusal = None

        self.stdout.write(self.style.SUCCESS('Импорт завершён'))
