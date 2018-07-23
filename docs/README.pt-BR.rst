Twitter Clean-up
================

    `🇬🇧 English version <../README.rst>`_

Um pequeno script para limpar seu perfil no Twitter:

* Parar de seguir usuários que não tuitam há algum tempo
* *Soft-blocking* de robôs (bloqueia e desbloqueia a conta imediatamente, por isso ela para de te seguir)

Requisitos
----------

* Python 3.6
* Configure variáveis de ambiente com suas `chaves da API do Twitter <https://apps.twitter.com/>`_ e com sua `chave da APi do Botometer <https://market.mashape.com/OSoMe/botometer>`_:
    * ``TWITTER_CONSUMER_KEY``
    * ``TWITTER_CONSUMER_SECRET``
    * ``TWITTER_ACCESS_TOKEN_KEY``
    * ``TWITTER_ACCESS_TOKEN_SECRET``
    * ``BOTOMETER_MASHAPE_KEY``

Instalação
----------

Instale o pacote com:

::

    $ pip install twitter-cleanup

Uso
---

Execute o programa com ``twitter-cleanup --help`` e siga as instruções na tela.

Por exemplo, para parar de seguir quem não tuita há 30 dias:

::

    $ twitter-cleanup inactive 30

Ou para dar um *soft-block* em todos os robôs:

::

    $ twitter-cleanup bots

Contribuindo
------------

Por favor, formate o seu código com o `Black <https://github.com/ambv/black>`_.
