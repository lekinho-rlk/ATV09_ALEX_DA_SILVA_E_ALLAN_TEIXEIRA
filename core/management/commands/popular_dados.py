from pathlib import Path

from django.core.management.base import BaseCommand

from core.models import Conteudo, Menu

PASTA = Path(__file__).resolve().parent.parent.parent / "conteudos"

# (título, slug, arquivo HTML)
CONTEUDOS = [
    ("Inicial", "inicio", "inicio.html"),
    ("Currículo: Alex", "curriculo-alex", "curriculo-alex.html"),
    ("Tema: Alex", "tema-alex", "tema-alex.html"),
    ("Currículo: Allan", "curriculo-allan", "curriculo-allan.html"),
    ("Tema: Allan", "tema-allan", "tema-allan.html"),
]

LINKS_EXTERNOS = [
    ("GitHub", "https://github.com"),
    ("W3Schools", "https://www.w3schools.com"),
]


class Command(BaseCommand):
    help = "Carrega os conteúdos da ATV06 (5 conteúdos, 2 links externos, 7 itens de menu)."

    def handle(self, *args, **options):
        objs = {}
        for titulo, slug, arquivo in CONTEUDOS:
            html = (PASTA / arquivo).read_text(encoding="utf-8")
            obj, _ = Conteudo.objects.update_or_create(
                slug=slug,
                defaults={"titulo": titulo, "conteudo_html": html, "ativo": True},
            )
            objs[slug] = obj

        ordem = 1
        for titulo, slug, _ in CONTEUDOS:
            Menu.objects.update_or_create(
                titulo=titulo,
                defaults={"tipo_destino": Menu.INTERNO, "conteudo": objs[slug],
                          "url_externa": "", "ordem": ordem, "ativo": True},
            )
            ordem += 1

        for titulo, url in LINKS_EXTERNOS:
            Menu.objects.update_or_create(
                titulo=titulo,
                defaults={"tipo_destino": Menu.EXTERNO, "conteudo": None,
                          "url_externa": url, "ordem": ordem, "ativo": True},
            )
            ordem += 1

        self.stdout.write(self.style.SUCCESS("Dados carregados com sucesso."))
