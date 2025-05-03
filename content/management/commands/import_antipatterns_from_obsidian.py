import re

from pathlib import Path

from django.core.management.base import BaseCommand
from content.models import (
    AntiPattern,
    AntiPatternExample,
    Snippet,
)


SNIPPET_MAP = {
    'Исключение': (True, 'not_fixable'),
    'Плохо': (True, 'fix_required'),
    'Допустимо': (True, 'fix_not_required'),
    'Хорошо': (False, 'fix_not_required'),
}


class Command(BaseCommand):
    help = 'Импортирует .md-файлы с анти-паттернами в модели AntiPattern, Example и Snippet.'

    def add_arguments(self, parser):
        parser.add_argument(
            'root_path',
            type=str,
            nargs='?',
            default="/Users/admin108/Library/Mobile Documents/com~apple~CloudDocs/Documents/PROGRAMMING/DEVMAN/ReviewGym/WorthGrid/ЦЕННОСТНАЯ СЕТКА/3. АНТИ-ПАТТЕРНЫ",
            help='Путь к директории с .md-файлами (будет рекурсивно обработан).'
        )

    def handle(self, *args, **options):
        root = Path(options['root_path'])
        md_files = list(root.rglob('*.md'))
        self.stdout.write(f'Найдено файлов: {len(md_files)}')

        for md_path in md_files:
            with open(md_path, 'r', encoding='utf-8') as file:
                lines = file.read().splitlines()

            # Парсим название Анти-паттерна из названия .md файла
            anti_pattern_title = md_path.stem
            anti_pattern, created = AntiPattern.objects.get_or_create(title=anti_pattern_title)

            # Парсим Группу Анти-паттернов из имени папки
            tag_name = md_path.parent.name
            anti_pattern.tags.add(tag_name)

            state = None  # 'anti_pattern_description' / 'example_description' / 'snippet_type' / 'snippet' / 'snippet_lines'

            anti_pattern_description_lines = []
            example_title = None
            example_description_lines = []
            snippet_lines = []
            snippet_type = None

            for index, line in enumerate(lines):

                # Парсим описание Анти-паттерна
                if state == 'anti_pattern_description':
                    if not line.startswith('>'):
                        anti_pattern.description = "\n".join(anti_pattern_description_lines).strip()
                        anti_pattern.save()
                        state = None
                        continue
                    anti_pattern_description_lines.append(line.lstrip('>').strip('_').strip())
                elif line.startswith(('> [!quote]', '> [!cite]')):
                    state = 'anti_pattern_description'
                    continue

                # Парсим описание Примера
                before_favicon, example_favicon, after_favicon = line.partition('💡')
                if example_favicon:
                    match = re.search(r'\d+', after_favicon.strip())
                    order_position = int(match.group()) if match else 0
                    state = 'example_description'
                    continue
                elif state == 'example_description':
                    if line.startswith('**'):
                        example, _ = AntiPatternExample.objects.get_or_create(
                            anti_pattern=anti_pattern,
                            description="\n".join(example_description_lines).strip(),
                            order_position=order_position,
                        )
                        example_description_lines = []
                        state = 'snippet_type'
                    else:
                        example_description_lines.append(line.lstrip().strip('_').rstrip())
                        continue

                # Парсим Сниппеты Примера
                snippet_type_line = re.match(r'\*\*(.+?):\*\*', line)
                if state == 'snippet_type' and snippet_type_line:
                    snippet_map_ru = snippet_type_line.group(1).strip()
                    snippet_type = SNIPPET_MAP.get(snippet_map_ru)
                    if not snippet_type:
                        self.stdout.write(self.style.ERROR(
                            f"{md_path}:{index+1}: неизвестный тип «{snippet_map_ru}», пропускаем"
                        ))
                        snippet_type = ''
                    print(snippet_type)
                    state = 'snippet'
                elif state == 'snippet' and line.strip().startswith('```'):
                    state = 'snippet_lines'
                elif state == 'snippet_lines' and '```' not in line:
                    snippet_lines.append(line.replace('\t', '    '))
                elif state == 'snippet_lines' and '```' in line:
                    Snippet.objects.get_or_create(
                        example=example,
                        anti_pattern_present=snippet_type[0],
                        fix_status=snippet_type[1],
                        code="\n".join(snippet_lines).strip(),
                    )
                    snippet_lines = []
                    snippet_type = None
                    state = 'snippet_type'
                if state == 'snippet_type' and '***' in line:
                    state = None

        self.stdout.write(self.style.SUCCESS('Импорт завершён.'))
