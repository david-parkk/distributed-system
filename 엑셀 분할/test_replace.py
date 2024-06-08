import re


def parse_numbers(text):
    # 괄호 안에 숫자가 있는 경우 음수로 처리
    match = re.search(r'\(?-?[\d,]+\)?', text)
    if match:
        # 매칭된 문자열을 가져옴
        number = match.group()

        # 괄호가 있으면 음수로 처리
        is_negative = False
        if number.startswith('(') and number.endswith(')'):
            is_negative = True
            number = number[1:-1]  # 괄호 제거

        # 쉼표 제거
        number = number.replace(',', '')

        # 정수로 변환
        number = int(number)

        # 음수 처리
        if is_negative:
            number = -number

        return number

print(parse_numbers("(1123,12312)"))