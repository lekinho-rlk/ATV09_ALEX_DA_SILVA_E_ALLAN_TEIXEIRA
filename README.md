# ATV09 — Migração do Portal para Django

**Dupla:** Alex da Silva e Allan Teixeira (Turma 523)
**Instituição:** IFAL

## Descrição
Portal da ATV06 migrado para Django. Menu e conteúdos são cadastrados no Django Admin
(models `Menu` e `Conteudo`) e o menu é gerado dinamicamente a partir do banco.

## Tecnologias
Python 3, Django, SQLite, HTML semântico, CSS (Flexbox/Grid, media queries), Git/GitHub.

## Como executar

```bash
# 1. Ambiente virtual
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Dependências
pip install -r requirements.txt

# 3. Migrations
python manage.py makemigrations core
python manage.py migrate

# 4. Superusuário
python manage.py createsuperuser

# 5. Carregar os conteúdos da ATV06 no banco: 5 conteúdos, 2 links externos, 7 itens de menu
python manage.py popular_dados

# 6. Servidor
python manage.py runserver
```

## Acesso
- Portal: http://127.0.0.1:8000/
- Conteúdo: http://127.0.0.1:8000/conteudo/meu-tema/
- Django Admin: http://127.0.0.1:8000/admin/

## Estrutura
- `core/models.py` — `Conteudo` e `Menu`
- `core/views.py`, `core/urls.py` — página inicial e `/conteudo/<slug>/`
- `core/context_processors.py` — menu dinâmico em todos os templates
- `core/templates/core/` — `base.html`, `home.html`, `conteudo.html`
- `core/static/core/` — `css/` e `img/`
- `core/conteudos/` — HTML de cada página (usado pelo `popular_dados`; pode ser colado no Admin)
