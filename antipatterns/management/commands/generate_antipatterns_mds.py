import os

from django.core.management.base import BaseCommand
from django.db.models import Prefetch

from antipatterns.models import (
    AntiPattern,
    AntiPatternExample,
    Snippet,
    StoryAcceptor,
)


class Command(BaseCommand):
    help = 'Экспорт каждого Анти-паттерна в отдельный Markdown-файл'

    def handle(self, *args, **options):
        examples_qs = AntiPatternExample.objects.prefetch_related(
            'acceptors',
            'snippets',
        )

        anti_patterns = AntiPattern.objects.all().prefetch_related(
            'tags',
            Prefetch('examples', queryset=examples_qs),
        )
        anti_pattern_dir = 'АНТИ-ПАТТЕРНЫ'
        for anti_pattern in anti_patterns:
            tags = anti_pattern.tags.all()
            for tag in tags:
                tag_dir = os.path.join(anti_pattern_dir, str(tag))
                os.makedirs(tag_dir, exist_ok=True)
                anti_pattern_md_filename = os.path.join(tag_dir, f'{anti_pattern.title}.md')
                examples = anti_pattern.examples.all().order_by('order_position')
                with open(anti_pattern_md_filename, 'w', encoding='utf-8') as md_file:
                    md_file.write(f'# Анти-паттерн: "{anti_pattern.title}"\n\n')

                    if anti_pattern.description:
                        md_file.write(f'***\n\n{anti_pattern.description}\n\n')

                    for example in examples:
                        snippets = example.snippets.all().order_by('order_position')
                        md_file.write('***\n\n### Пример\n\n')

                        if example.description:
                            md_file.write(f'{example.description}\n\n')

                        for snippet in snippets:
                            md_file.write(f'**{snippet.status_label}:**\n')
                            md_file.write(f'```{snippet.lang_ident}\n{snippet.code}\n```\n')

                    md_file.write('\n')

                    self.stdout.write(self.style.SUCCESS(
                        f'Анти-паттерн: {anti_pattern_md_filename}'
                    ))
