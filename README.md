<table align="center"><tr><td align="center" width="9999">
<img src="https://upload.wikimedia.org/wikipedia/en/thumb/e/ec/Lisa_Simpson.png/220px-Lisa_Simpson.png" align="center" width="100" alt="Project icon">


# LISA

*Lexical Interpreter for Sentiment Analysis*
</td></tr>

</table>    

<div align="center">

>![Version badge](https://img.shields.io/badge/version-0.1.17-silver.svg)
![GraphQl Badge](https://badgen.net/badge/icon/graphql/pink?icon=graphql&label)
[![Docs Link](https://badgen.net/badge/docs/github_wiki?icon=github)](https://github.com/brunolcarli/Lisa/wiki)

Demo:
> [![Run on Repl.it](https://repl.it/badge/github/brunolcarli/Lisa)](https://lisa--brunolcarli.repl.co/graphql/?query=query%7B%0A%09lisa%0A%7D)

</div>

<hr />

[Lisa](https://pt.wikipedia.org/wiki/Lisa_Simpson) é um serviço dedicado à execução e processamento de tarefas de linguagem natural e análise de sentimentos em texto (text mining). O nome é uma referência à fantástica personagem criada por [Matt Groening](https://pt.wikipedia.org/wiki/Matt_Groening). A plataforma também parte integrante do Trabalho de Conclusão de Curso desenvolvido para aquisição do grau de *Bacharel* em Engenharia de Software pela Universidade [Unicesumar](https://www.unicesumar.edu.br/home/).


# Rodando

![Linux Badge](https://img.shields.io/badge/OS-Linux-black.svg)
![Apple badge](https://badgen.net/badge/OS/OSX/:color?icon=apple)

Para rodar a plataforma, primeiramente é necessário inicializar um novo ambiente virtual (virtualenv) e instalar as depenências:

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


O serviço estará disponível em `localhost:2154/graphql`

<hr />

<table align="center"><tr><td align="center" width="9999">

## Docker

<img src="https://media.giphy.com/media/l2Jei7zzXNV8xCKzK/giphy.gif" align="center" width="300" alt="Project icon">

</td></tr>

</table>

![docker badge](https://badgen.net/badge/icon/docker?icon=docker&label)

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

<table align="center"><tr><td align="center" width="9999">
<img src="https://i.ibb.co/27dTgKD/LISA-SCREENSAVE.gif" align="center" width="1200" alt="Project icon">
</td></tr>

</table>    
