import os

from django.core.management.base import BaseCommand
from content.models import Interface, Story

class Command(BaseCommand):
    help = 'Экспорт данных каждого Интерфейса в отдельный Markdown-файл'

    def handle(self, *args, **options):
        interfaces = Interface.objects.prefetch_related('groups', 'stories__user_type')
        for interface in interfaces:
            interfaces_dir_name = 'ИНТЕРФЕЙСЫ'
            interfaces_groups_paths = []
            interfaces_groups = interface.groups.all()
            if interfaces_groups:
                for group in interfaces_groups:
                    interfaces_groups_paths.append(os.path.join(interfaces_dir_name, group.short_name))
            else:
                interfaces_groups_paths.append(interfaces_dir_name)

            for interfaces_group_path in interfaces_groups_paths:
                os.makedirs(interfaces_group_path, exist_ok=True)

                interface_md_filename = os.path.join(interfaces_group_path, f'{interface.short_name}.md')
                with open(interface_md_filename, 'w', encoding='utf-8') as md_file:

                    md_file.write(f'# 🖥️ Интерфейс "{interface.title}"\n***\n\n')
                    if interface.description:
                        md_file.write('###### Описание\n\n')
                        md_file.write(f'{interface.description}\n\n')
                    md_file.write('\n')

                    user_types = {
                        story.user_type for story in interface.stories.all() if story.user_type
                    }
                    for user_type in user_types:
                        md_file.write(f'## 👤 {user_type.role}\n***\n\n')
                        if user_type.description:
                            md_file.write('###### Описание\n\n')
                            md_file.write(f'{user_type.description}\n\n')
                        md_file.write('\n')

                        user_type_stories = Story.objects.filter(
                            interface=interface, user_type=user_type).prefetch_related('function')
                        user_type_functions = {story.function for story in user_type_stories}
                        for function in user_type_functions:
                            md_file.write(f'### 𝑓 {function.title}\n***\n\n')
                            if user_type.description:
                                md_file.write('###### Описание\n\n')
                                md_file.write(f'{function.description}\n\n')
                            md_file.write('\n')

                            function_stories = Story.objects.filter(
                                interface=interface, user_type=user_type, function=function).prefetch_related(
                                'context_points',
                                'start_points',
                            )
                            for story in function_stories:
                                md_file.write(f'##### ✔ {story.title}\n\n')
                                if story.description:
                                    md_file.write('###### Описание\n\n')
                                    md_file.write(f'{story.description}\n\n')

                                # Предыстория
                                if story.context_points.exists():
                                    md_file.write('**Когда:**\n\n')
                                    for context_point in story.context_points.all():
                                        md_file.write(f'- [ ] {context_point.text}\n\n')
                                    md_file.write('\n')

                                # Старт
                                if story.start_points.exists():
                                    md_file.write('**Старт:**\n\n')
                                    for start_point in story.start_points.all():
                                        md_file.write(f'- [ ] {start_point.text}\n\n')
                                    md_file.write('\n')

                                # Успех
                                if story.success_points.exists():
                                    md_file.write('**Успех:**\n\n')
                                    for success_point in story.success_points.all():
                                        # [Перейти к следующей странице](путь/к/файлу/)
                                        md_file.write(f'- [ ] {success_point.text}\n\n')
                                        # for example in success_point.example.all():
                                        #     md_file.write(f'  - Пример **{example.name or "—"}**: {example.description or "—"}\n')
                                        #     for sn in example.snippets.all():
                                        #         md_file.write('```python\n')
                                        #         md_file.write(sn.code.strip() + '\n')
                                        #         md_file.write('```\n')
                                    md_file.write('\n')

                                # Отказ
                                if story.refusal_points.exists():
                                    md_file.write('**Отказ:**\n\n')
                                    for refusal_point in story.refusal_points.all():
                                        md_file.write(f'- [ ] {refusal_point.text}\n\n')
                                        # for example in refusal_point.example.all():
                                        #     md_file.write(f'  - Пример **{example.name or "—"}**: {example.description or "—"}\n')
                                        #     for sn in example.snippets.all():
                                        #         md_file.write('```python\n')
                                        #         md_file.write(sn.code.strip() + '\n')
                                        #         md_file.write('```\n')
                                    md_file.write('\n')

                                md_file.write('***\n')

                        self.stdout.write(self.style.SUCCESS(
                            f'Интерфейс {interface.short_name} → {interface_md_filename}'
                        ))
