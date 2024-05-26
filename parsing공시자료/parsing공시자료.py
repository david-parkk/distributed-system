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




    return third_child,fifth_child,seventh_child
def remove_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
def parse_numbers(text):
    # 숫자 형식을 찾기 (숫자 형식과 쉼표 포함)
    match = re.search(r'-?[\d,]+', text)
    if match:
        # 쉼표 제거하고 정수로 변환
        number = match.group().replace(',', '')
        # 정수로 변환
        number = int(number)
        return number
    return None
def download_and_extract_data(crtfc_key, rcept_no):

        url = f"https://opendart.fss.or.kr/api/document.xml?crtfc_key={crtfc_key}&rcept_no={rcept_no}"
        result=[]
        # GET 요청 보내기
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            return "fail"
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
                with open(os.path.join('extracted_data', filename), 'rt', encoding='UTF8') as xml_file:
                #with open(os.path.join('extracted_data', filename), 'r') as xml_file:

                    print(f"XML data in {filename}:")

                    # print(xml_file.read())
                    # print("경계선")
                    findword1 = False
                    findword2 = False

                    for line in xml_file.readlines():

                        if line.strip() == '':
                            continue
                        #print(line)


                        if findword2:
                            try:
                                #print("line =",line)
                                word = remove_tags(line).strip()

                                number = parse_numbers(word)

                                if number is not None:
                                    # 음수 값을 붙여야 하는 경우
                                    if ',' in word and word.count(',') >= 2:  # 예: 7,955,894,919
                                        number = -number

                                    result.append(number)

                                    if len(result) >= 3:
                                        return result
                            except Exception as e:
                                continue

                            #print(word)
                        #elif "연결 현금흐름표" in line:
                            #print("찾음")
                            #findword1 = False
                        if ("현금흐름표<" or "연결 현금흐름표<" in line) and findword1==False :
                            findword1=True


                        elif findword1 and ("영업활동현금흐름" in line or "영업활동으로 인한 현금흐름" in line) and len(line)<30:
                            findword2=True
                            # print("zzzzzz")
                            # print(line)
                            #print(line)
                        # print(findword1)
                        # print("영업활동현금흐름" in line or "영업활동으로 인한 현금흐름" in line)
                        # print(findword1 and ("영업활동현금흐름" in line or "영업활동으로 인한 현금흐름" in line))
                        # print(findword2)
                    return "fail"

        # 파일 삭제
        os.remove('data.zip')
        for filename in os.listdir('extracted_data'):
            os.remove(os.path.join('extracted_data', filename))
        os.rmdir('extracted_data')
    # except Exception as e:
    #     try:
    #         os.remove('data.zip')
    #         for filename in os.listdir('extracted_data'):
    #             os.remove(os.path.join('extracted_data', filename))
    #         os.rmdir('extracted_data')
    #         return "fail";
    #     except Exception as e:
    #         return "fail"


# 예시 실행
crtfc_key = '15719e13918826eeafa58e56db3afde7c3418a7d'
#rcept_no='20230530000651'
rcept_no = '20230428000506'
result=download_and_extract_data(crtfc_key, rcept_no)
print(result)
