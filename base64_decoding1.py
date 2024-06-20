import base64
import json


def decode_jwt_header(jwt_token):

    # Base64 URL 디코딩을 위해 패딩 추가
    padded_base64 = jwt_token + '=' * (4 - len(jwt_token) % 4)

    # Base64 URL 디코딩
    header_bytes = base64.urlsafe_b64decode(padded_base64)

    # 바이트를 문자열로 디코딩
    header_str = header_bytes.decode('utf-8')

    # JSON 파싱
    header_json = json.loads(header_str)

    return header_json


# 테스트용 JWT 토큰
jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
header_base64 = jwt_token.split('.')[0]
payload_base64 = jwt_token.split('.')[1]
signature_base64 = jwt_token.split('.')[2]
# JWT 헤더 디코딩
print(decode_jwt_header(header_base64))
print(decode_jwt_header(payload_base64))
#print(decode_jwt_header(signature_base64))

