import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


def get_page_contents(driver, company_name, report_nm, date):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find_all('tr')
    is_company_found = False
    is_report_found = False
    count = 0
    for row in rows:
        columns = row.find_all('td')


        for col in columns:
            #print(col)
            if is_company_found:
                time_text = col.text.strip()
                if re.match(r'\d{2}:\d{2}', time_text):
                    print(time_text)
                    return time_text
                is_report_found = False

            if company_name in col.text:
                is_company_found = True
                count = 0

            if count == 4:
                is_company_found = False
            count += 1
    return None


def get_report_time(company_name, report_nm, date):
    # URL 설정
    url = 'https://dart.fss.or.kr/dsac001/mainK.do?selectDate=' + date + '&sort=&series=&mdayCnt=0'
    print(url)
    # Selenium 옵션 설정 (headless)
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("--headless")

    # Chrome 드라이버 시작
    driver = webdriver.Chrome(options=driver_options)
    driver.get(url)

    # 첫 페이지 내용 가져오기
    time_text = get_page_contents(driver, company_name, report_nm, date)
    if time_text:
        driver.quit()
        return time_text

    page_num = 2
    while True:
        try:
            page_button = WebDriverWait(driver, 12).until(
                EC.element_to_be_clickable((By.LINK_TEXT, str(page_num)))
            )
            page_button.click()

            # 페이지 로딩 대기
            WebDriverWait(driver, 10).until(EC.staleness_of(page_button))

            # 새로운 페이지 내용 가져오기
            time_text = get_page_contents(driver, company_name, report_nm, date)
            if time_text:
                driver.quit()
                return time_text

            # 다음 페이지로 이동
            page_num += 1
        except Exception as e:
            # 더 이상 페이지 번호 버튼이 없으면 루프 종료
            print(f"페이지 {page_num}로 이동할 수 없습니다: {e}")
            break

    # 작업이 끝난 후 드라이버 종료
    driver.quit()
    return None


# 엑셀 파일에서 기업 정보 읽기
df_excel = pd.read_excel("../request/23년공시번호+날짜.xlsx", dtype=str)

# 시간 정보를 저장할 새로운 열 추가
df_excel['time'] = None

# 각 기업에 대해 시간 정보 추출 및 업데이트
count=0
for index, row in df_excel.iterrows():
    company_name = row['corp_name']
    report_nm = row['report_nm']
    rcept_dt = row['rcept_dt']

    # 날짜 형식 변경 (YYYYMMDD -> YYYY.MM.DD)
    date = f"{rcept_dt[:4]}.{rcept_dt[4:6]}.{rcept_dt[6:]}"

    time_text = get_report_time(company_name, report_nm, date)
    df_excel.at[index, 'time'] = time_text
    print(f"Processed {company_name} - {report_nm} on {date}: {time_text}")

# 업데이트된 데이터프레임을 엑셀 파일로 저장
df_excel.to_excel("updated_corp_data.xlsx", index=False)