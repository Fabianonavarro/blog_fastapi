💸 API Bancária com FastAPI

Projeto desenvolvido como parte da formação na DIO, aplicando conceitos modernos de desenvolvimento backend com Python e FastAPI.
A API simula operações bancárias como criação de usuários, contas, depósitos, saques e transferências — com deploy gratuito no Render.

🚀 Deploy

🔗 API Online: https://blog-fastapi-4qn8.onrender.com

📘 Documentação Swagger: https://blog-fastapi-4qn8.onrender.com/docs

🧠 Funcionalidades

Cadastro de usuários

Criação de contas bancárias

Consulta de saldo

(Futuro) Depósitos, saques e transferências

Validação de dados com Pydantic

Migrações com Alembic

Deploy com Render (PostgreSQL em produção)

Configuração via variáveis de ambiente

📌 Rotas da API (versão atual)
🏁 Rota Raiz

GET /
Retorna status da API, contagem de usuários e contas.

👤 Usuários
➕ Criar usuário

POST /usuarios/
Cria um novo usuário com os dados enviados.

💳 Contas
➕ Criar conta bancária

POST /contas/
Cria uma nova conta associada a um usuário existente.

💰 Ver saldo

GET /contas/{conta_id}/saldo
Retorna o saldo de uma conta específica.

📘 Schemas disponíveis

Conta

Usuario

ValidationError

HTTPValidationError

Schemas definem o padrão de entrada e saída dos dados através do Pydantic.

✔️ Resumo das Rotas
Método	Rota	Descrição
GET	/	Rota raiz
POST	/usuarios/	Criar usuário
POST	/contas/	Criar conta
GET	/contas/{conta_id}/saldo	Ver saldo da conta
📦 Instalação Local
# Clone o repositório
git clone https://github.com/Fabianonavarro/blog_fastapi.git
cd blog_fastapi

# Instale as dependências
poetry install

# Execute as migrações
alembic upgrade head

# Rode a aplicação
uvicorn main:app --reload

📁 Estrutura do Projeto
blog_fastapi/
├── crud.py
├── database.py
├── exceptions.py
├── exit
├── main.py
├── models.py
├── poetry.lock
├── pyproject.toml
├── README.md
├── render.yaml
├── run.py
├── schemas.py
├── __init__.py
│
└── routers/
    ├── usuarios.py
    └── __init__.py

🧪 Teste Rápido
curl -X POST https://blog-fastapi-4qn8.onrender.com/usuarios/ \
-H "Content-Type: application/json" \
-d '{
  "nome": "João Silva",
  "cpf": "12345678900",
  "data_nascimento": "1990-05-20",
  "endereco": "Rua das Flores, 123",
  "senha": "senha123"
}'

📎 Recursos Adicionais

🔗 Repositório GitHub: https://github.com/Fabianonavarro/blog_fastapi

🔗 DIO.me

👨‍💻 Autor

Feito com 💙 por Fabiano Navarro
📎 GitHub: (adicione seu link aqui)