import re
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from content.models import (
    InterfaceGroup,
    Interface,
    UserType,
    Function,
    Story,
    ContextPoint,
    StartPoint,
    SuccessPoint,
    RefusalPoint,
)


RE_INTERFACE = re.compile(r'^##.*?Интерфейс\s*"(?P<title>[^"]+)"', re.MULTILINE)
RE_USER_TYPE = re.compile(r'^##\s+👤\s+(?P<role>.+)$', re.MULTILINE)
RE_FUNCTION = re.compile(r'^###\s+𝑓\s+(?P<title>.+)$', re.MULTILINE)
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

            interface_group_name = md_path.parent.name
            group, _ = InterfaceGroup.objects.get_or_create(short_name=interface_group_name, title=interface_group_name)
            
            interface = None
            user_type = None
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
                    interface_title = interface_md_title.group('title')
                    interface_name = md_path.stem
                    interface, _ = Interface.objects.get_or_create(short_name=interface_name, title=interface_title)
                    interface.groups.add(group)

                md_user_type = RE_USER_TYPE.search(line)
                if md_user_type:
                    user_type, _ = UserType.objects.get_or_create(role=md_user_type.group('role'))

                md_function = RE_FUNCTION.search(line)
                if md_function:
                    func_title = md_function.group('title').strip()
                    function, _ = Function.objects.get_or_create(title=func_title)

                md_story = RE_STORY.search(line)
                if md_story:
                    story_title = md_story.group('title').strip()
                    story, _ = Story.objects.get_or_create(
                        title=story_title,
                        function=function,
                        user_type=user_type,
                        interface=interface,
                    )

                if 'Ситуация' in line:
                    is_context = True
                    continue
                if is_context and len(line) > 3:
                    ContextPoint.objects.get_or_create(story=story, text=line.lstrip('>- [ ] '))
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
                    continue
                if is_success and len(line) > 3:
                    SuccessPoint.objects.get_or_create(story=story, text=line.lstrip('>- [ ] '))
                elif is_success and len(line) < 3:
                    is_success = None

                if 'Отказ' in line:
                    is_refusal = True
                    continue
                if is_refusal and len(line) > 3:
                    RefusalPoint.objects.get_or_create(story=story, text=line.lstrip('>- [ ] '))
                elif is_refusal and len(line) < 3:
                    is_refusal = None

        self.stdout.write(self.style.SUCCESS('Импорт завершён'))
