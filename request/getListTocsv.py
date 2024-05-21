import pandas as pd
import requests


def fetch_dart_data(api_key, corp_code, start_date, end_date, corp_cls, pblntf_ty):
    url = "https://opendart.fss.or.kr/api/list.json"
    params = {
        'crtfc_key': api_key,
        'corp_code': corp_code,
        'bgn_de': start_date,
        'end_de': end_date,
        'corp_cls': corp_cls,
        'pblntf_ty': pblntf_ty
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def save_to_excel(corp_codes, api_key, start_date, end_date, corp_cls, pblntf_ty):
    all_data = []

    for corp_code in corp_codes:

        response = fetch_dart_data(api_key, corp_code, start_date, end_date, corp_cls, pblntf_ty)
        if response:
            print(response)
            all_data.extend(response.get('list', []))

    df = pd.DataFrame(all_data)
    #print(df)
    df_selected = df[['corp_code', 'corp_name', 'stock_code', 'report_nm', 'rcept_no']]
    df_selected.to_excel("dart_data.xlsx", index=False)


# 엑셀 파일에서 기업 코드 읽기
df_excel = pd.read_excel("../cvs/corp_data.xlsx", dtype=str)  # 숫자를 문자열로 유지
corp_codes = df_excel['corp_code'].tolist()

# API 요청 및 데이터 저장
api_key = "15719e13918826eeafa58e56db3afde7c3418a7d"
start_date = 20221221
end_date = 20230731
corp_cls = "K"
pblntf_ty = "A"
print(corp_codes[0])
#response = fetch_dart_data(api_key, corp_codes[0], start_date, end_date, corp_cls, pblntf_ty)

save_to_excel(corp_codes, api_key, start_date, end_date, corp_cls, pblntf_ty)