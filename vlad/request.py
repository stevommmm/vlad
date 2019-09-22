from cryptography import x509
from cryptography.hazmat.backends import default_backend
from urllib.parse import urlparse
from collections import defaultdict
import base64
import json
import aiohttp
from typing import Union
import logging

logger = logging.getLogger(__name__)


class DockerRequest:
    __slots__ = (
        'user',
        'user_auth_method',
        'req_method',
        'req_uri',
        'req_body',
        'req_headers',
        'req_oids',
        'req_target',
        '_session',
    )

    def __init__(self, data: dict = {}):
        self.user = data.get('User', None)
        self.user_auth_method = data.get('UserAuthNMethod', None)
        self.req_oids = defaultdict(list)
        self.req_oids['OU'] += ['public']
        if self.user_auth_method == 'TLS':
            for cert in data['RequestPeerCertificates']:
                oids = _subject_to_dict(_load_b64_certificate(cert).subject)
                for k, v in oids.items():
                    self.req_oids[k] += v

        self.req_method = data.get('RequestMethod', None)
        self.req_uri = urlparse(data.get('RequestUri', ''))

        # Capture the 'thing' we're targeting with the commands
        self.req_target = '/{}'.format(self.req_uri.path.split('/', 2)[-1].lstrip('/'))

        self.req_body = _json_b64(data.get('RequestBody', None))
        self.req_headers = data.get('RequestHeaders', None)

        self._session = None

    async def _connect(self):
        conn = aiohttp.UnixConnector(path='/var/run/docker.sock')
        self._session = aiohttp.ClientSession(connector=conn)

    async def _docker_resolve(self, path, uid) -> Union[str, None]:
        if not self._session:
            await self._connect()

        async with self._session.get(f'http://localhost/{path}/{uid}') as resp:
            data = await resp.json()
            if 'Name' in data:  # vol net
                return data['Name']
            if 'Spec' in data and 'Name' in data['Spec']:  # svc
                return data['Spec']['Name']
            return None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        if self._session:
            await self._session.close()

    @property
    def is_tls_auth(self):
        return self.user_auth_method == 'TLS'

    @property
    def OU_prefix(self):
        return tuple(self.req_oids['OU'])

    def __repr__(self):
        return f"<Request {self.req_method}:{self.req_target} ({','.join(self.req_oids['OU'])})>"

    async def resolve_network(self, uid):
        logger.debug('Call to resolve ID for networks')
        return await self._docker_resolve('networks', uid)

    async def resolve_volume(self, uid):
        logger.debug('Call to resolve ID for volumes')
        return await self._docker_resolve('volumes', uid)

    async def resolve_service(self, uid):
        logger.debug('Call to resolve ID for services')
        return await self._docker_resolve('services', uid)

    async def resolve_secret(self, uid):
        logger.debug('Call to resolve ID for secrets')
        return await self._docker_resolve('secrets', uid)

    async def resolve_config(self, uid):
        logger.debug('Call to resolve ID for configs')
        return await self._docker_resolve('configs', uid)


class DockerResponse(DockerRequest):
    __slots__ = ('res_body', 'res_header', 'res_code')

    def __init__(self, data: dict = {}):
        super().__init__(data)
        self.res_body = _json_b64(data.get('ResponseBody', None))
        self.res_header = data.get('ResponseHeader', None)
        self.res_code = data.get('ResponseStatusCode', None)

    def __repr__(self):
        return f"<Response {self.req_method}:{self.req_target} ({','.join(self.req_oids['OU'])})>"


def _json_b64(blob):
    if blob is None:
        return blob
    return json.loads(base64.b64decode(blob))


def _load_b64_certificate(b64s: str):
    rcert = base64.b64decode(b64s)
    return x509.load_pem_x509_certificate(rcert, default_backend())


def _get_attrs_oid(subject, oid):
    return [x.value for x in subject.get_attributes_for_oid(oid)]


def _subject_to_dict(subject):
    attrs = defaultdict(list)
    attrs['CN'] = _get_attrs_oid(subject, x509.OID_COMMON_NAME)
    attrs['O'] = _get_attrs_oid(subject, x509.OID_ORGANIZATION_NAME)
    attrs['OU'] = _get_attrs_oid(subject, x509.OID_ORGANIZATIONAL_UNIT_NAME)
    return attrs
