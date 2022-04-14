#  🐍 Pycemaker - Repositório da API para Dashboard

A aplicaçao server recebe solicitaçoes através de endpoints, coleta os dados do banco de dados MongoDB, trata-os e retorna-os em JSON ou dispara um e-mail com relatório observando um intervalo de tempo.

# 📦 Repositórios integrantes do projeto

| Repositório                                                                                   | Descrição                   |
| --------------------------------------------------------------------------------------------- | --------------------------- |
| [pycemaker-docs](https://github.com/pycemaker/pycemaker-docs)                                 | Apresentação e documentação |
| [pycemaker-dashboard-client](https://github.com/pycemaker/pycemaker-dashboard-client)         | Front-End Dashboard         |
| [pycemaker-dashboard-api](https://github.com/pycemaker/pycemaker-dashboard-api)               | API para Dashboard          |
| [pycemaker-dashboard-middleware](https://github.com/pycemaker/pycemaker-dashboard-middleware) | ETL e Scheduler             |
| [pycemaker-form-client](https://github.com/pycemaker/pycemaker-form-client)                   | Front-End para Formuário    |
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
FLASK_APP=run.py:get_flask_app
FLASK_DEBUG=1
FLASK_ENV=development flask run
EMAIL_FROM=email_para_disparo_de_relatorios_e_alertas
PASSWORD=senha_do_email
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



# 🗺️ Rotas

* **/cpu/<date_now>/<time_range>** (Implementado)
* **/ram/<date_now>/<time_range>** (Implementado)
* `/disk/<date_now>/<time_range>`
* `/reponse_time/<date_now>/<time_range>`
* `/request_count/<date_now>/<time_range>`
* `/http_fail/<date_now>/<time_range>`
> Rotas *GET* que coletam todos os dados anteriores de consumo (CPU, RAM, Disco, Tempo de Resposta, Contagem de Requisições e Falhas HTTP) em um intervalo de tempo em horas **(time_range, ex: 06)** com base na data e hora recebida **(date_now, ex: 10-04-2022-09-43-23)**.

```sh
Response:
    data: array
        com os dados solicitados
        (na mesma estrutura do banco)
    data_anterior: array
        com dados anteriores ao intervalo solicitado
        (na mesma estrutura do banco)
    mean: float
        com média sobre os dados do intervalo solicitado
    mean_anterior: float
        com média sobre os dados do intervalo anterior ao solicitado
    lower: array
        com todos os menores picos de uso
        (na mesma estrutura do banco)
    higher: array
        com todos os menores picos de uso
        (na mesma estrutura do banco)
    criticity_classification: array
        com a classificação de criticidade dos dados solicitados
        na seguinte estrutura:
            {
                criticity: string
                    classificação,
                value: float
                    valor em porcentagem sobre o total de dados
            }
```

* **/cpu/<date_start>** (Implementado)
* **/ram/<date_start>** (Implementado)
* `/disk/<date_start>`
* `/reponse_time/<date_start>`
* `/http_fail/<date_start>`
> Rotas *GET* que coletam todos os dados de consumo (CPU, RAM, Disco, Tempo de Resposta, Contagem de Requisições e Falhas HTTP) a partir da data recebida **(date_start, ex: 10-04-2022-09-43-23)**.

```sh
Response:
    array
        com os dados solicitados
        (na mesma estrutura do banco)
```

* **/report/<date_now>/<time_range>/<email_to>** (Implementado)
> Rota *GET* que dispara criação de relatório e envio de e-mail para o endereço solicitado **(email_to, ex: roberto@email.com)** com todos os dados anteriores de consumo (CPU, RAM, Disco, Tempo de Resposta, Contagem de Requisições e Falhas HTTP) em um intervalo de tempo em horas **(time_range, ex: 06)** com base na data e hora recebida **(date_now, ex: 10-04-2022-09-43-23)**.

```sh
Response:
    msg: "Relatório enviado com sucesso!"
```

# 📂 Estrutura de arquivos
```
.
|___.env                           # guarda variáveis sensíveis da aplicação
|___.gitignore                     # ignore arquivos e pastas em respositório git
|___firebase-settings.json         # guarda chaves de conexão com o servidor Firebase
|___README.md                      # documentação descritiva
|___run.py                         # inicia servidor Flask
|___requirements.txt               # lista as dependências necessárias
|___app
    |_____init__.py                # cria servidor Flask
    |___routes.py                  # classe representativa das rotas
    |___controller
    |   |___cpu.py                 # classes controladoras das rotas cpu
    |   |___disk.py                # classes controladoras das rotas disk
    |   |___http_fail.py           # classes controladoras das rotas http_fail
    |   |___ram.py                 # classes controladoras das rotas ram
    |   |___report.py              # classe controladora da rota report
    |   |___response_time.py       # classes controladoras das rotas response_time
    |___entities
    |   |___cpu.py                 # classe representativa da collection cpu_usage no banco de dados MongoDB
    |   |___disk.py                # classe representativa da collection disk_usage no banco de dados MongoDB
    |   |___http_fail.py           # classe representativa da collection http_fail no banco de dados MongoDB
    |   |___ram.py                 # classe representativa da collection jvm_memory_usage no banco de dados MongoDB
    |   |___response_time.py       # classe representativa da collection response_time no banco de dados MongoDB
    |___services
        |___image_uploader.py      # objeto para upload de imagens no servidor Firebase
        |___mailer.py              # objeto para disparo de e-mails
        |___monitoramento.py       # objeto para coleta de dados de consumo
        |___plot_generator.py      # funções para geração de gráficos
        |___reporter.py            # objeto para criação do relatório
```
