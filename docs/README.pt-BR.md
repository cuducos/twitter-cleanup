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
1. Inicie o modo interativo com o comando `python -i cleanup.py`

### Removendo contas inativas

Chame o método `cleanup.unfollow_inactive_for(**kwargs)`.

> Ele aceita qualquer argumento de palavra-chave compatível com o [`timedelta`](https://docs.python.org/3.6/library/datetime.html#timedelta-objects) do Python. **Ele irá confirmar contigo antes de deixar de seguir alguém**.

Por exemplo, para deixar de seguir usuários inativos nos últimos 30 dias:

```python
>>> cleanup.unfollow_inactive_for(days=30)
```

### Bloqueando robôs

Chame o método `soft_block_bots(threshold=None)`.

> O valor `threshold` é um número decimal entre `0` e` 1`. Toda conta pública é analisada usando [Botometer](https://botometer.iuni.iu.edu/#!/) e todas as contas com uma probabilidade maior que o `threshold` serão consideradas um robô. **Ele irá confirmar contigo antes de bloquear qualquer pessoa**.

Por exemplo, para rodar a função com o threshold padrão (`0.75`):

```python
>>> cleanup.soft_block_bots()
```

Ou para rodar com um threshold personalizado:

```python
>>> cleanup.soft_block_bots(threshold=0.68)
```

## Contribuindo

Por favor, formate o seu código com o [Black](https://github.com/ambv/black).
