from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def get_page_contents(driver, company_name, date):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find_all('tr')
    is_purlovice_found = False
    is_business_report_found = False
    count = 0
    for row in rows:
        columns = row.find_all('td')
        for col in columns:
            print(col)
            if is_business_report_found:
                time_text = col.text.strip()
                if re.match(r'\d{2}:\d{2}', time_text):
                    print(company_name, "의 시간:", time_text)
                    is_business_report_found = False
                    return time_text

            if company_name in col.text:
                is_purlovice_found = True
                count = 0

            if is_purlovice_found and '사업보고서' in col.text:
                #print("찾음")
                #print(col.text)
                is_business_report_found = True
                is_purlovice_found = False

            if count == 4:
                is_purlovice_found = False
            count += 1

def get_all_pages(company_name, date):
    # URL 설정
    url = 'https://dart.fss.or.kr/dsac001/mainK.do?selectDate=' + date + '&sort=&series=&mdayCnt=0'

    # Selenium 옵션 설정 (headless)
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("--headless")

    # Chrome 드라이버 시작
    driver = webdriver.Chrome(options=driver_options)
    driver.get(url)

    # 첫 페이지 내용 가져오기
    get_page_contents(driver, company_name, date)

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
            get_page_contents(driver, company_name, date)

            # 다음 페이지로 이동
            page_num += 1
            print(page_num)
        except Exception as e:
            # 더 이상 페이지 번호 버튼이 없으면 루프 종료
            print(f"페이지 {page_num}로 이동할 수 없습니다: {e}")
            break

    # 작업이 끝난 후 드라이버 종료
    driver.quit()

get_all_pages("펄어비스", "2022.03.22")
