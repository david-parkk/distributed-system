import pandas as pd

def filter_rows_by_date(file_path, date, date_column="rcept_dt"):
    """
    엑셀 파일에서 특정 날짜에 해당하는 rcept_dt 값을 가지는 행을 필터링하여 리스트로 반환합니다.

    :param file_path: 엑셀 파일 경로
    :param date: 필터링할 날짜 (문자열 형식, 예: '2023-01-01')
    :param date_column: 날짜가 저장된 열 이름 (기본값: 'rcept_dt')
    :return: 특정 날짜에 해당하는 행의 리스트
    """
    print(date)
    # 엑셀 파일 읽기
    df = pd.read_excel(file_path)
    #print(df[date_column])
    #for i in range(df.shape[0]):
    #    print(df.iloc[i])
    # 특정 날짜에 해당하는 행 필터링

    #for col in df[date_column]:
    #    print(col)
    #    print(col==date)
    filtered_rows = df[df[date_column] == date]

    # 행 리스트로 반환
    return filtered_rows.to_dict(orient='records')

# 사용 예시
file_path = 'combined_output.xlsx'
date = 20230320
filtered_rows = filter_rows_by_date(file_path, date)
print(filtered_rows)