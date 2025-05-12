import os

from pathlib import Path
from textwrap import dedent

from django.core.management.base import BaseCommand
from interfaces.models import Interface

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

        base_dir = 'docs'
        os.makedirs(base_dir, exist_ok=True)

        interfaces_dir_path = Path(base_dir, 'ЦС', 'ИНТЕРФЕЙСЫ')
        os.makedirs(interfaces_dir_path, exist_ok=True)

        catalog_file_path = Path(base_dir, 'Интерфейсы.md')
        with open(catalog_file_path, 'w', encoding='utf-8') as catalog_file:
            catalog_file.write('# Интерфейсы\n\n')
        
            for interface in interfaces:
                interface_name = interface.subtitle
                interface_rel_link = os.path.join(f'../ЦС/ИНТЕРФЕЙСЫ', interface_name)
                encoded_interface_rel_link = interface_rel_link.replace(' ', '%20')

                catalog_file.write(dedent(f'''
                    <ul>
                    \t<li>
                    \t\t<img src="../img/{os.path.basename(interface.logo.name)}" alt="logo" style="width: 2em; vertical-align: middle;" />
                    \t\t<a href="{encoded_interface_rel_link}" style="margin-left: 5px;">{interface_name}</a>
                    \t</li>
                    </ul>
                '''))

                interface_md_filename = f'{interface_name}.md'
                interface_md_file_path = Path(interfaces_dir_path, interface_md_filename)
                with open(interface_md_file_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(dedent(f'''
                        <div style="display: flex; align-items: flex-start; align-items: center;">
                        \t<div style="margin-right: 5px;">
                        \t\t<img src="../../../img/{os.path.basename(interface.logo.name)}" alt="logo" style="display: block; width: 4em; height: auto; margin-right: 1rem;" />
                        \t</div>
                        \t<div>
                        \t\t<h1 style="margin: 0;">{interface_name}</h1>
                        \t\t<p style="margin: 0;">Интерфейс</p>
                        \t</div>
                        </div>\n
                    '''))

                    if interface.description:
                        md_file.write(dedent(f'''
                            **Описание:**\n
                            {interface.description}\n
                        '''))

                    roles = interface.roles.all().order_by('order_position')
                    for role in roles:
                        role_title = role.title
                        md_file.write(dedent(f'''
                            ***\n
                            <div style="display: flex; align-items: flex-start; align-items: center;">
                            \t<div style="margin-right: 5px;">
                            \t\t<img src="../../../img/{os.path.basename(role.logo.name)}" alt="logo" style="display: block; width: 3.3em; height: auto; margin-right: 1rem;" />
                            \t</div>
                            \t<div>
                            \t\t<h2 style="margin: 0; font-size: 22px;">{role_title}</h2>
                            \t\t<p style="margin: 0;">Роль</p>
                            \t</div>
                            </div>\n
                        '''))

                        if role.description:
                            md_file.write(dedent(f'''
                                **Описание:**\n
                                {role.description}\n
                            '''))

                        functions = role.functions.all().order_by('order_position')
                        for function in functions:
                            job = function.job
                            md_file.write(dedent(f'''
                                ***\n
                                ### 𝑓 {job}\n
                            '''))

                            if function.description:
                                md_file.write(dedent(f'''
                                    **Описание:**\n
                                    {function.description}\n
                                '''))

                            stories = function.stories.all().order_by('order_position')

                            for story in stories:
                                story_title = story.title
                                story_logo = '✅' if story.got_wanted else '⚠️'
                                md_file.write(dedent(f'''
                                    ***\n
                                    ##### {story_logo} {story_title}\n
                                '''))

                                # 1
                                if story.description:
                                    md_file.write(dedent(f'''
                                        **Описание:**\n
                                        {story.description}\n
                                    '''))
                                else:
                                    md_file.write(
                                        f'**Типичная История:** {role_title} хочет {job} {story_title}.\n\n'
                                    )

                                # 2
                                md_file.write(dedent(f'''
                                    **Кто я:**  {role_title}\n
                                    **Чего хочу:** {job}\n
                                '''))

                                # 3
                                md_file.write(dedent(f'''
                                    **Кто я:**\n
                                    - {role_title}\n
                                    **Чего хочу:**\n
                                    - {job}\n
                                '''))

                                if story.context_points.exists():
                                    context_points = story.context_points.all().order_by('order_position')
                                    md_file.write('**Когда:**\n\n')
                                    for context_point in context_points:
                                        md_file.write(f'- {context_point.text}\n\n')
                                    md_file.write('\n')

                                if story.start_point:
                                    md_file.write(dedent(f'''
                                        **Старт:**\n
                                        - {story.start_point.text}\n
                                    '''))

                                if story.acceptors.exists():
                                    got_wanted = 'Успех' if story.got_wanted else 'Отказ'
                                    md_file.write(f'**{got_wanted}:**\n\n')

                                    acceptors = story.acceptors.all().order_by('order_position')
                                    for acceptor in acceptors:

                                        example_links = acceptor.example_links.all()
                                        if example_links.exists():
                                            relations_dir_rel_path = os.path.join('ЦС', 'СВЯЗИ АКЦЕПТОРОВ')
                                            relations_dir_path = os.path.join(base_dir, relations_dir_rel_path)
                                            os.makedirs(relations_dir_path, exist_ok=True)

                                            relations_filename = f'Связи_Акцептора_{acceptor.id}.md'
                                            relations_file_path = os.path.join(relations_dir_path, relations_filename)
                                            with open(relations_file_path, 'w', encoding='utf-8') as file:
                                                file.write(dedent(f'''
                                                    # Анти-паттерны, повреждающие Акцептор\n
                                                    **Интерфейс:** {interface_name}\n
                                                    **Роль:** {role_title}\n
                                                    **Функция:** {job}\n
                                                    **История:** {story_title}\n
                                                    **Акцептор:** {acceptor.text}\n
                                                    ***\n
                                                '''))
                                                for example_link in example_links:
                                                    position = example_link.anti_pattern_example.order_position
                                                    number = position if position else ''
                                                    anti_pattern_name = example_link.anti_pattern_example.anti_pattern.title
                                                    comment_line = f'**Как обнаружить:** {example_link.comment}\n' if example_link.comment else ''
                                                    file.write(dedent(f'''
                                                        **Пример {number} к Анти-паттерну:** [{anti_pattern_name}](../../../ЦС/АНТИ-ПАТТЕРНЫ/{anti_pattern_name})\n
                                                        {comment_line}
                                                        ***\n
                                                    '''))
                                            relations_file_link = f'../../../{relations_dir_rel_path}/{relations_filename.replace(".md", "")}'
                                            md_file.write(f'- {acceptor.text} [☰]({relations_file_link})\n\n')
                                        else:
                                            md_file.write(f'- {acceptor.text}\n\n')
                                    md_file.write('\n')

                        self.stdout.write(self.style.SUCCESS(
                            f'Интерфейс {interface.title} → {interface_md_file_path}'
                        ))
