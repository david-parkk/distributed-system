import pandas as pd

import parsing공시자료.parsing공시자료

def main(input_excel_path,output_excel_path):
    crtfc_key = '15719e13918826eeafa58e56db3afde7c3418a7d'


    df = pd.read_excel(input_excel_path)

    df['영업활동으로 인한 현금흐름1'] = ""
    df['영업활동으로 인한 현금흐름2'] = ""
    df['영업활동으로 인한 현금흐름3'] = ""
    count=0
    for idx, row in df.iterrows():
        rcept_no = row['rcept_no']
        if ('사업보고서' not in row['report_nm']):
            continue

        # count+=1
        # if(count==10):
        #     break;

        print(f"Processing {rcept_no}...")

        result = parsing공시자료.parsing공시자료.download_and_extract_data(crtfc_key, rcept_no)
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
    for i in range(1, 11):
        input_path = f'./divide/split_part_{i}.xlsx'
        output_path = f'result2/output{i}.xlsx'
        main(input_path, output_path)
#parsing공시자료.parsing공시자료.extract_cash_flow_data("./divide/split_part_1")

