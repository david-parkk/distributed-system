import requests
import zipfile
import os
from bs4 import BeautifulSoup
import re
def extract_cash_flow_data(xml_data):
    soup = BeautifulSoup(xml_data, 'xml')

    cash_flows = []

    # 특정 텍스트가 있는 행을 찾습니다.
    target_text = "영업활동으로 인한 현금흐름"
    target_row = soup.find('P', string=lambda text: text and target_text in text)

    if target_row:
        print("find")
        #print(target_row)
        # target_row의 부모 요소인 TR 태그를 찾습니다.
        parent_tr = target_row.parent.parent
        #print(parent_tr)
        third_child = parent_tr.contents[3].text if len(parent_tr.contents) > 3 else 0
        fifth_child = parent_tr.contents[5].text if len(parent_tr.contents) > 5 else 0
        seventh_child = parent_tr.contents[7].text if len(parent_tr.contents) > 7 else 0


        # try:
        #     # 부모 요소인 TR 태그의 하위 td 태그들을 가져옵니다.
        #     td_tags = parent_tr.find_all('td')
        #     #print(td_tags)
        #     # td_tags에서 인덱스 2와 4에 해당하는 값을 가져옵니다.
        #     cash_flows = [td_tags[2].text.strip(), td_tags[4].text.strip()]
        #
        # except Exception as e:
        #     print("Error occurred:", e)
        #     cash_flows = None

    return third_child,fifth_child,seventh_child
def remove_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
def download_and_extract_data(crtfc_key, rcept_no):
    url = f"https://opendart.fss.or.kr/api/document.xml?crtfc_key={crtfc_key}&rcept_no={rcept_no}"
    result=[]
    # GET 요청 보내기
    response = requests.get(url)
    if response.status_code != 200:
        print("Error:", response.text)
        return

    # zip 파일 저장
    with open('data.zip', 'wb') as f:
        f.write(response.content)

    # zip 파일 압축 해제
    with zipfile.ZipFile('data.zip', 'r') as zip_ref:
        zip_ref.extractall('extracted_data')

    # XML 파일 읽기 및 출력
    for filename in os.listdir('extracted_data'):
        if filename.endswith('.xml'):
            with open(os.path.join('extracted_data', filename), 'r') as xml_file:
                print(f"XML data in {filename}:")
                #print(xml_file.read())
                findword1 = False
                findword2 = False
                for line in xml_file.readlines():
                    if findword2:
                        word=remove_tags(line).strip()

                        if word != '':
                            print(word)
                            result.append(word)
                            if len(result)>=3:
                                return result

                        print(word)
                    elif ">현금흐름표<" in line:
                        findword1=True
                        print(line)
                    elif findword1 and "영업활동으로 인한 현금흐름" in line:
                        findword2=True
                        print(line)

                cash_flows =extract_cash_flow_data(xml_file)
                print(cash_flows)
                # XML 데이터에서 현금흐름 데이터 추출
                #cash_flows = extract_cash_flow_data(xml_file.read())
                if cash_flows:
                    print("영업활동으로 인한 현금흐름 데이터:", cash_flows)
                else:
                    print("영업활동으로 인한 현금흐름 데이터를 찾을 수 없습니다.")

    # 파일 삭제
    os.remove('data.zip')
    for filename in os.listdir('extracted_data'):
        os.remove(os.path.join('extracted_data', filename))
    os.rmdir('extracted_data')

# 예시 실행
crtfc_key = '15719e13918826eeafa58e56db3afde7c3418a7d'
rcept_no = '20220513001654'
result=download_and_extract_data(crtfc_key, rcept_no)
print(result)