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

## Funcionalidades implementadas

- CRUD completo para **profissionais da saúde**
- CRUD completo para **consultas** vinculadas a profissionais
- Busca de consultas pelo **ID do profissional**
- **Autenticação JWT**
- Segurança:
  - Sanitização de inputs
  - Prevenção de SQL Injection
  - CORS configurado
- Logs estruturados (DRF Logger + Sentry)
- Containerização com Docker e PostgreSQL
- CI com GitHub Actions (lint, testes, build)
- Documentação automática (Swagger / Redoc)

## Fluxo de desenvolvimento e CI/CD

- **Branch principal:** `main`
- **Pipeline:** `.github/workflows/ci.yml`

  - Lint: flake8
  - Testes: Django `APITestCase`
  - Build: Docker
- **Deploy:** pipeline pronto para AWS Elastic Beanstalk (deploy real não implementado por questões de inviabilidade)

## Logs e monitoramento

- Logs da aplicação em `logs/app.log`
- Sentry captura erros críticos em produção e staging
- Monitoramento de requests via DRF Logger

## Observações técnicas

- Autenticação JWT facilita integração futura com front-end e microserviços
- DRF-Spectacular fornece documentação clara e gerenciável
- Docker + PostgreSQL garante replicabilidade do ambiente em qualquer máquina
- Decisões de design priorizam **segurança, manutenção e legibilidade**

## Melhorias futuras

- Integração com **Assas** para split de pagamento
- Deploy multi-ambiente com **rollback automático**
- CI/CD completo com **staging e produção**
- Monitoramento avançado via Sentry + Prometheus

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
