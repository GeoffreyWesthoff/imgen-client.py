Welcome to imgen-client's documentation!
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   reference



Indices and tables
==================

* :ref:`search`

Example
=======
.. code-block:: python

   import imgen

   from imgen import SyncClient

   client = SyncClient(token='tokengoeshere')

   client.crab.save(text='This is an, example')
