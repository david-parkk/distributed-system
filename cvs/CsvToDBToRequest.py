import pandas as pd
import mysql.connector

df = pd.read_excel('kosdaq_code.xlsx')

# 한글 종목명 열만 추출
korean_stock_names = df['한글종목명']

# 추출한 데이터 출력
#print(korean_stock_names)
print(type(korean_stock_names))
# for i in range(len(korean_stock_names)):
#     print(korean_stock_names[i])


# MySQL 데이터베이스에 연결
def connect_to_database(host, user, password, database):
    return mysql.connector.connect(
        host=host[0],
        user=user[0],
        password=password[0],
        database=database
    )


# 쿼리 실행 및 데이터 추출
def get_corp_code(cursor, corp_name):
    query = "SELECT corp_code FROM corpcode WHERE corp_name = %s"
    cursor.execute(query, (corp_name,))
    result = cursor.fetchone()
    corp_code = result[0] if result else None
    cursor.fetchall()  # 모든 결과 소비
    return corp_code


# 데이터 저장
def save_to_excel(data):
    df = pd.DataFrame(data, columns=['corp_name', 'corp_code'])
    df.to_excel('corp_data.xlsx', index=False)
    print("Data saved to corp_data.xlsx")


# 메인 함수
def main():
    host = "127.0.0.1", # MySQL 서버 호스트 이름
    user = "root", # MySQL 사용자 이름
    password = "12345678", # MySQL 비밀번호
    database = "dsc" # 데이터베이스 이름


    corp_name = "이스트아시아홀딩스"

    # 데이터베이스 연결
    db_connection = connect_to_database(host, user, password, database)
    cursor = db_connection.cursor()

    data = []

    # 각 종목명에 대해 반복
    for corp_name in df['한글종목명']:
        try:
            # 쿼리 실행 및 corp_code 추출
            corp_code = get_corp_code(cursor, corp_name)

            if corp_code:
                # 데이터 추가
                data.append((corp_name, corp_code))
            else:
                print(f"No corp_code found for corp_name: {corp_name}")
        except Exception as e:
            print(f"Error occurred for corp_name: {corp_name}, Error: {str(e)}")
    # 연결 닫기
    cursor.close()
    db_connection.close()

    # 데이터 저장
    save_to_excel(data)


if __name__ == "__main__":
    main()


