Reference
=========

This explains how to use imgen-client

SyncClient
===========

.. class:: imgen.SyncClient(token)

    A synchronous wrapper for the Dank Memer imgen

    **Parameters**

    * base(Optional) - Set a different base URL if you are selfhosting

    .. py:attribute:: base
    String: The base URL where imgen is located

    .. py:attribute:: token
    String: The authorization token required for sending requests

    .. py:attribute:: endpoints
    Tuple: Contains every endpoint name that imgen has at this moment
    All endpoints are attributes on this class!

    .. py:function:: <endpoint>.get()
    **Kwargs**

    * avatar_1
    * avatar_2
    * username_1
    * username_2
    * text

    Please see https://dankmemer.services/documentation on how to use these parameters and which endpoints are available!


    Returns BytesIO, which is similiar to a file

    .. py:function:: <endpoint>.get_as_discord()
    **Kwargs**

    * avatar_1
    * avatar_2
    * username_1
    * username_2
    * text

    Please see https://dankmemer.services/documentation on how to use these parameters and which endpoints are available!


    Returns discord.File, which you can immediately send with a discord.py bot.

    .. py:function:: <endpoint>.save(filename)
    **Kwargs**

    * avatar_1
    * avatar_2
    * username_1
    * username_2
    * text

    Please see https://dankmemer.services/documentation on how to use these parameters and which endpoints are available!


    Saves the generated image to the path set in filename


AsyncClient
===========
.. class:: imgen.AsyncClient(token)

    An asynchronous wrapper for the Dank Memer imgen

    **Parameters**

    * base(Optional) - Set a different base URL if you are selfhosting
    * loop(Optional) - Pass an asyncio event loop
    * session(Optional) - Pass an aiohttp.ClientSession

    .. py:attribute:: base
    String: The base URL where imgen is located

    .. py:attribute:: token
    String: The authorization token required for sending requests

    .. py:attribute:: endpoints
    Tuple: Contains every endpoint name that imgen has at this moment
    All endpoints are attributes on this class!

    .. py:attribute:: loop
    The event loop for the async client

    .. py:attribute:: session
    The aiohttp session for the async client

    .. py:function:: *await* <endpoint>.get()
    **Kwargs**

    * avatar_1
    * avatar_2
    * username_1
    * username_2
    * text

    Please see https://dankmemer.services/documentation on how to use these parameters and which endpoints are available!


    Returns BytesIO, which is similiar to a file

    .. py:function:: *await* <endpoint>.get_as_discord()
    **Kwargs**

    * avatar_1
    * avatar_2
    * username_1
    * username_2
    * text

    Please see https://dankmemer.services/documentation on how to use these parameters and which endpoints are available!


    Returns discord.File, which you can immediately send with a discord.py bot.

    .. py::: *await* <endpoint>.save(filename)
    **Kwargs**

    * avatar_1
    * avatar_2
    * username_1
    * username_2
    * text

    Please see https://dankmemer.services/documentation on how to use these parameters and which endpoints are available!


Saves the generated image to the path set in filename
