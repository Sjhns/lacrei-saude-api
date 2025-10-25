# Lacrei Saúde API

[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.x-green)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-15-blue)](https://www.postgresql.org/)
[![Poetry](https://img.shields.io/badge/poetry-1.8.2-yellow)](https://python-poetry.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

## Descrição

API RESTful para gerenciamento de **profissionais de saúde** e **consultas médicas**, com foco em:

- **Qualidade de código**
- **Segurança dos dados**
- **Boas práticas de desenvolvimento**
- **Documentação clara e interativa**

## Tecnologias utilizadas

- **Linguagem:** Python 3.10  
- **Framework:** Django + Django REST Framework  
- **Autenticação:** JWT (djangorestframework-simplejwt)  
- **Banco de dados:** PostgreSQL  
- **Gerenciamento de dependências:** Poetry  
- **Containerização:** Docker + Docker Compose  
- **CI/CD:** GitHub Actions (Lint, Testes, Build)  
- **Monitoramento:** Sentry + DRF Logger  
- **Documentação da API:** Swagger / Redoc (drf-spectacular)

## Estrutura do projeto

```sh

project_root/
├── core/               # Configurações Django (settings, urls, wsgi)
├── professionals/      # App de profissionais
├── consultations/      # App de consultas
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── .env                # Variáveis de ambiente
├── logs/               # Logs da aplicação
└── README.md

```

## Setup local (desenvolvimento)

### Pré-requisitos

- Python 3.10  
- Poetry  
- Docker & Docker Compose  

### Configuração do ambiente

1. Clone o repositório:

```bash
git clone https://github.com/Sjhns/lacrei-saude-api.git
cd lacrei-saude-api
```

2. Crie arquivo `.env` com as variáveis:

```env
DEBUG=True
SECRET_KEY=chave_super_secreta
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=lacrei_db
POSTGRES_USER=lacrei_user
POSTGRES_PASSWORD=senha_segura
POSTGRES_HOST=db
POSTGRES_PORT=5432

SENTRY_DSN=
DJANGO_SETTINGS_MODULE=core.settings.dev
```

3. Instale dependências:

```bash
poetry install
```

4. Rodar migrations:

```bash
python manage.py migrate
```

5. Criar superusuário:

```bash
python manage.py createsuperuser
```

6. Rodar servidor:

```bash
python manage.py runserver
```

> Ou usando Docker:

```bash
docker-compose up --build
```

## Testes

Execute todos os testes automatizados:

```bash
poetry run python manage.py test
```

- Cobertura mínima inclui CRUD de **profissionais** e **consultas**, testes de erros e autenticação JWT.

## Documentação da API

- **Swagger UI:** `http://localhost:8000/api/docs/swagger/`
- **Redoc UI:** `http://localhost:8000/api/docs/redoc/`
- **Schema JSON:** `http://localhost:8000/api/schema/`

Todos os endpoints exigem **autenticação JWT**, exceto o login.

## Deploy Automático

- Deploy via **GitHub Actions** para **Elastic Beanstalk**

- Etapas do workflow:

  1. Lint e build do projeto
  2. Execução de testes automatizados
  3. Criação do pacote ZIP e upload para S3
  4. Criação de nova versão no Elastic Beanstalk
  5. Atualização do ambiente
  6. **Rollback automático** se deploy falhar
  7. Notificação por e-mail (AWS SES)

- Segredos necessários no GitHub Actions:

  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_REGION`
  - `S3_BUCKET`
  - `EB_APP`
  - `EB_ENV`
  - `SES_FROM_EMAIL` e `SES_TO_EMAIL`

## Checklist de Entrega

| Item                                | Status |
| ----------------------------------- | ------ |
| CRUD completo de profissionais      | ✅      |
| CRUD completo de consultas          | ✅      |
| Busca por ID do profissional        | ✅      |
| JWT e autenticação                  | ✅      |
| Validação de dados e sanitização    | ✅      |
| Docker + PostgreSQL configurados    | ✅      |
| CI/CD (lint, testes, build, deploy) | ✅      |
| Rollback automático                 | ✅      |
| Notificação de deploy por e-mail    | ✅      |
| Documentação Swagger / Redoc        | ✅      |
| Testes com APITestCase              | ✅      |

## Fluxo de Rollback

1. O workflow captura a **versão atual do ambiente** (`PREV_VERSION`)
2. Cria uma **nova versão** com o pacote ZIP do commit
3. Atualiza o ambiente com a nova versão
4. Se o deploy falhar (`Status != Ready`):
   - Executa rollback para `PREV_VERSION`
   - Notifica por e-mail sobre rollback
5. Se o deploy tiver sucesso:
   - Notifica por e-mail sobre deploy bem-sucedido

## Logs e monitoramento

- Logs da aplicação em `logs/app.log`
- Sentry captura erros críticos em produção e staging
- Monitoramento de requests via DRF Logger

## Observações técnicas

- Autenticação JWT facilita integração futura com front-end e microserviços
- DRF-Spectacular fornece documentação clara e gerenciável
- Docker + PostgreSQL garante replicabilidade do ambiente em qualquer máquina
- Decisões de design priorizam **segurança, manutenção e legibilidade**

## Fluxo de Rollback para Deploy da Aplicação

### Visão Geral

O processo de rollback automatizado para reverter deployments problemáticos e garantir a estabilidade do serviço em produção.

### Pré-requisitos

- GitHub Actions configurado
- Tags de versão seguindo semantic versioning (v1.0.0, v1.1.0, etc.)
- Monitoramento de health checks configurado
- Permissões adequadas para o workflow de rollback

### Processo de Rollback

#### 1. Detecção de Falha

- **Automática**: Health checks falham por mais de 3 minutos consecutivos
- **Manual**: Desenvolvedor identifica problema e aciona rollback manual

#### 2. Acionamento do Rollback

- **Automático**: Workflow de CI detecta falha e inicia rollback
- **Manual**: Desenvolvedor acessa repositório no GitHub e inicia workflow de rollback
