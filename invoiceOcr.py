from google.cloud import vision
import os
import io
import json
from openai import OpenAI
import re
import sys

# Service Account Key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './loyal-coast-412223-091bd2dc7f2a.json'

client = vision.ImageAnnotatorClient()

file_path = sys.argv[1]

# Read with Image File Bytes
with io.open(file_path, 'rb') as image_file:
    content = image_file.read()

# Use the Vision API feature (create a class instance)
image = vision.Image(content=content)

# Document text detection and extraction
response = client.document_text_detection(image=image)

texts = response.text_annotations[0].description if response.text_annotations else ""


# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

api_key = 'your api key'

client = OpenAI(api_key=api_key)

prompt = f"""Extract important information from the following document and organize the data into the specified JSON format:
Document:
{texts}

Return the information in JSON format with the following structure: owner, customer, po_no, po_date, company_address, customer_address, shipping_address_name, grand_total, items (including item_name, description, qty, rate, amount, income_account), and taxes (including charge_type, account_head, description, tax_amount).
"""

# Choose the information you need using the OpenAI API and map it to the existing json format
response = client.completions.create(
    model="gpt-3.5-turbo-instruct",  
    prompt=prompt,
    max_tokens=1000,
    temperature=0.3
)

# text obtained
response_text = response.choices[0].text.strip()

# Extract information, put "" if no matching information is found
def extract_with_default(pattern, text, default=""):
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return default

try:
    # Dynamic value assignment (this is how openAI mapped... results are dynamically entered)
    structured_response = json.loads(response.choices[0].text.strip())
    
except json.JSONDecodeError:
    print("Failed to decode the response into JSON")
    data_to_json = {}

# result
print(json.dumps(structured_response, indent=4))

