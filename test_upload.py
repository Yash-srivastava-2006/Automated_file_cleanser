import requests

# Test uploading a file
url = 'http://127.0.0.1:5000/upload'

# Open the test file
with open('test_sensitive_data.txt', 'rb') as f:
    files = {'files[]': f}
    response = requests.post(url, files=files)
    
print("Status Code:", response.status_code)
print("Response:", response.json())