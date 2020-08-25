import os; import sys; sys.path.append(os.path.dirname(os.getcwd()))
from microfocus.perfcenter import PerfCenter

host = "HOST"
domain = "COMPANY"
project = "PROJECT"
login = "tester"
password = "tester"

wp_pc_client = PerfCenter(host=host, domain=domain, project=project)
wp_pc_client.authenticate(login=login, password=password)

to_upload = {
    'local_path': '.',
    'remote_path': 'Subject\\scripts',
    'scripts': [
        'vugen_script',
    ]
}

pc_test_folder_path = to_upload['remote_path']
os.chdir(to_upload['local_path'])

def clear(path):
    return path

def zip_dir(script):
    return f'{script}.zip'

for script in to_upload['scripts']:
    clear(path=script)
    script_zip = zip_dir(script=script)
    response = wp_pc_client.upload_vugen_script(script_zip_path=script_zip,
                                                pc_test_folder_path=pc_test_folder_path)
    print(f'HTTP Status {response.status_code}\n', response.text)
    # os.remove(script_zip)

wp_pc_client.logout()
