# performance-center-python-rest-api
Performance Center (12.5^) REST API Library

# Installation

pip install git+https://github.com/insbruk/performance-center-python-rest-api.git

# Examples 
```python
from microfocus.perfcenter import PerfCenter

prfctr = PerfCenter(
    host='http://<<HOST>>',
    domain="<<DOMAIN>>",
    project="<<PROJECT>>"
)

prfctr.login(
    login='<<login>>',
    password='<<password>>'
)

r = prfctr.get_test_run_status(798)
print(r.status_code)
```
Response:
```json
{
  "ID": 798,
  "Duration": 347,
  "RunState": "Finished",
  "RunSLAStatus": "Not Completed",
  "TestID": 257,
  "TestInstanceID": 109,
  "PostRunAction": "Do Not Collate",
  "TimeslotID": 6599,
  "VudsMode": false
}
```

# For contributors
I am happy for any PR requests, let's fork and provide your changes.
Please look into contribution guidelines.