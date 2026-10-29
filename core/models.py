from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Conteudo(models.Model):
    """Página interna do portal. O HTML guardado aqui é só o miolo da página."""

    titulo = models.CharField("título", max_length=100)
    slug = models.SlugField("slug", max_length=100, unique=True)
    conteudo_html = models.TextField(
        "conteúdo HTML",
        help_text="Somente o conteúdo interno (section, article...). "
                  "Não use html, head, body, header, nav ou footer.",
    )
    ativo = models.BooleanField("ativo", default=True)

    class Meta:
        verbose_name = "conteúdo"
        verbose_name_plural = "conteúdos"
        ordering = ["titulo"]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        if self.slug == "inicio":
            return reverse("home")
        return reverse("conteudo", kwargs={"slug": self.slug})


class Menu(models.Model):
    """Item da navegação: aponta para um Conteudo interno ou para uma URL externa."""

    INTERNO = "interno"
    EXTERNO = "externo"
    TIPO_CHOICES = [
        (INTERNO, "Conteúdo interno"),
        (EXTERNO, "Link externo"),
    ]

    titulo = models.CharField("título", max_length=50)
    tipo_destino = models.CharField(
        "tipo de destino", max_length=10, choices=TIPO_CHOICES, default=INTERNO
    )
    ordem = models.PositiveIntegerField("ordem", default=0)
    ativo = models.BooleanField("ativo", default=True)
    conteudo = models.ForeignKey(
        Conteudo,
        verbose_name="conteúdo relacionado",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="itens_menu",
        help_text="Obrigatório quando o destino é conteúdo interno.",
    )
    url_externa = models.URLField(
        "URL externa",
        blank=True,
        help_text="Obrigatório quando o destino é link externo.",
    )

    class Meta:
        verbose_name = "item de menu"
        verbose_name_plural = "itens de menu"
        ordering = ["ordem", "titulo"]

    def __str__(self):
        return f"{self.ordem} - {self.titulo}"

    @property
    def eh_externo(self):
        return self.tipo_destino == self.EXTERNO

    def get_url(self):
        if self.eh_externo:
            return self.url_externa
        return self.conteudo.get_absolute_url() if self.conteudo else "#"

    def clean(self):
        if self.tipo_destino == self.INTERNO and not self.conteudo:
            raise ValidationError(
                {"conteudo": "Selecione um conteúdo para um destino interno."}
            )
        if self.tipo_destino == self.EXTERNO and not self.url_externa:
            raise ValidationError(
                {"url_externa": "Informe a URL para um link externo."}
            )
