import codecs

import requests
import zipfile
import os
import pandas as pd
from bs4 import BeautifulSoup
import re

def extract_cash_flow_data(xml_data):
    soup = BeautifulSoup(xml_data, 'xml')
    cash_flows = []

    target_text = "영업활동으로 인한 현금흐름"
    target_row = soup.find('P', string=lambda text: text and target_text in text)

    if target_row:
        parent_tr = target_row.parent.parent
        third_child = parent_tr.contents[3].text.strip() if len(parent_tr.contents) > 3 else 0
        fifth_child = parent_tr.contents[5].text.strip() if len(parent_tr.contents) > 5 else 0
        seventh_child = parent_tr.contents[7].text.strip() if len(parent_tr.contents) > 7 else 0
    else:
        third_child, fifth_child, seventh_child = 0, 0, 0

    return third_child, fifth_child, seventh_child

def remove_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


import parsing공시자료
def main():
    crtfc_key = '15719e13918826eeafa58e56db3afde7c3418a7d'
    input_excel_path = 'updated_corp_data.xlsx'
    output_excel_path = 'output.xlsx'

    df = pd.read_excel(input_excel_path)

    df['영업활동으로 인한 현금흐름1'] = ""
    df['영업활동으로 인한 현금흐름2'] = ""
    df['영업활동으로 인한 현금흐름3'] = ""
    count=0
    for idx, row in df.iterrows():
        rcept_no = row['rcept_no']
        if ('사업보고서' not in row['report_nm']):
            continue

        count+=1
        if(count==10):
            break;

        print(f"Processing {rcept_no}...")
        result = parsing공시자료.download_and_extract_data(crtfc_key, rcept_no)
        print("result = ", result);
        if(result=='fail'):

            continue;

        if(result[0]==0 and result[1]==0 and result[2]==0):
            continue
        df.at[idx, '영업활동으로 인한 현금흐름1'] = result[0]
        df.at[idx, '영업활동으로 인한 현금흐름2'] = result[1]
        df.at[idx, '영업활동으로 인한 현금흐름3'] = result[2]

    df.to_excel(output_excel_path, index=False)

if __name__ == "__main__":
    main()
