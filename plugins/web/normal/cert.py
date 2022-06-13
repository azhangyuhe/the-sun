import ssl
import OpenSSL
from core.my_class import Plugin


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'cert'
        self.type = 'web'
        self.time = '2022-02-02'
        self.author = 'beginner'

    def scan(self, scanner):
        if scanner.scheme == 'https':
            try:
                port = 443
                cert = ssl.get_server_certificate((scanner.domain, port))
                cert_obj = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert.encode())
                certIssue = cert_obj.get_issuer()
                scanner.cert['public_key'] = OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM,
                                                                          cert_obj.get_pubkey()).decode("utf-8")
                scanner.cert['cert_version'] = cert_obj.get_version() + 1
                scanner.cert['cert_serial_number'] = hex(cert_obj.get_serial_number())
                scanner.cert['signature_algorithm '] = cert_obj.get_signature_algorithm().decode()
                scanner.cert['is_expire'] = cert_obj.has_expired()
                scanner.cert['public_key_len'] = cert_obj.get_pubkey().bits()
                scanner.cert['lssure'] = certIssue.commonName
                scanner.cert['ST'] = cert_obj.get_subject().ST
                scanner.cert['L'] = cert_obj.get_subject().L
                scanner.cert['O'] = cert_obj.get_subject().O
                scanner.cert['CN'] = cert_obj.get_subject().CN
                scanner.cert['before'] = cert_obj.get_notBefore().decode()
                scanner.cert['after'] = cert_obj.get_notAfter().decode()
            except Exception as error:
                print('cert error')
