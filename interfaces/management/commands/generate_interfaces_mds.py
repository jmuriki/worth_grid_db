import os

from pathlib import Path
from textwrap import dedent

from django.core.management.base import BaseCommand
from interfaces.models import Interface

class Command(BaseCommand):
    help = 'Экспорт данных каждого Интерфейса в отдельный Markdown-файл и создание Каталога'

    def handle(self, *args, **options):
        interfaces = Interface.objects.prefetch_related(
            'subcatalogs',
            'roles',
            'roles__functions',
            'roles__functions__stories',
            'roles__functions__stories__context_points',
            'roles__functions__stories__start_point',
            'roles__functions__stories__acceptors',
            'roles__functions__stories__acceptors__example_links',
            'roles__functions__stories__acceptors__example_links__anti_pattern_example',
            'roles__functions__stories__acceptors__example_links__anti_pattern_example__snippets',
        )

        base_dir = 'docs'
        os.makedirs(base_dir, exist_ok=True)

        interfaces_dir_path = Path(base_dir, 'ЦС', 'ИНТЕРФЕЙСЫ')
        os.makedirs(interfaces_dir_path, exist_ok=True)

        interfaces_catalog_file_path = Path(base_dir, 'Интерфейсы.md')
        with open(interfaces_catalog_file_path, 'w', encoding='utf-8') as interfaces_catalog_file:
            interfaces_catalog_file.write(dedent('''
                # Интерфейсы\n\n
                <ul>
            '''))

            for interface in interfaces:

                interface_name = interface.subtitle
                interface_rel_link = os.path.join(f'../ЦС/ИНТЕРФЕЙСЫ', interface_name)
                encoded_interface_rel_link = interface_rel_link.replace(' ', '%20')
                interface_catalog_line = dedent(f'''
                    <li>
                        <img src="../img/{os.path.basename(interface.logo.name)}" alt="logo" style="width: 2em; vertical-align: middle;" />
                        <a href="{encoded_interface_rel_link}" style="margin-left: 5px;">{interface_name}</a>
                    </li>
                ''')
                interfaces_catalog_file.write(interface_catalog_line)

                interface_md_filename = f'{interface_name}.md'
                interface_md_file_path = Path(interfaces_dir_path, interface_md_filename)
                with open(interface_md_file_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(dedent(f'''
                        <div class="sticky-header">
                            <div style="display: flex; align-items: flex-start; align-items: center;">
                              <div style="margin-right: 5px;">
                                  <img src="../../../img/{os.path.basename(interface.logo.name)}" alt="logo" style="display: block; width: 4em; height: auto; margin-right: 1rem;" />
                              </div>
                              <div>
                                  <h1 style="margin: 0;">{interface_name}</h1>
                                  <p style="margin: 0;">Интерфейс</p>
                              </div>
                            </div>
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

                        # # 1
                        # md_file.write(dedent(f'''
                        #     ***\n
                        #     <div style="display: flex; align-items: flex-start; align-items: center;">
                        #     \t<div style="margin-right: 5px;">
                        #     \t\t<img src="../../../img/{os.path.basename(role.logo.name)}" alt="logo" style="display: block; width: 3.3em; height: auto; margin-right: 1rem;" />
                        #     \t</div>
                        #     \t<div>
                        #     \t\t<h2 style="margin: 0; font-size: 22px;">{role_title}</h2>
                        #     \t\t<p style="margin: 0;">Роль</p>
                        #     \t</div>
                        #     </div>\n
                        # '''))

                        # # 2
                        # md_file.write(dedent(f'''
                        #     ***\n
                        #     <div>
                        #         <h2 style="margin: 0;">{role_title}</h2>
                        #         <p style="margin: 0;">Роль Пользователя</p>
                        #     </div>\n
                        # '''))

                        # if role.description:
                        #     md_file.write(dedent(f'''
                        #         **Описание:**\n
                        #         {role.description}\n
                        #     '''))

                        functions = role.functions.all().order_by('order_position')
                        for function in functions:
                            job = function.job

                            # # 1
                            # md_file.write(dedent(f'''
                            #     ***\n
                            #     ### 𝑓 {job}\n
                            # '''))

                            # # 2
                            # md_file.write(dedent(f'''
                            #     ***\n
                            #     <div>
                            #         <h3 style="margin: 0;">{job}</h3>
                            #         <p style="margin: 0;">Ключевая Функция</p>
                            #     </div>\n
                            # '''))

                            # if function.description:
                            #     md_file.write(dedent(f'''
                            #         **Описание:**\n
                            #         {function.description}\n
                            #     '''))

                            stories = function.stories.all().order_by('order_position')
                            for story in stories:
                                story_title = story.title
                                story_logo = '✅' if story.got_wanted else '⚠️'

                                # # 1
                                # md_file.write(dedent(f'''
                                #     ***\n
                                #     ##### {story_logo} {story_title}\n
                                # '''))

                                # 2
                                md_file.write(dedent(f'''
                                    <br>
                                    <div class="sticky-subheader">
                                        <br>
                                        <div>
                                            <h2 style="margin: 0;">{role_title}</h2>
                                            <p style="margin: 0;">Роль Пользователя</p>
                                        </div>
                                        <br>
                                        <div>
                                            <h3 style="margin: 0;">{job}</h3>
                                            <p style="margin: 0;">Ключевая Функция</p>
                                        </div>
                                        <br>
                                        <div>
                                            <h4 style="margin: 0;">{story_title} {story_logo}</h4>
                                            <p style="margin: 0;">Типичная История</p>
                                        </div>
                                        <br>
                                    </div>
                                    <br>
                                '''))

                                # # 1
                                # if story.description:
                                #     md_file.write(dedent(f'''
                                #         **Описание:**\n
                                #         {story.description}\n
                                #     '''))
                                # else:
                                #     md_file.write(dedent(f'''
                                #         **Кто я:**\n
                                #         - {role_title}\n
                                #         **Чего хочу:**\n
                                #         - {job} {story_title.lower()}\n
                                #     '''))

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
                                    md_file.write(f'**Акцепторы {got_wanted}а:**\n\n')

                                    acceptors = story.acceptors.all().order_by('order_position')
                                    for acceptor in acceptors:

                                        example_links = acceptor.example_links.all()
                                        if example_links.exists():
                                            relations_dir_rel_path = os.path.join('ЦС', 'СВЯЗИ АКЦЕПТОРОВ')
                                            relations_dir_path = os.path.join(base_dir, relations_dir_rel_path)
                                            os.makedirs(relations_dir_path, exist_ok=True)

                                            relations_filename = f'Связи_Акцептора {acceptor.id}: {acceptor.text}.md'
                                            relations_file_path = os.path.join(relations_dir_path, relations_filename)
                                            with open(relations_file_path, 'w', encoding='utf-8') as relations_file:

                                                # # 1
                                                # relations_file.write(dedent(f'''
                                                #     # Повреждение и удовлетворение Акцептора\n
                                                #     ***\n
                                                #     **Интерфейс:**\n
                                                #     - {interface_name}\n
                                                #     **Роль:**\n
                                                #     - {role_title}\n
                                                #     **Функция:**\n
                                                #     - {job}\n
                                                #     **История:**\n
                                                #     - {story_title}\n
                                                #     **Акцептор {got_wanted}а:**\n
                                                #     - {acceptor.text}\n
                                                #     ***\n
                                                # '''))

                                                # 2
                                                relations_file.write(dedent(f'''
                                                    <div class="sticky-header">
                                                        <br>
                                                        <h1>Повреждение и удовлетворение Акцептора</h1>
                                                    </div>
                                                    <br>
                                                    <div class="sticky-subheader">
                                                        <br>
                                                        <div>
                                                            <h3 style="margin: 0;">{interface_name}</h3>
                                                            <p style="margin: 0;">Интерфейс</p>
                                                        </div>
                                                        <br>
                                                        <div>
                                                            <h3 style="margin: 0;">{role_title}</h3>
                                                            <p style="margin: 0;">Роль Пользователя</p>
                                                        </div>
                                                        <br>
                                                        <div>
                                                            <h3 style="margin: 0;">{job}</h3>
                                                            <p style="margin: 0;">Ключевая Функция</p>
                                                        </div>
                                                        <br>
                                                        <div>
                                                            <h3 style="margin: 0;">{story_title} {story_logo}</h3>
                                                            <p style="margin: 0;">Типичная История</p>
                                                        </div>
                                                        <br>
                                                        <div>
                                                            <h3 style="margin: 0;">{acceptor.text}</h3>
                                                            <p style="margin: 0;">Акцептор {got_wanted}а</p>
                                                        </div>
                                                        <br>
                                                    </div>
                                                    <br>
                                                '''))

                                                for example_link in example_links:
                                                    snippets = example_link.anti_pattern_example.snippets.all()

                                                    if snippets:
                                                        order_position = example_link.anti_pattern_example.order_position
                                                        example_number = order_position if order_position else ''
                                                        anti_pattern_name = example_link.anti_pattern_example.anti_pattern.title
                                                        comment = example_link.comment if example_link.comment else 'ожидается в будущей версии ЦС.'
                                                        relations_file.write(dedent(f'''
                                                            ***\n
                                                            #### Пример {example_number} из Анти-паттерна ["{anti_pattern_name}"](../../../ЦС/АНТИ-ПАТТЕРНЫ/{anti_pattern_name})\n
                                                            **Как обнаружить повреждение Акцептора:** {comment}\n
                                                        '''))

                                                        for snippet in snippets:
                                                            # relations_file.write(f'**{snippet.status_label}:**\n')
                                                            # relations_file.write(f'```{snippet.lang_ident}\n{snippet.code}\n```\n')
                                                            relations_file.write(dedent(f'''
                                                                \r**{snippet.status_label}:**\n
                                                                \r```{snippet.lang_ident}
                                                                \r{snippet.code}
                                                                \r```\n
                                                            '''))

                                            relations_file_link = f'../../../{relations_dir_rel_path}/{relations_filename.replace(".md", "")}'
                                            md_file.write(f'- {acceptor.text} [🔗]({relations_file_link})\n\n')
                                        else:
                                            md_file.write(f'- {acceptor.text}\n\n')

                        self.stdout.write(self.style.SUCCESS(
                            f'Интерфейс {interface.title} → {interface_md_file_path}'
                        ))

            interfaces_catalog_file.write('</ul>\n')
            self.stdout.write(self.style.SUCCESS(
                f'Каталог Интерфейсов → {interfaces_catalog_file_path}'
            ))
