from .models import Menu


def menu_itens(request):
    """Disponibiliza `menu_itens` em todos os templates (menu dinâmico)."""
    itens = Menu.objects.filter(ativo=True).select_related("conteudo")
    # Esconde itens internos cujo conteúdo esteja desativado
    itens = [i for i in itens if i.eh_externo or (i.conteudo and i.conteudo.ativo)]
    return {"menu_itens": itens}
