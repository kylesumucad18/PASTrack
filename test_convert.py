import requests
import base64
import os

api_secret = "OoLm1SeWltZvzUzwinJQfl3gyMA6nCAz"
url = f"https://v2.convertapi.com/convert/docx/to/pdf?Secret={api_secret}"

# create a dummy docx file
file_content = b"PK\x03\x04\x14\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0b\x00\x00\x00_rels/.rels"

files = {
    'File': ("test.docx", file_content)
}

response = requests.post(url, files=files)
print("Status:", response.status_code)
print("Response:", response.text)
