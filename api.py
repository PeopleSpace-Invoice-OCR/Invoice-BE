from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
import requests
import json
import subprocess
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Cookie
import os

app = FastAPI()
base_url = "http://development.localhost:8000" #http://172.27.44.122/  -> docker ip mapping file: "C:\Windows\System32\drivers\etc\hosts"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)


@app.options("/api/login")
def options_login():
    return {"Allow": "POST"}

@app.post("/api/login") #login   
def login(login_data: dict):  
    
    url = f"{base_url}/api/method/login"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "usr": login_data['email'], 
        "pwd": login_data['password'] 
    }

    # Make a POST request to the login endpoint
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful (status code 2xx)
    if response.status_code // 100 == 2:

        # Get cookies
        cookies_from_response = response.cookies

        return JSONResponse(content={"cookies": cookies_from_response.get_dict(), "data": response.json()}, status_code=200)
    else:
        # Raise an HTTPException with the details of the error
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.post("/api/invoice") # invoice extract
async def invoice(file: UploadFile = File(...)):
    try:
        
        # Save the uploaded file
        file_path = os.path.abspath(file.filename)
        with open(file.filename, "wb") as f:
            f.write(file.file.read())

        # Run ocr_module.py using subprocess with absolute file path
        ocr_module_path = os.path.join(os.path.dirname(__file__), "invoiceOcr.py")
        result = subprocess.check_output(["python", ocr_module_path, file_path])
        print("result: ", result)

        # Find the starting point of the JSON string
        start_index = result.find(b'{')

        # Extract the JSON string from the starting point
        json_str = result[start_index:]

        # Parse the result as JSON
        result_json = json.loads(json_str.decode('utf-8'))

        return JSONResponse(content=result_json, status_code=200)

    except Exception as e:
        # Output tracking information for exceptions to get more details.
        import traceback
        traceback.print_exc()

        # Returns HTTP 500 responses with error details
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)