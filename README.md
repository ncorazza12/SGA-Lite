# SGA Lite (Entrega - Prática Python)

Projeto simples de um Sistema de Gestão Acadêmica (SGA Lite) com:
- SQLAlchemy (SQLite local)
- Camada de serviços
- API REST com FastAPI
- CLI com Click
- Testes com pytest

## Requisitos
- Python 3.10+
- pip

## Banco de Dados
- **SQLite (local)**: utilizado para desenvolvimento e testes locais.
- **MariaDB / RDS**: suporte opcional. Caso disponível, é possível conectar definindo a URL de conexão no SQLAlchemy.

## Instalação e Execução

### 1. Crie e ative o ambiente virtual
```bash
python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate
