#  🐍 Pycemaker - Repositório da API para Dashboard

A aplicaçao server recebe solicitaçoes através de endpoints, coleta os dados do banco de dados MongoDB, trata-os e retorna-os em JSON ou dispara um e-mail com relatório observando um intervalo de tempo.

# 📦 Repositórios integrantes do projeto

| Repositório                                                                                   | Descrição                   |
| --------------------------------------------------------------------------------------------- | --------------------------- |
| [pycemaker-docs](https://github.com/pycemaker/pycemaker-docs)                                 | Apresentação e documentação |
| [pycemaker-dashboard-client](https://github.com/pycemaker/pycemaker-dashboard-client)         | Front-End Dashboard         |
| [pycemaker-dashboard-api](https://github.com/pycemaker/pycemaker-dashboard-api)               | API para Dashboard          |
| [pycemaker-ETL-Flow](https://github.com/pycemaker/pycemaker-etl-flow)                         | Pycemaker ETL Flow          |
| [pycemaker-form-client](https://github.com/pycemaker/pycemaker-form-client)                   | Front-End para Formulário    |
| [pycemaker-form-server](https://github.com/pycemaker/pycemaker-form-server)                   | Api para Formuário          |


# ⚙️ Instruções de Instalação e Uso

<ul>
<li><b>Banco de dados</b></li>
<ul>
<li>Baixe e instale o banco de dados MongoDB:</li>
<a href="https://www.mongodb.com/try/download/community">MongoDB Community 5.0.7</a>
</ul>
</ul>

<ul>
<li><b>Python</b></li>
<ul>
<li>Baixe e instale o ambiente de desenvolvimento Python:</li>
<a href="https://www.python.org/downloads/">Python 3.10.4</a>
</ul>
</ul>

<ul>
<li><b>Dependências</b></li>
<ul>
<li>Abra o terminal na raiz desse repositório e instale as dependências necessárias:
<br/>

```bash
$ pip install -r requirements.txt
```

</li>
</ul>
</ul>

<ul>
<li><b>Criação das Variáveis</b></li>
<ul>
<li>Crie um arquivo <b>.env</b> e configure as variáveis a seguir:
<br/>

```bash
FLASK_APP=run.py:app
FLASK_DEBUG=1
FLASK_ENV=development flask run
EMAIL_FROM=email_para_disparo_de_relatorios_e_alertas
PASSWORD=senha_do_email
MONGO_DB_URL=endereco_de_conexao
FIREBASE_SETTINGS=credenciais_de_conexao
```

</li>
</ul>
<ul>
<li>Configure um serviço no Firebase, gere uma chave e armazena-a na raiz desse repositório com o nome:  <b>firebase-settings.json</b>.
<br/>


</li>
</ul>
</ul>

<ul>
<li><b>Execute a aplicação</b></li>
<ul>
<li>Abra o terminal na raiz desse repositório e execute o comando:
<br/>

```bash
$ py run.py
```
ou
```bash
$ flask run
```

</li>
</ul>
  
  
</ul>

<ul>
<li><b>Execute a aplicação em ambiente virtual</b></li>
<ul>
<li>Abra o terminal na raiz desse repositório e execute os comandos:
<br/>

```bash
$ pip install virtualenv
$ py -m venv env
$ .\env\Scripts\activate
$ py run.py
```
ou
```bash
$ pip install virtualenv
$ py -m venv env
$ .\env\Scripts\activate
$ flask run
```

</li>
</ul>
  
  
</ul>
