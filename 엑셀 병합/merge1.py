import pandas as pd

def merge(input_excel_file,output_excel_file):

    # 엑셀 파일에서 데이터 불러오기
    df = pd.read_excel(input_excel_file)

    # 필요한 컬럼이 모두 있는 행만 선택
    filtered_df = df.dropna(subset=['영업활동으로 인한 현금흐름1', '영업활동으로 인한 현금흐름2', '영업활동으로 인한 현금흐름3'])

    # 새로운 엑셀 파일로 저장
    filtered_df.to_excel(output_excel_file, index=False)


if __name__ == "__main__":
    for i in range(1, 11):
        print(i)
        input_path = f'../엑셀 분할/result2/output{i}.xlsx'
        output_path = f'./result/output{i}.xlsx'
        merge(input_path, output_path)
