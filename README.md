# CRUD API

Este projeto implementa uma API CRUD (Create, Read, Update, Delete) em Python usando Flask e PostgreSQL como banco de dados. O objetivo é fornecer endpoints para gerenciar um cadastro de pacientes, com integração de testes unitários via pytest e documentação via Swagger.

## Tecnologias Utilizadas

- Python
- Flask
- PostgreSQL
- Docker
- Swagger (para documentação)
- pytest (para testes)

## Requisitos

Certifique-se de ter instalado em seu ambiente:

- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Docker](https://docs.docker.com/get-docker/) (opcional)

## Configuração do Ambiente (Com o Docker)
### 1. Clonando o Repositório
No seu terminal/cmd execute os seguintes comandos:
```bash
git clone https://github.com/carlosmorais01/crud-python.git
cd crud-python
```
### 2. Executando o Docker
Abra o Docker Desktop e, no CMD/Terminal, execute:
```bash
docker-compose up --build
```
e aguarde o processo terminar.


## Configuração do Ambiente (Sem o Docker)
### 1. Clonando o Repositório
No seu terminal/cmd execute os seguintes comandos:
```bash
git clone https://github.com/carlosmorais01/crud-python.git
cd crud-python
```
### 2. Criando o .env com informações de Login do PostgreSQL
Crie um arquivo no diretório atual com o nome ".env" e preencha-o utilizando o template abaixo:
```.env
POSTGRES_DB=nome_do_banco_de_dados
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha_do_banco_de_dados
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```
### 3. Instalando dependências
No terminal, instale as dependências presentes no arquivo "requirements.txt":
```bash
pip install -r requirements.txt
```
### 4. Executando o Flask
No terminal, execute os seguintes comandos:
```bash
set FLASK_APP=app.main
flask run
```

## Uso da API
### Endpoints
Abaixo estão descritos os principais endpoints da API.

#### Criar Paciente (POST)
- Endpoint: /pacientes
- Descrição: Cria um novo paciente no banco de dados.
#### Listar Pacientes (GET)
- Endpoint: /pacientes
- Descrição: Retorna uma lista com todos os pacientes cadastrados.
#### Listar Paciente com ID especificado (GET)
- Endpoint: /pacientes{id}
- Descrição: Retorna um paciente com o ID informado.
#### Atualizar Paciente (PUT)
- Endpoint: /pacientes/{id}
- Descrição: Atualiza os dados de um paciente com base no ID informado.
#### Deletar Paciente (DELETE)
- Endpoint: /pacientes/{id}
- Descrição: Remove um paciente da base de dados.
  
## Acessando pelo Swagger
A API está documentada utilizando Swagger e o arquivo de definição está no formato OpenAPI 3.0. Após iniciar a aplicação, acesse a [documentação no navegador](http://localhost:5000/api/docs). A interface permitirá testar todos os endpoints diretamente.

## Acessando pela URL
O acesso da lista de pacientes pode ser feito pela URL http://localhost:5000/pacientes.

## Executando testes
Para a execução dos testes unitários, no CMD execute o seguinte comando no diretório do repositório:
```bash
pytest
```
Se estiver usando o Docker, os testes podem ser executados pela opção "Open In Terminal" no container "flask_app", usando o mesmo comando citado acima.
