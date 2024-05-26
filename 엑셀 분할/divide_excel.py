import pandas as pd
import math


def split_excel_into_parts(file_path, output_dir, num_parts):
    # 엑셀 파일 읽기
    df = pd.read_excel(file_path)

    # 총 행 수 계산
    total_rows = len(df)

    # 한 파일당 행 수 계산
    rows_per_part = math.ceil(total_rows / num_parts)

    # 분할된 파일 생성
    for part in range(num_parts):
        start_row = part * rows_per_part
        end_row = min((part + 1) * rows_per_part, total_rows)
        chunk_df = df.iloc[start_row:end_row]

        # 파일 저장
        chunk_file_path = f"{output_dir}/split_part_{part + 1}.xlsx"
        chunk_df.to_excel(chunk_file_path, index=False)
        print(f"Saved {chunk_file_path}")


# 예제 사용법
file_path = 'updated_corp_data.xlsx'  # 대용량 엑셀 파일 경로
output_dir = 'divide'  # 출력 디렉토리 경로
num_parts = 10  # 분할할 파일 수

split_excel_into_parts(file_path, output_dir, num_parts)
