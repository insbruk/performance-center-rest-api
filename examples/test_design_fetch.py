import os; import sys; sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from lxml import etree
from microfocus.perfcenter import PerfCenter

host = "HOST"
domain = "COMPANY"
project = "PROJECT"
login = "tester"
password = "tester"

wp_pc_client = PerfCenter(host=host, domain=domain, project=project)
wp_pc_client.authenticate(login=login, password=password)
xml_parser = etree.XMLParser(remove_blank_text=True)

tests = [
    {
        'name': 'test_design',
        'id': 1000,
    }
]

for test in tests:
    print(test)
    test_id = test['id']
    test_design = wp_pc_client.get_test_design(test_id=test_id).content
    test_design_content = test_design.decode('utf-8')

    test_design_content = etree.fromstring(test_design_content, parser=xml_parser)
    test_design_content = [node for node in test_design_content if etree.QName(node).localname == 'Content'][0]

    test_design_content = etree.tostring(test_design_content, pretty_print=True)
    test_design_content = test_design_content.decode('utf-8')

    test_design_file = f'{test["name"]}.xml'
    with open(test_design_file, 'w') as f:
        f.write(test_design_content)

wp_pc_client.logout()