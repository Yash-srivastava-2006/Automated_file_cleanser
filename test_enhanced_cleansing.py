import requests
import time
import os

def test_enhanced_cleansing():
    """Test enhanced cleansing functionality with various file types"""
    
    print("Testing enhanced file cleansing functionality...")
    
    # Create test files with sensitive data
    test_files = {
        'test_client_data.txt': '''CONFIDENTIAL - CLIENT DOCUMENT

Client Information:
- Client Name: Acme Corporation
- Contact: John Smith (john.smith@acmecorp.com)
- Phone: 555-123-4567
- SSN: 123-45-6789

Technical Details:
- Server IP: 192.168.1.100
- MAC: 00:1A:2B:3C:4D:5E
- Policy: Complex passwords required (min 12 chars)
- Rule: Allow HTTPS from 10.0.0.0/8

Personal Data:
- Address: 123 Main Street, Anytown, CA 90210
- Passport: P12345678
- Driver License: CA123456789

This document contains confidential information about Acme Corporation.
''',
        
        'global_tech.pdf': '''CONFIDENTIAL - GLOBAL TECH SOLUTIONS

Client Contact:
- Name: Jane Doe
- Email: jane.doe@globaltech.com
- Phone: 555-987-6543
- SSN: 987-65-4321

Network Information:
- Internal IP: 10.0.0.25
- MAC Address: AA:BB:CC:DD:EE:FF
- Password Policy: Minimum 16 characters
- Firewall Rule: Deny SSH from external networks

Personal Information:
- Home Address: 456 Oak Avenue, Springfield, IL 62701
- Passport Number: G98765432
- License: IL123456789

This document is for Global Tech Solutions only.
'''
    }
    
    # Create test files
    for filename, content in test_files.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created test file: {filename}")
    
    # Test uploading each file
    for filename in test_files.keys():
        print(f"\nTesting cleansing for: {filename}")
        
        # Upload the file
        url = 'http://127.0.0.1:5000/upload'
        with open(filename, 'rb') as f:
            files = {'files[]': f}
            response = requests.post(url, files=files)
        
        print(f"Upload Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                cleansed_filename = data['results'][0]['cleansed_filename']
                print(f"Cleansed filename: {cleansed_filename}")
                
                # Wait a moment for file processing
                time.sleep(1)
                
                # Download the cleansed file
                download_url = f'http://127.0.0.1:5000/download/cleansed/{cleansed_filename}'
                download_response = requests.get(download_url)
                
                if download_response.status_code == 200:
                    # Save and analyze the cleansed content
                    cleansed_file_path = f'cleansed_{filename}'
                    with open(cleansed_file_path, 'wb') as f:
                        f.write(download_response.content)
                    
                    # For text files, read and display content
                    if filename.endswith('.txt'):
                        with open(cleansed_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            cleansed_content = f.read()
                        
                        print("Cleansed Content Preview:")
                        print("=" * 40)
                        print(cleansed_content[:500] + ("..." if len(cleansed_content) > 500 else ""))
                        print("=" * 40)
                        
                        # Check if cleansing happened
                        checks = {
                            'Email': '[EMAIL]' in cleansed_content,
                            'Phone': '[PHONE]' in cleansed_content,
                            'SSN': '[SSN]' in cleansed_content,
                            'IP': '[IP ADDRESS]' in cleansed_content,
                            'MAC': '[MAC ADDRESS]' in cleansed_content,
                            'Client Name': '[CLIENT NAME]' in cleansed_content or '[CLIENT TERM]' in cleansed_content,
                            'Passport': '[PASSPORT]' in cleansed_content,
                            'Address': '[ADDRESS]' in cleansed_content
                        }
                        
                        print("Cleansing Verification:")
                        all_passed = True
                        for check_name, result in checks.items():
                            status = "✅ PASS" if result else "❌ FAIL"
                            print(f"  {check_name}: {status}")
                            if not result:
                                all_passed = False
                        
                        if all_passed:
                            print("🎉 ALL CLEANSING TESTS PASSED!")
                        else:
                            print("⚠️  Some cleansing tests failed - check implementation")
                        
                else:
                    print(f"Failed to download cleansed file. Status code: {download_response.status_code}")
            else:
                print("No results found in response")
        else:
            print(f"Upload failed for {filename}")
            print("Response:", response.text)
    
    print("\nEnhanced cleansing test completed!")

if __name__ == "__main__":
    test_enhanced_cleansing()