# Gemini AI Integration Setup Guide

This guide will help you set up the Gemini AI integration for enhanced file analysis in the File Cleansing and Analysis system.

## Prerequisites

1. **Google AI API Key**: You need a Google AI Studio API key to use Gemini AI
2. **Python Dependencies**: The required Python packages are already included in the requirements.txt file

## Step 1: Get a Google AI API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new API key:
   - Click on "Get API key" or navigate to the API keys section
   - Create a new API key
   - Copy the API key and save it securely

## Step 2: Set Environment Variable

Set the `GEMINI_API_KEY` environment variable with your API key:

### On Windows (Command Prompt):
```cmd
set GEMINI_API_KEY=your_actual_api_key_here
```

### On Windows (PowerShell):
```powershell
$env:GEMINI_API_KEY="your_actual_api_key_here"
```

### On macOS/Linux:
```bash
export GEMINI_API_KEY=your_actual_api_key_here
```

## Step 3: Install Dependencies

Make sure all required dependencies are installed:
```bash
pip install -r requirements.txt
```

This will install the `google-generativeai` package along with all other required packages.

## Step 4: Restart the Application

After setting the environment variable, restart the Flask application:
```bash
python app.py
```

## Using Gemini AI Analysis

Once the application is running with the API key set:

1. Upload files through the web interface
2. After cleansing, you'll see a "Gemini AI Analysis" button next to each file
3. Click this button to perform AI-powered analysis of the cleansed content
4. The analysis results will include:
   - Document overview and summary
   - Key insights and findings
   - Potential use cases
   - Recommendations

## Troubleshooting

### "Gemini AI analyzer not available" Error
- Make sure you've installed all dependencies with `pip install -r requirements.txt`
- Verify the `google-generativeai` package is installed: `pip show google-generativeai`

### "GEMINI_API_KEY environment variable not set" Error
- Double-check that you've correctly set the environment variable
- On Windows, you can verify with:
  ```cmd
  echo %GEMINI_API_KEY%
  ```
- On macOS/Linux, you can verify with:
  ```bash
  echo $GEMINI_API_KEY
  ```

### "API_KEY_INVALID" Error
- Verify that your API key is correct and hasn't expired
- Check that you've copied the entire key without any extra spaces

## Features of Gemini AI Analysis

The Gemini AI integration provides:

1. **Document Overview**: Understanding of document type, purpose, and main topics
2. **Content Summarization**: Concise summary of key points
3. **Insight Extraction**: Identification of important patterns and findings
4. **Use Case Analysis**: Suggestions for how the document might be applied
5. **Recommendations**: Actionable suggestions based on the content

This AI-powered analysis complements the existing security-focused analysis with broader insights and understanding of the document content.