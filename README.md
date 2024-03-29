<table align="center"><tr><td align="center" width="9999">

<img src="https://upload.wikimedia.org/wikipedia/en/thumb/e/ec/Lisa_Simpson.png/220px-Lisa_Simpson.png" align="center" width="100" alt="Project icon">

# LISA

*Lexical Interface for Sentiment Analysis*
</td></tr>

</table>    

<div align="center">

> [![Version badge](https://img.shields.io/badge/version-1.1.1-silver.svg)](http://104.237.1.145:2154/graphql/?query=query%20%7B%0A%20%20lisa%0A%7D)

>[![GraphQl Badge](https://badgen.net/badge/icon/graphql/pink?icon=graphql&label)](http://104.237.1.145:2154/graphql/?query=query%20%7B%0A%20%20lisa%0A%7D)
[![Docs Link](https://badgen.net/badge/docs/github_wiki?icon=github)](https://github.com/brunolcarli/Lisa/wiki)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=PPYA5P239NRML&currency_code=USD&source=url)
![docker badge](https://badgen.net/badge/icon/docker?icon=docker&label)

</div>

<hr />

[Lisa](https://pt.wikipedia.org/wiki/Lisa_Simpson) é um serviço dedicado à execução de tarefas de processamento de linguagem natural e análise de sentimentos em texto (text mining). O nome é uma referência à fantástica personagem criada por [Matt Groening](https://pt.wikipedia.org/wiki/Matt_Groening). A plataforma foi parte integrante do Trabalho de Conclusão de Curso desenvolvido para aquisição do grau de *Bacharel* em Engenharia de Software pela Universidade [Unicesumar](https://www.unicesumar.edu.br/home/).

# Consumindo a API

O serviço está disponvível e pode ser acessado através do endpoint `http://104.237.1.145:2154/graphql/` aceitando requisições GraphQl via internet.

Por exemplo:

## Curl

```bash
$ curl -X POST -H "Content-Type: application/json" --data '{ "query": "query{ sentimentExtraction(text: \"A dúvida é o princípio da sabedoria.\") }" }' http://104.237.1.145:2154/graphql/
```

*Saída:*

```
{"data":{"sentimentExtraction":0.03333333333333333}}
```


## Python

```python
import requests

URL = 'http://104.237.1.145:2154/graphql/'
data = '{sentimentExtraction(text: "A dúvida é o princípio da sabedoria")}'
request = requests.post(URL, json={'query': data})

print(request.status_code)  # 200
print(request.text)  # '{"data":{"sentimentExtraction":0.03333333333333333}}'
```

Pode-se utilizar outros métodos e linguagens da mesma forma para consumir a API.

## Playground

Ao acessar diretemente o endpoint de desenvolvimento através do navegador você terá acesso ao [*playground*](http://104.237.1.145:2154/graphql/) onde poderá escrever diretamente as queries para LISA:

<table align="center"><tr><td align="center" width="9999">
<img src="https://i.ibb.co/GQ162Wj/capa-readme.gif" align="center" width="1200" alt="Project icon">
</td></tr>

</table>

## Veja também

- [Get Started Ilustrado](https://github.com/brunolcarli/Lisa/wiki/Noob-Guide---Get-Started);

- [Documentação das consultas disponíveis](https://github.com/brunolcarli/Lisa/wiki/Queries);

- [Estudo de caso](https://github.com/brunolcarli/Lisa/wiki);

<hr />

# Desenvolvedores

## Rodando localmente

![Linux Badge](https://img.shields.io/badge/OS-Linux-black.svg)
![Apple badge](https://badgen.net/badge/OS/OSX/:color?icon=apple)

Para rodar a plataforma, primeiramente é necessário inicializar um novo ambiente virtual (virtualenv) e instalar as dependências:

```
$ make install
```

Crie um arquivo contendo as variáveis de ambiente conforme o `template` disponível em [lisa/environment/](https://github.com/brunolcarli/Lisa/blob/develop/lisa/environment/template) contendo as variáveis para seu ambiente de execução (por exemplo: *develop*)

```
$ source develop
```

Iniciar a plataforma com o comando:

```
$ make run
```


O serviço estará disponível em `localhost:2154/graphql/`

<hr />

<table align="center"><tr><td align="center" width="9999">

# Rodando com Docker

<img src="https://media.giphy.com/media/l2Jei7zzXNV8xCKzK/giphy.gif" align="center" width="300" alt="Project icon">

</td></tr>

</table>


Crie um arquivo `lisa.env` em  `lisa/environment/lisa.env` e adicone as variáveis de ambiente:

Insira e preencha neste arquivo as seguintes variáveis de ambiente:

```
DJANGO_SECRET_KEY=<your_secret_key>
DJANGO_SETTINGS_MODULE=lisa.settings.docker

MYSQL_ROOT_PASSWORD=<your_database_root_password>
MYSQL_USER=<your_database_user>
MYSQL_DATABASE=<your_database_name>
MYSQL_PASSWORD=<your_database_password>
MYSQL_HOST=lisa_db
```

Instale o docker compose:

```
$ pip install docker-compose
```

Suba os containers com:

```
$ make container
```

<hr />
