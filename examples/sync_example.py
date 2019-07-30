"""
DANK MEMER IMGEN API CLIENT
---------------------------
Copyright: Copyright 2019 Melms Media LLC
License: MIT

"""
from imgen import SyncClient

client = SyncClient(token='tokengoeshere')

client.crab.save(text='This is an, example')
