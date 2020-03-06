<table align="center"><tr><td align="center" width="9999">
<img src="https://upload.wikimedia.org/wikipedia/en/thumb/e/ec/Lisa_Simpson.png/220px-Lisa_Simpson.png" align="center" width="100" alt="Project icon">


# LISA

*Lexical Interpreter for Sentiment Analysis*
</td></tr>

</table>    

<div align="center">

>![Version badge](https://img.shields.io/badge/version-0.1.10-silver.svg)
![GraphQl Badge](https://badgen.net/badge/icon/graphql/pink?icon=graphql&label)
[![Docs Link](https://badgen.net/badge/docs/github_wiki?icon=github)](https://github.com/brunolcarli/Lisa/wiki)


</div>

<hr />

[Lisa](https://pt.wikipedia.org/wiki/Lisa_Simpson) é um serviço dedicado à execução e processamento de tarefas de linguagem natural e análise de sentimentos em texto (text mining). O nome é uma referência à fantástica personagem criada por [Matt Groening](https://pt.wikipedia.org/wiki/Matt_Groening). A plataforma também parte integrante do Trabalho de Conclusão de Curso desenvolvido para aquisição do grau de *Bacharel* em Engenharia de Software pela Universidade [Unicesumar](https://www.unicesumar.edu.br/home/).


# Rodando

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
<img src="https://uploaddeimagens.com.br/images/002/520/430/full/Peek_29-11-2019_17-02.gif?1575057764" align="center" width="1000" alt="Project icon">
</td></tr>

</table>    
