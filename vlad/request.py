from cryptography import x509
from cryptography.hazmat.backends import default_backend
from urllib.parse import urlparse
from collections import defaultdict
import base64
import json


class DockerRequest:
    __slots__ = (
        'user',
        'user_auth_method',
        'res_body',
        'res_header',
        'res_code',
        'req_method',
        'req_uri',
        'req_body',
        'req_headers',
        'req_oids',
        'req_target',
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

        # Response
        if 'ResponseBody' in data:
            self.res_body = _json_b64(data.get('ResponseBody', None))
        if 'ResponseHeader' in data:
            self.res_header = data['ResponseHeader']
        if 'ResponseStatusCode' in data:
            self.res_code = data['ResponseStatusCode']
        # Request
        self.req_method = data.get('RequestMethod', None)
        self.req_uri = urlparse(data.get('RequestUri', ''))

        # Capture the 'thing' we're targeting with the commands
        self.req_target = '/{}'.format(self.req_uri.path.split('/', 2)[-1].lstrip('/'))

        self.req_body = _json_b64(data.get('RequestBody', None))
        self.req_headers = data.get('RequestHeaders', None)

    @property
    def is_tls_auth(self):
        return self.user_auth_method == 'TLS'

    @property
    def OU_prefix(self):
        return tuple(self.req_oids['OU'])

    @property
    def OU_vol_prefix(self):
        return tuple(f"/volumes/{bg}" for bg in self.OU_prefix)

    @property
    def OU_svc_prefix(self):
        return tuple(f"/services/{bg}" for bg in self.OU_prefix)

    @property
    def OU_net_prefix(self):
        return tuple(f"/networks/{bg}" for bg in self.OU_prefix)

    def __repr__(self):
        return json.dumps({x: getattr(self, x, None) for x in self.__slots__}, indent=2)


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
