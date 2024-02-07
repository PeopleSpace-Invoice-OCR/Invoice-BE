# Invoice-BE
---
## Code Description - FrontEnd
[FrontEnd README](https://github.com/PeopleSpace-Invoice-OCR/Invoice-FE/blob/main/README.md)

## Code Description - BackEnd
#### 1. api.py

#### 2. invoiceOcr.py
1. **OCR Text Extraction**
   - Utilize Google Cloud Vision API to extract text from images.
   - OCR technology recognizes text within the image and converts it to character data.

2. **Information Extraction via OpenAI API**
   - Write prompts for the OpenAI API based on the text obtained from OCR results.
   - Example prompt: "Please find the company name, address, telephone number, order number, order date, and total amount in the following text."

3. **OpenAI API Call**
   - Invoke the OpenAI API using Python code and send the written prompts.
   - Extract the required information from the API response.

4. **Mapping Extracted Information to JSON**
   - Analyze the response received from the API to identify necessary information.
   - Map identified information to a predefined JSON structure.


## Overview
<img width="754" alt="image" src="https://github.com/PeopleSpace-Invoice-OCR/Invoice-BE/assets/85086390/3c1f7428-d491-4f1a-894f-4050373ad01b">

#### 1. Photo Capture: User photographs the invoice.
#### 2. OCR Text Extraction: Google Cloud Vision API extracts text from the image.
#### 3. OpenAI API Query: Call the OpenAI API with prompts to extract specific information.
#### 4. Data Extraction: Retrieve necessary information from the API response.
#### 5. JSON Mapping: Map extracted data into a predefined JSON structure.
#### 6. User Verification: User reviews the mapped data.
#### 7. Data Save: User clicks 'save', and the information is stored in the ERPNext system.
#### 8. Feedback Loop: Continuous feedback and updates through GitHub.
