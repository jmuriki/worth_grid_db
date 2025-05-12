from django.core.management.base import BaseCommand
from django.core.management import call_command

from antipatterns.models import (
    AntiPattern,
    AntiPatternExample,
    AntiPatternExampleStoryAcceptor,
    Snippet,
)
from interfaces.models import (
    InterfaceSubCatalog,
    InterfaceCatalog,
    Interface,
    Role,
    Function,
    Story,
    StoryContext,
    StartPoint,
    StoryAcceptor,
)


class Command(BaseCommand):
    help = 'Запускает кастомные команды Django'

    def handle(self, *args, **options):

        # self.stdout.write(self.style.SUCCESS('Запуск команды import_antipatterns_from_obsidian'))
        # call_command('import_antipatterns_from_obsidian')

        # self.stdout.write(self.style.SUCCESS('Запуск команды import_stories_from_obsidian'))
        # call_command('import_stories_from_obsidian')

        # qs = AntiPatternExampleStoryAcceptor.objects.all()
        # total, _ = qs.delete()
        # self.stdout.write(self.style.SUCCESS(
        #     f'Удалено связей: {total}'
        # ))

        # acceptors = StoryAcceptor.objects.all()
        # examples = AntiPatternExample.objects.all().order_by('anti_pattern__title')
        # if not acceptors.exists() or not examples.exists():
        #     self.stdout.write(self.style.WARNING('Нет акцепторов или примеров для обработки.'))
        #     return

        # for acceptor in acceptors:
        #     for idx, example in enumerate(examples, start=1):
        #         obj, created = AntiPatternExampleStoryAcceptor.objects.get_or_create(
        #             anti_pattern_example=example,
        #             story_acceptor=acceptor,
        #             # comment=example.description,
        #             defaults={'order_position': idx},
        #         )
        #         if created:
        #             self.stdout.write(self.style.SUCCESS(
        #                 f'Создано: Пример "{example}" → Акцептор "{acceptor}" (позиция {idx})'
        #             ))
        #         else:
        #             self.stdout.write(
        #                 f'Пропущено: связь уже существует для Примера "{example}" и Акцептора "{acceptor}"'
        #             )

        # self.stdout.write(self.style.SUCCESS('Запуск команды generate_antipatterns_mds'))
        # call_command('generate_antipatterns_mds')

        # self.stdout.write(self.style.SUCCESS('Запуск команды generate_interfaces_mds'))
        # call_command('generate_interfaces_mds')

        self.stdout.write(self.style.SUCCESS('Все команды успешно выполнены!'))
