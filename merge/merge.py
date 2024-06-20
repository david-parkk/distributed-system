import pandas as pd
import os


def merge_excel_files(input_directory, output_file):
    # 병합할 모든 데이터프레임을 저장할 리스트
    dataframes = []

    # input_directory가 실제로 존재하는지 확인
    if not os.path.exists(input_directory):
        print(f"Error: Directory {input_directory} does not exist.")
        return

    # input_directory의 모든 파일을 순회
    for filename in os.listdir(input_directory):
        print(f"Processing file: {filename}")
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            # 엑셀 파일의 전체 경로
            file_path = os.path.join(input_directory, filename)

            try:
                # 엑셀 파일 읽기
                df = pd.read_excel(file_path)
                print(f"Read file successfully: {filename}")

                # 열 이름의 공백 제거
                df.columns = [col.strip() for col in df.columns]

                # 필요한 열이 존재하는지 확인하고, 해당 열의 값이 모두 비어 있지 않은지 확인
                required_columns = ['영업활동으로 인한 현금흐름1', '영업활동으로 인한 현금흐름2', '영업활동으로 인한 현금흐름3']
                if all(col in df.columns for col in required_columns):
                    # 필요한 열 모두가 비어 있지 않은 경우에만 추가
                    if not df[required_columns].isnull().any().any():
                        dataframes.append(df)
                        print(f"Added dataframe from file: {filename}")
                    else:
                        print(f"Warning: File {filename} has missing values in required columns.")
                else:
                    print(f"Warning: File {filename} does not contain all required columns.")
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

    # 병합할 데이터프레임이 있는지 확인
    if dataframes:
        # 모든 데이터프레임을 하나로 병합
        merged_df = pd.concat(dataframes, ignore_index=True)
        try:
            # 병합된 데이터프레임을 엑셀 파일로 저장
            merged_df.to_excel(output_file, index=False)
            print(f"Successfully merged files into {output_file}")
        except Exception as e:
            print(f"Error saving merged file: {e}")
    else:
        print("No valid dataframes to merge.")

# 실행 예시
input_directory = '../엑셀 분할/result2'  # 여러 엑셀 파일이 있는 디렉토리 경로
output_file = 'merged_file.xlsx'  # 병합된 결과를 저장할 엑셀 파일 경로

merge_excel_files(input_directory, output_file)