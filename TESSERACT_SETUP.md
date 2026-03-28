# Tesseract OCR Installation Guide for Windows

This guide will help you install and configure Tesseract OCR on Windows to enable image text extraction in the FileClean AI application.

## Step 1: Download Tesseract OCR

1. Visit the official Tesseract OCR Windows installer page:
   [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

2. Download the latest version of the installer for your system architecture (32-bit or 64-bit)

## Step 2: Install Tesseract OCR

1. Run the downloaded installer as Administrator
2. During installation, make sure to select the option:
   **"Add Tesseract to PATH"** - This is crucial for the application to find Tesseract
3. Choose the installation directory (default is usually fine):
   `C:\Program Files\Tesseract-OCR\`
4. Complete the installation process

## Step 3: Verify Installation

1. Open a new Command Prompt or PowerShell window (important: must be new after installation)
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

## Step 4: Configure the Application

The application is already configured to look for Tesseract at the default installation path:
```
C:\Program Files\Tesseract-OCR\tesseract.exe
```

If your installation is in a different location, you'll need to update the path in [app.py](file:///C:/Users/Anmol's%20ThinkPad/Desktop/optive/app.py):
```python
pytesseract.pytesseract.tesseract_cmd = r'YOUR_TESSERACT_PATH_HERE'
```

## Step 5: Test OCR Functionality

1. Restart the Flask application:
   ```
   python app.py
   ```

2. Upload an image file (PNG, JPG, JPEG) through the web interface
3. The application should now be able to extract text from images

## Troubleshooting

### Issue: "tesseract is not recognized as an internal or external command"

This means Tesseract was not added to your system PATH during installation:

1. Find your Tesseract installation directory (usually `C:\Program Files\Tesseract-OCR\`)
2. Add this directory to your system PATH:
   - Press Win + X and select "System"
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System Variables", find and select "Path", then click "Edit"
   - Click "New" and add the Tesseract directory path
   - Click "OK" to save changes
3. Restart your command prompt and test again

### Issue: Permission denied or access issues

Run your command prompt or PowerShell as Administrator when starting the Flask application.

### Issue: Still not working in the application

1. Make sure you've restarted the Flask application after installing Tesseract
2. Check that the path in [app.py](file:///C:/Users/Anmol's%20ThinkPad/Desktop/optive/app.py) matches your Tesseract installation directory
3. Test Tesseract directly from the command line:
   ```
   tesseract test_ocr.png output
   ```

## Additional Language Support

By default, Tesseract includes English language support. To add support for other languages:

1. During installation, select additional languages
2. Or download language data files separately and place them in the `tessdata` folder in your Tesseract installation directory

For example, to add Spanish language support:
- Download `spa.traineddata` from the [Tesseract language data repository](https://github.com/tesseract-ocr/tessdata)
- Place it in `C:\Program Files\Tesseract-OCR\tessdata\`
- Use it in your code: `pytesseract.image_to_string(image, lang='spa')`