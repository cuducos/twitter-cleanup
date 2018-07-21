# Twitter Clean-up

Um pequeno script para limpar seu perfil no Twitter:

* removendo usuários que não tweetam há algum tempo
* soft-bloking de bots (bloqueia e desbloqueia a conta imediatamente, por isso ela para de te seguir)

## Requisitos

* Python 3.6
* [Twitter API keys](https://apps.twitter.com/) especificados no arquivo `.env.sample`
* [Botometer API key](https://market.mashape.com/OSoMe/botometer) nomeado como `MASHAPE_KEY` no `.env.sample`

## Executando

Dentro de um _virtualenv_ Python:

1. Copie o arquivo `.env.sample` nomeando como `.env` e adicione suas credenciais
1. Instale as dependências rodando o comapndo `pip install -r requirements.txt`
1. Inicie o modo interativo com o comando `python -i cleanup.py`

### Removendo contas inativas

Chame o método `cleanup.unfollow_inactive_for(**kwargs)`.

> Aceita qualquer argumento de palavra-chave compatível com o Python [`timedelta`](https://docs.python.org/3.6/library/datetime.html#timedelta-objects). **Ele irá te questionar antes de deixar de seguir alguém**.

Por exemplo, para deixar de seguir usuários inativos nos últimos 30 dias:

```python
>>> cleanup.unfollow_inactive_for(days=30)
```


### Soft-blocking bots

Chame a função `soft_block_bots(threshold=None)`.

> O valor `threshold` é um` float` entre `0` e` 1`. Toda conta pública é analisada usando [Botometer] (https://botometer.iuni.iu.edu/#!/) e todas as contas com uma probabilidade maior que o `threshold` seriam consideradas um bot. ** Ele irá perguntar antes de bloquear qualquer pessoa **.

Por exemplo, para rodar a função com o threshold padrão (`0.75`):

```python
>>> cleanup.soft_block_bots()
```

Ou para rodar com um threshold específico:

```python
>>> cleanup.soft_block_bots(threshold=0.68)
```

## Contribuindo

Por favor, formate o seu código com o [Black](https://github.com/ambv/black).
