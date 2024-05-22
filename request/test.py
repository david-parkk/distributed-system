import pandas as pd
import requests
from time import sleep


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


def save_to_excel(corp_codes, api_key, start_date, end_date, corp_cls, pblntf_ty, output_file):
    try:
        # 기존 엑셀 파일을 읽음
        df_existing = pd.read_excel(output_file, dtype=str)
    except FileNotFoundError:
        # 파일이 없으면 빈 데이터프레임을 생성
        df_existing = pd.DataFrame(
            columns=['corp_code', 'corp_name', 'stock_code', 'report_nm', 'rcept_no', 'rcept_dt'])

    all_data = []

    for corp_code in corp_codes:
        response = fetch_dart_data(api_key, corp_code, start_date, end_date, corp_cls, pblntf_ty)
        if response:
            all_data.extend(response.get('list', []))
        sleep(1)  # API 호출 간의 지연 시간 설정

    df_new = pd.DataFrame(all_data)
    df_selected = df_new[['corp_code', 'corp_name', 'stock_code', 'report_nm', 'rcept_no', 'rcept_dt']]

    # 새로운 데이터를 기존 데이터와 결합
    df_combined = pd.concat([df_existing, df_selected]).drop_duplicates(subset=['corp_code', 'report_nm', 'rcept_no'],
                                                                        keep='last')

    # 엑셀 파일로 저장
    df_combined.to_excel(output_file, index=False)


# 엑셀 파일에서 기업 코드 읽기
df_excel = pd.read_excel("../cvs/corp_data.xlsx", dtype=str)  # 숫자를 문자열로 유지
corp_codes = df_excel['corp_code'].tolist()

# API 요청 및 데이터 저장
api_key = "15719e13918826eeafa58e56db3afde7c3418a7d"
start_date = 20221221
end_date = 20230731
corp_cls = "K"
pblntf_ty = "A"

output_file = "dart_data.xlsx"
save_to_excel(corp_codes, api_key, start_date, end_date, corp_cls, pblntf_ty, output_file)
