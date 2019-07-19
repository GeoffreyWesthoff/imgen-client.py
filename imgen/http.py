"""
DANK MEMER IMGEN API CLIENT
---------------------------
Copyright: Copyright 2019 Melms Media LLC
License: MIT

"""


from aiohttp import ClientSession
from requests import get as make_get_request
from asyncio import Event, Lock, get_event_loop, sleep, coroutine
from weakref import WeakValueDictionary
from time import sleep as sync_sleep

from io import BytesIO
from .errors import *
from .utils import _parse_ratelimit_header, MaybeUnlock

try:
    from discord import File
except ModuleNotFoundError:
    File = None

BASE = 'https://dankmemer.services'
_locks = WeakValueDictionary()


class _AsyncEndpoint:
    """Endpoint class"""
    def __init__(self, base, token, session, name, params, ratelimit):
        self.BASE = base or BASE
        self._token = token
        self._session = session
        if not token:
            raise NoTokenError
        self.name = name
        self.params = params
        self._global_over = Event(loop=self._session.loop)
        self._global_over.set()

        quanta = ratelimit.split('/')[0]
        duration = ratelimit.split('/')[1].replace('s', '')
        self.ratelimit = (int(quanta), int(duration))
        self._headers = {"Authorization": self._token,
                         "Content-Type": "application/json",
                         "user-agent": "python/imgen-client/aiohttp"}

    @coroutine
    def get(self, **kwargs):
        a1 = ''
        a2 = ''
        u1 = ''
        u2 = ''
        text = ''
        if 'avatar0' in self.params:
            a1 = kwargs.pop('avatar1', None)
            if not a1:
                raise MissingParameterError('avatar1')
        if 'avatar1' in self.params:
            a2 = kwargs.pop('avatar2', '')
            if not a2:
                raise MissingParameterError('avatar2')
        if 'username0' in self.params:
            u1 = kwargs.pop('username1', '')
            if not u1:
                raise MissingParameterError('username1')
        if 'username1' in self.params:
            u2 = kwargs.pop('username2', '')
            if not u2:
                raise MissingParameterError('username2')
        if 'text' in self.params:
            text = kwargs.pop('text', '')
            if not text:
                raise MissingParameterError('text')

        params = {"text": str(text), "username1": str(u1), "username2": str(u2), "avatar1": str(a1), "avatar2": str(a2)}
        for k, v in kwargs.items():
            params[k] = v

        lock = _locks.get(self.name)
        if not lock:
            lock = Lock(loop=self._session.loop)
            _locks[self.name] = lock

        yield from lock.acquire()
        with MaybeUnlock(lock) as maybe_lock:
            for tries in range(5):
                r = yield from self._session.get('%s/api/%s' % (self.BASE, self.name),
                                            headers=self._headers,
                                            params=params)
                remaining = r.headers.get('X-Ratelimit-Remaining')
                if remaining == '0' and r.status != 429:
                    delta = _parse_ratelimit_header(r)
                    maybe_lock.defer()
                    self._session.loop.call_later(delta, lock.release)

                if r.status == 429:
                    retry_after = int(r.headers['retry-after']) / 1000

                    data = yield from r.json()
                    is_global = data.get('global', False)
                    if is_global:
                        self._global_over.clear()
                    yield from sleep(retry_after, loop=self._session.loop)

                    if is_global:
                        self._global_over.set()
                    continue

                if r.status == 200:
                    result = yield from r.read()
                    return BytesIO(result), r.headers['Content-Type'].split('/')[1]

                if r.status in (500, 502):
                    yield from sleep(1 + tries * 2, loop=self._session.loop)
                    continue
                result = yield from r.text()

                if r.status == 401:
                    raise IncorrectTokenError
                elif r.status == 403:
                    raise Forbidden
                elif r.status == 400:
                    raise BadRequest(result)
                elif r.status == 404:
                    raise NotFound(result)
            raise HTTPError(result)

    @coroutine
    def get_as_discord(self, **kwargs):
        if not File:
            raise NoDiscordInstalled
        r, ext = yield from self.get(**kwargs)
        r.seek(0)
        return File(filename=self.name + '.%s' % ext, fp=r)

    @coroutine
    def save(self, filename=None, **kwargs):
        if not filename:
            filename = self.name
        r, ext = yield from self.get(**kwargs)
        filepath = filename + '.%s' % ext
        r.seek(0)
        with open(filepath, 'wb') as f:
            f.write(r.read())
            f.close()


