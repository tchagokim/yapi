# yapi
API CRUD simples, gerada por um arquivo YAML apenas, utilizando Python, FastAPI e Peewee

Objetivos:
- Não precisar editar arquivos python, somente o YAML e .env
- Servir para propósitos comuns, nada muito complexo
- Não deixar esse arquivo YAML ficar gigante a ponto de dar trabalho pra manter
- Migrações simples

TODO: 
- Autorizacao
- Relacionamentos
- Outras colunas , so tem str e int por enquanto
- Atribuir tipo da coluna sem precisar do dicionário
- Peewee async + rotinas open/close
