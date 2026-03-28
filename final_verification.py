import requests
import time
import os

def final_verification_test():
    """Final verification test to confirm all enhancements are working"""
    
    print("🚀 FINAL VERIFICATION TEST")
    print("=" * 50)
    
    # Create a comprehensive test file
    test_content = '''CONFIDENTIAL DOCUMENT - ACME CORPORATION

CLIENT INFORMATION:
- Client Name: Acme Corporation
- Contact Person: John Smith
- Email: john.smith@acmecorp.com
- Phone: 555-123-4567
- SSN: 123-45-6789

TECHNICAL DETAILS:
- Server IP Address: 192.168.1.100
- MAC Address: 00:1A:2B:3C:4D:5E
- Password Policy: Minimum 12 characters with special chars
- Firewall Rule: Allow TCP 443 from 10.0.0.0/8

PERSONAL INFORMATION:
- Home Address: 123 Main Street, Anytown, CA 90210
- Passport Number: P12345678
- Driver License: CA123456789
- Birth Date: 12/25/1980

NETWORK CONFIGURATION:
- Internal IP: 10.0.0.25
- External IP: 203.0.113.45
- Subnet Mask: 255.255.255.0

This document contains confidential information about Acme Corporation.
Company Confidential - Do Not Distribute
'''

    # Create test file
    test_filename = 'comprehensive_test.txt'
    with open(test_filename, 'w', encoding='utf-8') as f:
        f.write(test_content)
    print(f"✅ Created comprehensive test file: {test_filename}")
    
    # Upload the file
    print("\n📤 Uploading test file...")
    url = 'http://127.0.0.1:5000/upload'
    with open(test_filename, 'rb') as f:
        files = {'files[]': f}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        print("✅ Upload successful")
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            cleansed_filename = data['results'][0]['cleansed_filename']
            print(f"📄 Cleansed filename: {cleansed_filename}")
            
            # Wait for processing
            time.sleep(1)
            
            # Download the cleansed file
            print("\n📥 Downloading cleansed file...")
            download_url = f'http://127.0.0.1:5000/download/cleansed/{cleansed_filename}'
            download_response = requests.get(download_url)
            
            if download_response.status_code == 200:
                # Save the cleansed content
                cleansed_file_path = 'final_cleansed_result.txt'
                with open(cleansed_file_path, 'wb') as f:
                    f.write(download_response.content)
                
                # Read and analyze the result
                with open(cleansed_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    cleansed_content = f.read()
                
                print("\n🔍 CLEANSING RESULTS:")
                print("=" * 30)
                print(cleansed_content)
                print("=" * 30)
                
                # Verification checks
                print("\n✅ VERIFICATION RESULTS:")
                print("=" * 25)
                
                checks = {
                    'Email Addresses': '[EMAIL]' in cleansed_content,
                    'Phone Numbers': '[PHONE]' in cleansed_content,
                    'SSNs': '[SSN]' in cleansed_content,
                    'IP Addresses': '[IP ADDRESS]' in cleansed_content,
                    'MAC Addresses': '[MAC ADDRESS]' in cleansed_content,
                    'Client Names': '[CLIENT NAME]' in cleansed_content or '[CLIENT TERM]' in cleansed_content,
                    'Passport Numbers': '[PASSPORT]' in cleansed_content,
                    'Driver Licenses': '[DRIVER LICENSE]' in cleansed_content,
                    'Addresses': '[ADDRESS]' in cleansed_content,
                    'Dates': '[DATE]' in cleansed_content
                }
                
                all_passed = True
                for check_name, result in checks.items():
                    status = "✅ PASS" if result else "❌ FAIL"
                    print(f"  {check_name:<20}: {status}")
                    if not result:
                        all_passed = False
                
                print("\n" + "=" * 25)
                if all_passed:
                    print("🎉 ALL TESTS PASSED! File cleansing is working correctly.")
                    print("✨ Sensitive data has been successfully removed while preserving format.")
                else:
                    print("⚠️  Some tests failed. Review the implementation.")
                
                # Test analysis functionality
                print("\n📊 Testing analysis functionality...")
                analyze_url = f'http://127.0.0.1:5000/analyze/{cleansed_filename}'
                analyze_response = requests.get(analyze_url)
                
                if analyze_response.status_code == 200:
                    analyze_data = analyze_response.json()
                    if analyze_data.get('success'):
                        print("✅ Analysis completed successfully!")
                        print(f"📄 Analyzed file: {analyze_data.get('analyzed_filename')}")
                    else:
                        print("❌ Analysis failed")
                else:
                    print(f"❌ Analysis request failed with status {analyze_response.status_code}")
                
            else:
                print(f"❌ Failed to download cleansed file (Status: {download_response.status_code})")
        else:
            print("❌ No results in upload response")
    else:
        print(f"❌ Upload failed (Status: {response.status_code})")
        print("Response:", response.text)
    
    print("\n🏁 VERIFICATION COMPLETE")

if __name__ == "__main__":
    final_verification_test()