import requests
import time

# Test uploading a file
url = 'http://127.0.0.1:5000/upload'

print("Testing file cleansing functionality...")

# Open the test file
with open('test_cleansing_verification.txt', 'rb') as f:
    files = {'files[]': f}
    response = requests.post(url, files=files)
    
print("Upload Status Code:", response.status_code)
if response.status_code == 200:
    data = response.json()
    print("Upload Response:", data)
    
    # Get the cleansed filename
    if 'results' in data and len(data['results']) > 0:
        cleansed_filename = data['results'][0]['cleansed_filename']
        original_filename = data['results'][0]['original_filename']
        print(f"Original filename: {original_filename}")
        print(f"Cleansed filename: {cleansed_filename}")
        
        # Wait a moment for file processing
        time.sleep(1)
        
        # Try to download the cleansed file
        download_url = f'http://127.0.0.1:5000/download/cleansed/{cleansed_filename}'
        download_response = requests.get(download_url)
        
        if download_response.status_code == 200:
            # Save the downloaded file to check its contents
            with open('downloaded_cleansed_file.txt', 'wb') as f:
                f.write(download_response.content)
            
            # Read and display the cleansed content
            with open('downloaded_cleansed_file.txt', 'r', encoding='utf-8') as f:
                cleansed_content = f.read()
                print("\nCleansed Content:")
                print("=" * 50)
                print(cleansed_content)
                print("=" * 50)
                
                # Check if cleansing happened
                if '[EMAIL]' in cleansed_content or '[PHONE]' in cleansed_content or '[SSN]' in cleansed_content:
                    print("\n✅ CLEANSING VERIFICATION: SUCCESS - Sensitive data has been cleansed!")
                else:
                    print("\n❌ CLEANSING VERIFICATION: FAILED - Sensitive data was not cleansed!")
        else:
            print(f"Failed to download cleansed file. Status code: {download_response.status_code}")
    else:
        print("No results found in response")
else:
    print("Upload failed")
    print("Response:", response.text)