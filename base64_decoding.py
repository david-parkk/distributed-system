#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9

import base64
import json

str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'

padded_base64 = str + '=' * (4 - len(str) % 4)
print(padded_base64)
result = base64.urlsafe_b64decode(padded_base64)
result_str = result.decode('utf-8')

print(result_str)