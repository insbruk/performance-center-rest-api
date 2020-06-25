import requests
from base64 import b64encode


class ALM:
    def __init__(self, host, domain, project, fiddler=False):
        self.host = host
        self.domain = domain
        self.project = project
        self.project_rest_api = f'{self.host}/qcbin/rest/domains/{self.domain}/projects/{self.project}'
        self.session = requests.Session()
        if fiddler:
            self.session.proxies = {
                'http': 'http://127.0.0.1:8888',
                'https': 'http://127.0.0.1:8888',
            }

    def is_authenticated(self):
        return self.session.get(f'{self.host}/qcbin/rest/is-authenticated')

    def login(self, login, password):
        self.auth_token = b64encode(f'{login}:{password}'.encode('unicode_escape')).decode('utf-8')
        self.auth_token = f'Basic {self.auth_token}'
        self.session.headers.update(
            {
                'Authorization': self.auth_token,
                'Accept': 'application/json',
            }
        )
        self.session.get(
            url=f'{self.host}/qcbin/authentication-point/authenticate',
        )
        return self.session.post(url=f'{self.host}/qcbin/rest/site-session/')

    def logout(self):
        self.session.delete(
            url=f'{self.host}/qcbin/rest/site-session'
        )
        return self.session.get(
            url=f'{self.host}/qcbin/authentication-point/logout',
        )

    def get_tests(self):
        return self.session.get(
            url=f'{self.project_rest_api}/test',
        )

    def get_defects(self):
        return self.session.get(
            url=f'{self.project_rest_api}/defects',
        )

    def get_list_items(self):
        return self.session.get(
            url=f'{self.project_rest_api}/list-items',
        )

    def get_attachments(self):
        return self.session.get(
            url=f'{self.project_rest_api}/attachments',
        )

    def get_test_run_info(self, run_id):
        return self.session.get(
            f'{self.project_rest_api}/runs/{run_id}',
        )

