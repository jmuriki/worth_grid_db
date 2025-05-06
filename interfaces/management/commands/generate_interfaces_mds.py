import os

from django.core.management.base import BaseCommand
from content.models import Interface

class Command(BaseCommand):
    help = 'Экспорт данных каждого Интерфейса в отдельный Markdown-файл'

    def handle(self, *args, **options):
        interfaces = Interface.objects.prefetch_related(
            'subcatalogs',
            'roles',
            'roles__functions',
            'roles__functions__stories',
            'roles__functions__stories__context_points',
            'roles__functions__stories__start_point',
            'roles__functions__stories__acceptors',
        )
        
        for interface in interfaces:
            interfaces_dir_name = 'ИНТЕРФЕЙСЫ'
            interfaces_subcatalogs_paths = []
            interfaces_subcatalogs = interface.subcatalogs.all()
            if interfaces_subcatalogs:
                for subcatalog in interfaces_subcatalogs:
                    interfaces_subcatalogs_paths.append(os.path.join(interfaces_dir_name, subcatalog.title))
            else:
                interfaces_subcatalogs_paths.append(interfaces_dir_name)

            for subcatalog_path in interfaces_subcatalogs_paths:
                os.makedirs(subcatalog_path, exist_ok=True)

                interface_md_filename = os.path.join(subcatalog_path, f'{interface.title}.md')
                with open(interface_md_filename, 'w', encoding='utf-8') as md_file:

                    md_file.write(f'# 🖥️ Интерфейс "{interface.title}"\n***\n\n')
                    if interface.description:
                        md_file.write('###### Описание\n\n')
                        md_file.write(f'{interface.description}\n\n')
                    md_file.write('\n')

                    roles = interface.roles.all().order_by('order_position')
                    for role in roles:
                        md_file.write(f'## 👤 {role.title}\n***\n\n')
                        if role.description:
                            md_file.write('###### Описание\n\n')
                            md_file.write(f'{role.description}\n\n')
                        md_file.write('\n')

                        functions = role.functions.all().order_by('order_position')
                        for function in functions:
                            md_file.write(f'### 𝑓 {function.job}\n***\n\n')
                            if role.description:
                                md_file.write('###### Описание\n\n')
                                md_file.write(f'{function.description}\n\n')
                            md_file.write('\n')

                            stories = function.stories.all().order_by('order_position')
                            for story in stories:
                                md_file.write(f'##### ✔ {story.title}\n\n')
                                if story.description:
                                    md_file.write('###### Описание\n\n')
                                    md_file.write(f'{story.description}\n\n')

                                if story.context_points.exists():
                                    md_file.write('**Когда:**\n\n')
                                    context_points = story.context_points.all().order_by('order_position')
                                    for context_point in context_points:
                                        md_file.write(f'- {context_point.text}\n\n')
                                    md_file.write('\n')

                                if story.start_point:
                                    md_file.write('**Старт:**\n\n')
                                    md_file.write(f'- {story.start_point.text}\n\n')
                                    md_file.write('\n')
                                    
                                if story.acceptors.exists():
                                    got_wanted = 'Успех' if story.got_wanted else 'Отказ'
                                    md_file.write(f'**{got_wanted}:**\n\n')
                                    acceptors = story.acceptors.all().order_by('order_position')
                                    for acceptor in acceptors:
                                        md_file.write(f'- {acceptor.text}\n\n')
                                    md_file.write('\n')

                                md_file.write('***\n')

                        self.stdout.write(self.style.SUCCESS(
                            f'Интерфейс {interface.title} → {interface_md_filename}'
                        ))
