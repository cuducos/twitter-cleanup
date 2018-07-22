# Twitter Clean-up

> [🇬🇧 English version](../README.md)

Um pequeno script para limpar seu perfil no Twitter:

* removendo usuários que não tweetam há algum tempo
* _soft-blocking_ de robôs (bloqueia e desbloqueia a conta imediatamente, por isso ela para de te seguir)

## Requisitos

* Python 3.6
* [Chaves da API do Twitter](https://apps.twitter.com/) especificados no arquivo `.env.sample`
* [Chavae da API do Botometer](https://market.mashape.com/OSoMe/botometer) nomeado como `MASHAPE_KEY` no `.env.sample`

## Executando

Dentro de um _virtualenv_ do Python:

1. Copie o arquivo `.env.sample` nomeando como `.env` e adicione suas credenciais
1. Instale as dependências rodando o comando `pip install -r requirements.txt`
1. Execute o programa com `python -m twitter_cleanup` e siga as instruções

## Contribuindo

Por favor, formate o seu código com o [Black](https://github.com/ambv/black).
