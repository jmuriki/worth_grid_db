import os

from pathlib import Path

from django.core.management.base import BaseCommand
from django.db.models import Prefetch

from antipatterns.models import (
    AntiPattern,
    AntiPatternExample,
)


class Command(BaseCommand):
    help = 'Экспорт каждого Анти-паттерна в отдельный Markdown-файл и составление каталога'

    def handle(self, *args, **options):
        examples_qs = AntiPatternExample.objects.prefetch_related(
            'acceptors',
            'snippets',
        )
        antipatterns = AntiPattern.objects.all().prefetch_related(
            'tags',
            Prefetch('examples', queryset=examples_qs),
        )
        tags = [tag for tag in AntiPattern.tags.all().distinct().order_by('name')]

        base_dir = 'docs'
        os.makedirs(base_dir, exist_ok=True)

        antipatterns_dir_path = Path(base_dir, 'ЦС', 'АНТИ-ПАТТЕРНЫ')
        os.makedirs(antipatterns_dir_path, exist_ok=True)

        catalog_file_path = Path(base_dir, 'Анти-паттерны.md')
        with open(catalog_file_path, 'w', encoding='utf-8') as catalog_file:
            catalog_file.write(f"# Анти-паттерны\n\n")

            for tag in tags:
                catalog_file.write(f"### {tag.name}\n\n")

                for antipattern in antipatterns.filter(tags=tag).order_by('title'):
                    antipattern_title = antipattern.title
                    antipattern_md_file_path = Path(antipatterns_dir_path, f'{antipattern_title}.md')
                    antipattern_rel_path = os.path.join('../ЦС/АНТИ-ПАТТЕРНЫ/', antipattern_title)
                    antipattern_link = antipattern_rel_path.replace(os.sep, '/')
                    antipattern_encoded_link = antipattern_link.replace(' ', '%20')
                    catalog_file.write(f"- [{antipattern_title}]({antipattern_encoded_link})\n")

                    examples = antipattern.examples.all().order_by('order_position')
                    with open(antipattern_md_file_path, 'w', encoding='utf-8') as antipattern_md_file:
                        antipattern_md_file.write(f'# Анти-паттерн: "{antipattern_title}"\n\n')

                        if antipattern.description:
                            antipattern_md_file.write(f'***\n\n{antipattern.description}\n\n')

                        num_examples = len(examples)
                        for index, example in enumerate(examples):
                            example_number = example.order_position if num_examples > 1 else ''
                            snippets = example.snippets.all().order_by('order_position')
                            antipattern_md_file.write(f'***\n\n### Пример {example_number}\n\n')

                            if example.description:
                                antipattern_md_file.write(f'{example.description}\n\n')

                            for snippet in snippets:
                                antipattern_md_file.write(f'**{snippet.status_label}:**\n')
                                antipattern_md_file.write(f'```{snippet.lang_ident}\n{snippet.code}\n```\n')

                        antipattern_md_file.write('\n')

                    self.stdout.write(self.style.SUCCESS(
                        f'Анти-паттерн: {antipattern_title}'
                    ))


                catalog_file.write("\n")
