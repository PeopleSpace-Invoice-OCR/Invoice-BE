from google.cloud import vision
import os
import io
import json
from openai import OpenAI
import re
import sys

# 서비스 계정 키
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './loyal-coast-412223-091bd2dc7f2a.json'

client = vision.ImageAnnotatorClient()

file_path = sys.argv[1]

# 이미지 파일 바이트로 읽기
with io.open(file_path, 'rb') as image_file:
    content = image_file.read()

# Vision API 기능 사용 (class instance 생성)    
image = vision.Image(content=content)

# 문서 텍스트 감지 + 추출
response = client.document_text_detection(image=image)
# texts = response.text_annotations
texts = response.text_annotations[0].description if response.text_annotations else ""
# print(texts)

# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

api_key = 'your api key'

client = OpenAI(api_key=api_key)

prompt = f"""Extract important information from the following document and organize the data into the specified JSON format:
Document:
{texts}

Return the information in JSON format with the following structure: owner, customer, po_no, po_date, company_address, customer_address, shipping_address_name, grand_total, items (including item_name, description, qty, rate, amount, income_account), and taxes (including charge_type, account_head, description, tax_amount).
"""

# OpenAI API 써서 필요한 정보 고르고, 기존에 정한 json 형식이랑 매핑
response = client.completions.create(
    model="gpt-3.5-turbo-instruct",  
    prompt=prompt,
    max_tokens=1000,
    temperature=0.3
)

# 얻은 텍스트
response_text = response.choices[0].text.strip()

# 정보를 추출하고, 일치하는 정보가 없으면 "" 넣음
def extract_with_default(pattern, text, default=""):
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return default

try:
    # 동적으로 값 할당 (이래야 openAI가 매핑한 ... 결과가 동적으로 들어감)
    structured_response = json.loads(response.choices[0].text.strip())
    # data_to_json = {"data": structured_response}
except json.JSONDecodeError:
    print("Failed to decode the response into JSON")
    data_to_json = {}

# 결과 출력
print(json.dumps(structured_response, indent=4))

