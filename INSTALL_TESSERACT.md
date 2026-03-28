# Installing Tesseract OCR on Windows

This guide provides step-by-step instructions for installing Tesseract OCR on Windows to enable image text extraction in the FileClean AI application.

## Prerequisites

- Windows 7 or later (32-bit or 64-bit)
- Administrator privileges for installation

## Installation Steps

### Step 1: Download Tesseract OCR

1. Visit the official Tesseract OCR Windows installer page:
   [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

2. Download the appropriate installer for your system:
   - For 64-bit systems: `tesseract-ocr-w64-setup-vX.X.X.X.exe`
   - For 32-bit systems: `tesseract-ocr-w32-setup-vX.X.X.X.exe`

### Step 2: Run the Installer

1. Locate the downloaded installer file
2. Right-click on the file and select "Run as administrator"
3. Follow the installation wizard:
   - **Welcome**: Click "Next"
   - **License Agreement**: Accept the license and click "Next"
   - **Select Components**: 
     - Check "Additional language data" if you need languages other than English
     - **Important**: Check "Add to PATH" - This is crucial for the application to find Tesseract
   - **Destination Folder**: 
     - Default is `C:\Program Files\Tesseract-OCR\` (recommended)
     - Click "Next"
   - **Ready to Install**: Click "Install"
   - **Completing**: Click "Finish"

### Step 3: Verify Installation

1. Open a **new** Command Prompt or PowerShell window (must be new after installation)
2. Run the following command:
   ```
   tesseract --version
   ```
3. You should see output similar to:
   ```
   tesseract v5.3.0.20221222
    leptonica-1.82.0
     libgif 5.2.1 : libjpeg 9e : libpng 1.6.39 : libtiff 4.4.0 : zlib 1.2.13 : libwebp 1.2.4 : libopenjp2 2.5.0
    ...
   ```

### Step 4: Restart the Application

1. If the Flask application is running, stop it (Ctrl+C)
2. Start the application again:
   ```
   python app.py
   ```

## Troubleshooting

### Issue: "tesseract is not recognized as an internal or external command"

This means Tesseract was not added to your system PATH during installation:

**Solution 1: Reinstall with PATH option**
1. Uninstall Tesseract from "Add or Remove Programs"
2. Reinstall and make sure to check "Add to PATH" during installation

**Solution 2: Manually add to PATH**
1. Find your Tesseract installation directory (usually `C:\Program Files\Tesseract-OCR\`)
2. Add this directory to your system PATH:
   - Press Win + X and select "System"
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System Variables", find and select "Path", then click "Edit"
   - Click "New" and add the Tesseract directory path
   - Click "OK" to save changes
3. Restart your command prompt and test again

### Issue: Application still shows "OCR Not Available"

**Solution:**
1. Make sure you've restarted the Flask application after installing Tesseract
2. Check that the path in [app.py](file:///C:/Users/Anmol's%20ThinkPad/Desktop/optive/app.py) matches your Tesseract installation directory
3. Run the check_tesseract.py script to verify:
   ```
   python check_tesseract.py
   ```

### Issue: Permission denied or access issues

**Solution:**
Run your command prompt or PowerShell as Administrator when starting the Flask application.

## Testing OCR Functionality

After successful installation:

1. Use the test image we created ([test_ocr.png](file:///C:/Users/Anmol's%20ThinkPad/Desktop/optive/test_ocr.png)) or create your own image with text
2. Upload the image through the web interface
3. The application should now be able to extract text from images

## Additional Language Support

By default, Tesseract includes English language support. To add support for other languages:

1. During installation, select additional languages in the "Additional language data" section
2. Or download language data files separately:
   - Visit [Tesseract language data repository](https://github.com/tesseract-ocr/tessdata)
   - Download the `.traineddata` file for your language (e.g., `spa.traineddata` for Spanish)
   - Place it in the `tessdata` folder in your Tesseract installation directory (usually `C:\Program Files\Tesseract-OCR\tessdata\`)
   - Use it in code: `pytesseract.image_to_string(image, lang='spa')`

## Support

If you continue to have issues:

1. Check the [Tesseract documentation](https://tesseract-ocr.github.io/)
2. Review the [Tesseract GitHub issues](https://github.com/tesseract-ocr/tesseract/issues)
3. Restart your computer and try again