import os

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

        mkdocs_dir_name = 'docs'
        os.makedirs(mkdocs_dir_name, exist_ok=True)

        worth_grid_dir_name = 'ЦС'
        interfaces_dir_name = 'ИНТЕРФЕЙСЫ'
        interfaces_dir_path = os.path.join(mkdocs_dir_name, worth_grid_dir_name, interfaces_dir_name)

        interfaces_catalog_filename = f'{interfaces_dir_name.lower().capitalize()}.md'
        interfaces_catalog_file_path = os.path.join(mkdocs_dir_name, interfaces_catalog_filename)
        with open(interfaces_catalog_file_path, 'w', encoding='utf-8') as catalog_file:
            catalog_file.write('# Интерфейсы\n\n')
        
        for interface in interfaces:
            interface_name = interface.subtitle

            interfaces_subcatalogs_paths = []
            interfaces_subcatalogs = interface.subcatalogs.all()
            if interfaces_subcatalogs:
                for subcatalog in interfaces_subcatalogs:
                    subcatalog_dir_name = subcatalog.title
                    interfaces_subcatalogs_paths.append(os.path.join(interfaces_dir_path, subcatalog_dir_name))
            else:
                interfaces_subcatalogs_paths.append(interfaces_dir_path)

            for subcatalog_path in interfaces_subcatalogs_paths:
                os.makedirs(subcatalog_path, exist_ok=True)

                interface_link = os.path.join(
                    f'../', worth_grid_dir_name, interfaces_dir_name, subcatalog_dir_name, interface_name
                )
                encoded_interface_link = interface_link.replace(' ', '%20')

                with open(interfaces_catalog_file_path, 'a', encoding='utf-8') as catalog_file:
                    catalog_file.write('<ul>\n')
                    catalog_file.write('\t<li>\n')
                    catalog_file.write(
                        f'\t\t<img src="../../../../img/{os.path.basename(interface.logo.name)}"\r\
                        alt="logo" style="width: 2em; vertical-align: middle;" />\n'
                    )
                    catalog_file.write(
                        f'\t\t<a href="{encoded_interface_link}" style="margin-left: 5px;">{interface_name}</a>\n'
                    )
                    catalog_file.write('\t</li>\n')
                    catalog_file.write('</ul>\n\n')

                interface_md_filename = f'{interface_name}.md'
                interface_md_file_path = os.path.join(subcatalog_path, interface_md_filename)
                with open(interface_md_file_path, 'w', encoding='utf-8') as md_file:

                    md_file.write('<div style="display: flex; align-items: flex-start; align-items: center;">\n')
                    md_file.write(f'\t<div style="margin-right: 5px;">\n')
                    md_file.write(
                        f'\t\t<img src="../../../../img/{os.path.basename(interface.logo.name)}"\r\
                        alt="logo" style="display: block; width: 4em; height: auto; margin-right: 1rem;" />\n'
                    )
                    md_file.write(f'\t</div>\n')
                    md_file.write(f'\t<div>\n')
                    md_file.write(f'\t\t<h1 style="margin: 0;">{interface.subtitle}</h1>\n')
                    md_file.write('\t\t<p style="margin: 0;">Интерфейс</p>\n')
                    md_file.write('\t</div>\n')
                    md_file.write('</div>\n\n')

                    if interface.description:
                        md_file.write('**Описание:**\n\n')
                        md_file.write(f'{interface.description}\n\n')

                    roles = interface.roles.all().order_by('order_position')
                    for role in roles:

                        md_file.write('***\n\n')
                        md_file.write(
                            '<div style="display: flex; align-items: flex-start; align-items: center;">\n'
                        )
                        md_file.write(f'\t<div style="margin-right: 5px;">\n')
                        md_file.write(
                            f'\t\t<img src="../../../../img/{os.path.basename(role.logo.name)}"\r\
                            alt="logo" style="display: block; width: 3.3em; height: auto; margin-right: 1rem;" />\n'
                        )
                        md_file.write(f'\t</div>\n')
                        md_file.write(f'\t<div>\n')
                        md_file.write(f'\t\t<h2 style="margin: 0; font-size: 22px;">{role.title}</h2>\n')
                        md_file.write('\t\t<p style="margin: 0;">Роль</p>\n')
                        md_file.write('\t</div>\n')
                        md_file.write('</div>\n\n')

                        if role.description:
                            md_file.write('**Описание:**\n\n')
                            md_file.write(f'{role.description}\n\n')

                        functions = role.functions.all().order_by('order_position')
                        for function in functions:
                            md_file.write('***\n\n')
                            md_file.write(f'### 𝑓 {function.job}\n\n')

                            if function.description:
                                md_file.write('**Описание:**\n\n')
                                md_file.write(f'{function.description}\n\n')

                            stories = function.stories.all().order_by('order_position')
                            for story in stories:
                                md_file.write('***\n\n')
                                md_file.write(f'##### {story.title}\n\n')

                                if story.description:
                                    md_file.write('**Описание:**\n\n')
                                    md_file.write(f'{story.description}\n\n')
                                else:
                                    md_file.write(
                                        f'**Типичная История:** {role.title} хочет {function.job} {story.title}.\n\n'
                                    )

                                md_file.write(f'**Кто я:**  {role.title}\n\n')
                                md_file.write(f'**Чего хочу:** {function.job}\n\n')

                                md_file.write(f'**Кто я:**\n\n')
                                md_file.write(f'- {role.title}\n\n')
                                md_file.write(f'**Чего хочу:**\n\n')
                                md_file.write(f'- {function.job}\n\n')

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

                        self.stdout.write(self.style.SUCCESS(
                            f'Интерфейс {interface.title} → {interface_md_file_path}'
                        ))