class _SyncEndpoint:
    def __init__(self, base, token, name, params, ratelimit):
        self.BASE = base or BASE
        self.token = token
        if not token:
            raise NoTokenError
        self.name = name
        self.params = params
        quanta = ratelimit.split('/')[0]
        duration = ratelimit.split('/')[1].replace('s', '')
        self._global_over = True
        self.ratelimit = (int(quanta), int(duration))
        self.headers = {"Authorization": self.token,
                        "Content-Type": "application/json",
                        "user-agent": "python/imgen-client/requests"}

    def get(self, **kwargs):
        a1 = ''
        a2 = ''
        u1 = ''
        u2 = ''
        text = ''
        if 'avatar0' in self.params:
            a1 = kwargs.pop('avatar1', None)
            if not a1:
                raise MissingParameterError('avatar1')
        if 'avatar1' in self.params:
            a2 = kwargs.pop('avatar2', None)
            if not a2:
                raise MissingParameterError('avatar2')
        if 'username0' in self.params:
            u1 = kwargs.pop('username1', None)
            if not u1:
                raise MissingParameterError('username1')
        if 'username1' in self.params:
            u2 = kwargs.pop('username2', None)
            if not u2:
                raise MissingParameterError('username2')
        if 'text' in self.params:
            text = kwargs.pop('text', None)
            if not text:
                raise MissingParameterError('text')

        params = {"text": text, "username1": u1, "username2": u2, "avatar1": a1, "avatar2": a2}
        for k, v in kwargs.items():
            params[k] = v

        for tries in range(5):
            r = make_get_request('%s/api/%s' % (self.BASE, self.name),
                                 headers=self.headers,
                                 params=params)
            if not self._global_over:
                continue

            if r.status_code == 429:
                retry_after = int(r.headers['retry-after']) / 1000

                data = r.json()
                is_global = data.get('global', False)
                if is_global:
                    self._global_over = False
                sync_sleep(retry_after)

                if is_global:
                    self._global_over = True
                continue

            if r.status_code == 200:
                result = r.content
                return BytesIO(result), r.headers['Content-Type'].split('/')[1]

            if r.status_code in (500, 502):
                sync_sleep(1 + tries * 2)
                continue
            result = r.text

            if r.status_code == 401:
                raise IncorrectTokenError
            elif r.status_code == 403:
                raise Forbidden
            elif r.status_code == 400:
                raise BadRequest(result)
            elif r.status_code == 404:
                raise NotFound(result)
            raise HTTPError(result)

    def get_as_discord(self, **kwargs):
        r, ext = self.get(**kwargs)
        return File(filename=self.name + '.%s' % ext, fp=r)

    def save(self, filename=None, **kwargs):
        if not filename:
            filename = self.name
        r, ext = self.get(**kwargs)
        filepath = filename + '.%s' % ext
        r.seek(0)
        with open(filepath, 'wb') as f:
            f.write(r.read())
            f.close()


class SyncClient:
    """
    NOTE: If you are writing a Discord Bot, we strongly recommend using AsyncClient instead.
    Using SyncClient can cause your bot to stop working correctly under high load!
    Bear in mind also, that only the async client supports ratelimit buckets.
    If you are using the synchronous client, you must ensure your users do not cause a ratelimit
    """
    def __init__(self, base=None, token=None):
        self.BASE = base or BASE
        self.token = token

        if not token:
            raise NoTokenError

        self.endpoints = self.load_endpoints()

    def load_endpoints(self):
        endpoints = list()
        endpoints_raw = make_get_request('%s/endpoints.json' % self.BASE).json().get('endpoints', None)
        if not endpoints_raw:
            raise NoEndpointsError
        for endpoint in endpoints_raw:
            endpoints.append(endpoint['name'])
            e = _SyncEndpoint(self.BASE,
                              self.token,
                              endpoint['name'],
                              endpoint['parameters'],
                              endpoint['ratelimit'])
            setattr(self, endpoint['name'], e)
        return tuple(endpoints)


class AsyncClient:
    def __init__(self, base=None, token=None, session=None, loop=None):
        self.BASE = base or BASE
        self.token = token
        if not token:
            raise NoTokenError
        self.loop = get_event_loop() if not loop else loop
        self.session = session or ClientSession(loop=self.loop)
        self.endpoints = self.load_endpoints()

    def load_endpoints(self):
        endpoints = list()
        endpoints_raw = make_get_request('%s/endpoints.json' % self.BASE).json().get('endpoints', None)
        if not endpoints_raw:
            raise NoEndpointsError
        for endpoint in endpoints_raw:
            endpoints.append(endpoint['name'])
            e = _AsyncEndpoint(self.BASE,
                               self.token,
                               self.session,
                               endpoint['name'],
                               endpoint['parameters'],
                               endpoint['ratelimit'])
            setattr(self, endpoint['name'], e)
        return tuple(endpoints)










