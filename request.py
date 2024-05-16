import requests
URL = 'https://opendart.fss.or.kr/api/list.json?crtfc_key=15719e13918826eeafa58e56db3afde7c3418a7d&corp_code=00307897&bgn_de=20200117&end_de=20240117'

try:
    print("adf")
    response = requests.get(URL)
    response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킴
    
    # Print status code
    print(f"Status Code: {response.status_code}")
    
    # Parse JSON response
    data = response.json()
    
    # Pretty print JSON data
    import json
    print(json.dumps(data, indent=4, ensure_ascii=False))
    
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"Other error occurred: {err}")