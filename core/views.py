from django.shortcuts import get_object_or_404, render

from .models import Conteudo


def home(request):
    """Página inicial: exibe o Conteudo de slug 'inicio'."""
    conteudo = Conteudo.objects.filter(slug="inicio", ativo=True).first()
    return render(request, "core/home.html", {"conteudo": conteudo})


def conteudo_detalhe(request, slug):
    """Exibe um Conteudo específico a partir do slug da URL."""
    conteudo = get_object_or_404(Conteudo, slug=slug, ativo=True)
    return render(request, "core/conteudo.html", {"conteudo": conteudo})
