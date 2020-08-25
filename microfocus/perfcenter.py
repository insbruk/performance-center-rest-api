import os
import io
import json
import zipfile
import requests
from base64 import b64encode


class PerfCenter:
    # This class provides ability to create and run load tests, upload vugen scripts, get test status
    # and etc, without using the Performance Center user interface (by using REST API)
    # For all POST requests, the default Content-Type is application/xml.
    # To pass the request data in JSON format, use header Content-type: application/json.
    # For all requests that return data, the default Accept is application/xml.
    # To request that data be returned in JSON format, use header Accept: application/json.
    def __init__(self, host, domain, project, fiddler=False):
        self.host = host
        self.domain = domain
        self.project = project
        self.project_rest_api = f"{self.host}/LoadTest/rest/domains/{self.domain}/projects/{self.project}"
        self.session = requests.Session()
        if fiddler:
            self.session.proxies = {
                'http': 'http://127.0.0.1:8888',
                'https': 'http://127.0.0.1:8888',
            }

    def authenticate(self, login, password):
        # Logs the user on to the server and returns LW-SSO (Light Weight Single Sign On) and
        # QCSession cookies for use with all subsequent requests.
        self.auth_token = b64encode(f"{login}:{password}".encode("unicode_escape")).decode("utf-8")
        self.auth_token = f"Basic {self.auth_token}"
        self.session.headers.update(
            {
                'Authorization': self.auth_token,
                'Accept': 'application/json',
            }
        )
        return self.session.get(
            url=f'{self.host}/LoadTest/rest/authentication-point/authenticate',
        )

    def logout(self):
        # Ends the session and cancels the authentication cookie.
        return self.session.get(
            url=f'{self.host}/LoadTest/rest/authentication-point/logout',
        )

    def get_domains(self):
        # Gets the domains list for the authenticated user.
        return self.session.get(
            url=f'{self.host}/LoadTest/rest/domains',
        )

    def get_projects(self):
        # Gets the projects list for a domain for the authenticated user.
        return self.session.get(
            url=f'{self.host}/LoadTest/rest/domains/{self.domain}/projects',
        )

    def analyze_test_results(self, run_id):
        # Starts a late analyze for a run.
        return self.session.post(
            url=f'{self.project_rest_api}/Runs/{run_id}/analyze',
        )

    def collate_test_results(self, run_id):
        # Starts a late collate for a run.
        return self.session.post(
            url=f'{self.project_rest_api}/Runs/{run_id}/collate',
        )

    def get_test_groups(self, test_id):
        # Gets all groups from a test.
        return self.session.get(
            url=f'{self.project_rest_api}/tests/{test_id}/Groups',
        )

    def delete_test_groups(self, test_id):
        # Deletes all groups from a test.
        return self.session.delete(
            url=f'{self.project_rest_api}/tests/{test_id}/Groups',
        )

    def get_test_group_data(self, test_id, group_name):
        # Gets the data on the group.
        return self.session.get(
            url=f'{self.project_rest_api}/tests/{test_id}/Groups/{group_name}',
        )

    def add_or_update_test_group(self, test_id, group_name, group_definition):
        # Adds or updates the group.
        # TODO: check if it works.
        # https://admhelp.microfocus.com/pc/en/all/api_refs/Performance_Center_REST_API/Performance_Center_REST_API.htm#test_entity_xml.htm
        return self.session.put(
            url=f'{self.project_rest_api}/tests/{test_id}/Groups/{group_name}',
            data={
                '': group_definition,
            },
        )

    def delete_group_from_test(self, test_id, group_name):
        # Removes the group from the test.
        return self.session.delete(
            url=f'{self.project_rest_api}/tests/{test_id}/Groups/{group_name}',
        )

    def get_test_group_rts(self, test_id, group_name):
        # Gets the runtime settings for the group.
        return self.session.get(
            url=f'{self.project_rest_api}/tests/{test_id}/Groups/{group_name}/RTS',
        )

    def update_test_group_rts(self, test_id, group_name, group_rts):
        # Gets the runtime settings for the group.
        # https://admhelp.microfocus.com/pc/en/all/api_refs/Performance_Center_REST_API/Content/RTS_entity_xml.htm
        return self.session.put(
            url=f'{self.project_rest_api}/tests/{test_id}/Groups/{group_name}/RTS',
            data={
                '': group_rts,
            },
        )

    def get_test_results_metadata(self, run_id):
        return self.session.get(
            url=f'{self.project_rest_api}/Runs/{run_id}/Results',
        )

    def get_test_run_status(self, run_id):
        return self.session.get(
            url=f'{self.project_rest_api}/Runs/{run_id}',
        )

    def get_test_run_status_extended(self, run_id):
        return self.session.get(
            url=f'{self.project_rest_api}/Runs/{run_id}/Extended',
        )

    def get_test_description(self, test_id):
        return self.session.get(
            url=f'{self.project_rest_api}/tests/{test_id}',
        )

    def download_test_results_files(self, run_id='', files='', dir=''):
        test_results = self.get_test_results_metadata(run_id=run_id)
        test_results = json.loads(test_results)
        for tr_file in test_results:
            for f in files:
                if tr_file['Name'] == f:
                    file_dir = 'lr_{}_{}'.format(tr_file['Type'].replace(' ', '_').lower(), run_id)
                    if file_dir in os.listdir(dir):
                        print(f'{f} are already there')
                        continue
                    file_id = str(tr_file['ID'])
                    req = self.session.get(
                        url=f'{self.project_rest_api}/Runs/{run_id}/Results/{file_id}/data',
                    )
                    if req.ok:
                        z = zipfile.ZipFile(io.BytesIO(req.content))
                        z.extractall(f'{dir}/{file_dir}')
                        print(f'{f} is successfully downloaded!')
                    else:
                        print(f'Error during downloading {f}')

    def download_lr_results(self, date='', run_id='', files='', dst=''):
        if not os.path.exists(dst):
            os.mkdir(dst)
        test_results = self.get_test_results_metadata(run_id=run_id)
        test_results = test_results.json()
        for file in test_results:
            for dwnl_file in files:
                if file['Name'] == dwnl_file:
                    file_dir = 'lr_{}'.format(file['Type'].replace(' ', '_').lower())
                    if file_dir in os.listdir(dst):
                        print(f'{dwnl_file} are already there')
                        continue
                    # print(f'Downloading {dwnl_file} ...')
                    file_id = str(file['ID'])
                    req = self.session.get(
                        url=f'{self.project_rest_api}/Runs/{run_id}/Results/{file_id}/data',
                    )
                    if req.ok:
                        z = zipfile.ZipFile(io.BytesIO(req.content))
                        z.extractall(f'{dst}/{file_dir}')
                        print(f'{dwnl_file} is successfully downloaded!')
                    else:
                        print(f'Error during downloading {dwnl_file}')

    def start_test_run(self, duration_hours, duration_mins, test_id, test_instance_id, post_run_action):
        headers = {
            'Content-Type': 'application/xml',
        }
        data = f"""
            <Run xmlns="http://www.hp.com/PC/REST/API">
                <PostRunAction>{post_run_action}</PostRunAction>
                <TestID>{test_id}</TestID>
                <TestInstanceID>{test_instance_id}</TestInstanceID>
                <TimeslotDuration>
                    <Hours>{duration_hours}</Hours>
                    <Minutes>{duration_mins}</Minutes>
                </TimeslotDuration>
                <VudsMode>false</VudsMode>
            </Run>
            """
        return self.session.post(
            url=f'{self.project_rest_api}/Runs',
            headers=headers,
            data=data,
        )

    def stop_test_run(self, run_id):
        return self.session.post(
            url=f'{self.project_rest_api}/Runs/{run_id}/stop',
        )

    def stop_now_test_run(self, run_id):
        return self.session.post(
            url=f'{self.project_rest_api}/Runs/{run_id}/stopNow',
        )

    def abort_test_run(self, run_id):
        return self.session.post(
            url=f'{self.project_rest_api}/Runs/{run_id}/abort',
        )

    def is_valid_test(self, test_id):
        return self.session.get(
            url=f'{self.project_rest_api}/tests/{test_id}/validity',
        )

    def get_script_metadata(self, script_id):
        return self.session.get(
            url=f'{self.project_rest_api}/scripts/{script_id}',
        )

    def download_vugen_script(self, script_id):
        return self.session.get(
            url=f'{self.project_rest_api}/scripts/{script_id}/zip',
        )

    def delete_vugen_script(self, script_id):
        return self.session.delete(
            url=f'{self.project_rest_api}/scripts/{script_id}',
        )

    def get_vugen_scripts(self):
        return self.session.get(
            url=f'{self.project_rest_api}/scripts',
        )

    def upload_vugen_script(self, script_zip_path, pc_test_folder_path):
        script_xml = f"""
            <Script xmlns="http://www.hp.com/PC/REST/API">
                <TestFolderPath>{pc_test_folder_path}</TestFolderPath>
                <Overwrite>true</Overwrite>
                <RuntimeOnly>true</RuntimeOnly>
                <KeepCheckedOut>false</KeepCheckedOut>
            </Script>
        """
        script_name = os.path.splitext(os.path.basename(script_zip_path))[0]
        with open(script_zip_path, 'rb') as scr_zip_rb:
            files = {
                'file': (f'{script_name}', scr_zip_rb, 'application/x-zip-compressed')
            }
            print(f'Uploading "{script_name}" to "\\\\Performance Center\\{pc_test_folder_path}": in progress')
        return self.session.post(
            url=f'{self.project_rest_api}/Scripts',
            files=files,
            data={
                '': script_xml
            },
        )

    def get_test_version_control_state(self, test_id):
        # Returns the version control state of a test.
        return self.session.get(
            url=f'{self.project_rest_api}/tests/{test_id}/versioncontrol',
        )

    def update_test_version_control_state(self, test_id, version_control):
        # Updates the version control state of a test.
        headers = {
            'Content-Type': 'application/xml',
        }
        return self.session.patch(
            url=f'{self.project_rest_api}/tests/{test_id}/versioncontrol',
            headers=headers,
            data={
                '': version_control,
            },
        )
