import os; import sys; sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from microfocus.perfcenter import PerfCenter


host = "HOST"
domain = "COMPANY"
project = "PROJECT"
login = "tester"
password = "tester"

wp_pc_client = PerfCenter(host=host, domain=domain, project=project)
wp_pc_client.authenticate(login=login, password=password)

test_run_id = 2099
files = {
    'VuserLog.zip',  # Output Log
    f'RawResults_{test_run_id}.zip',  # Raw Results
    f'Results_{test_run_id}.zip',  # Analyzed Result
    # 'Reports.zip',  # HTML Report
    # 'output.mdb.zip'                                  # Output Log
    # f'HighLevelReport_{test_run_id}.xls'              # Rich Report
}

r = wp_pc_client.get_test_run_status_extended(run_id=test_run_id)
test_run_date = r.json()['StartTime'].split(' ')[0]
test_run_dir = f'{test_run_date}_Run{test_run_id}'
test_run_path = f'./{test_run_dir}'

if not os.path.exists(test_run_path):
    os.mkdir(test_run_path)
    os.chdir(test_run_path)

wp_pc_client.download_lr_results(
    run_id=test_run_id,
    files=files,
    dst=test_run_path
)

wp_pc_client.logout()
