import os; import sys; sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from microfocus.perfcenter import PerfCenter


host = "HOST"
domain = "COMPANY"
project = "PROJECT"
login = "tester"
password = "tester"

wp_pc_client = PerfCenter(host=host, domain=domain, project=project)
wp_pc_client.authenticate(login=login, password=password)

tests = [
    'test_design',
]

for test in tests:
    test_design_file = f'{test}.xml'
    test_id = 1000
    with open(test_design_file, 'r') as f:
        test_design = f.read()
        r = wp_pc_client.update_test_design(test_id=test_id, payload=test_design)
        print(r.status_code, r.text)

wp_pc_client.logout()