# Optive: AI-Powered File Cleansing and Analysis

## Overview
Optive is a multi-format document cleansing and analysis system designed to:

- Accept mixed enterprise files (PDF, image, PPTX, XLSX, TXT)
- Extract text from each file type using the right parser/OCR stack
- Detect and mask PII before downstream interpretation
- Produce structured JSON summaries with human-readable key findings
- Expose everything through an interactive Streamlit report UI

The repository currently contains two app layers:

- Streamlit app: end-to-end upload, cleanse, analyze, and report workflow
- Flask app: legacy interface and earlier modules retained for compatibility

## What Is Used in the Project

### Core languages and framework
- Python 3.11+ (tested with Python 3.13 in this workspace)
- Streamlit for the primary UI and report layer
- Flask for legacy app routes

### Parsing and extraction stack
- pytesseract for OCR on images
- pdfplumber for primary PDF text extraction
- PyMuPDF as fallback PDF extractor and PDF redaction handler
- python-pptx for slide/table extraction and masking
- pandas plus openpyxl for Excel extraction and rewrite

### PII and NLP stack
- spaCy NER model target: en_core_web_trf
- spaCy fallback model: en_core_web_sm
- Regex-based detectors for email, phone, Aadhaar, SSN

### Image masking stack
- OpenCV for image operations and blur/blackout
- YOLOv8 face detector via ultralytics (local weight file: yolov8n-face.pt)

### Other important libraries
- PyPDF2
- presidio-analyzer and presidio-anonymizer (legacy components in repo)
- google-generativeai (optional, legacy analysis path)

## Repository Structure

- app.py: legacy Flask application
- streamlit_app.py: primary Streamlit UI entrypoint
- ai_pipeline.py: main extraction, PII, masking, findings, and JSON logic
- comprehensive_cleanser.py: previous hybrid redactor implementation
- gemini_analyzer.py: optional Gemini analysis module
- requirements.txt: Python dependencies
- uploads/: incoming files (created/used at runtime)
- outputs/masked/: masked output files
- outputs/raw_text/: raw extracted text
- outputs/clean_text/: masked cleaned text
- outputs/json/: structured report JSON outputs
- processed/ and cleansed/: legacy artifact folders used by older flows

## Supported File Types

Input upload types:
- PDF (.pdf)
- Images (.png, .jpg, .jpeg)
- PowerPoint (.pptx)
- Excel (.xlsx)
- Text (.txt)

## Model Details

### 1) Named Entity Recognition (NER)
- Primary: en_core_web_trf
- Fallback order in code:
  1. en_core_web_trf
  2. en_core_web_sm
  3. spacy.blank("en") for regex-only operation

Why fallback exists:
- On some Windows/Python combinations (especially Python 3.13), en_core_web_trf may fail to install because native build tooling is required for a dependency wheel.

### 2) Face Detection for image redaction
- YOLOv8 face model expected as local file: yolov8n-face.pt
- If file is missing, the pipeline skips face blurring safely and still performs OCR-based text masking.

## End-to-End Workflow

### Step 1: Upload
User uploads one or more supported files from Streamlit UI.

### Step 2: Type detection
The pipeline detects file type from extension.

### Step 3: Text extraction
- Image: OCR via pytesseract
- PDF: pdfplumber first, then PyMuPDF fallback
- PPTX: iterate slide shapes and table cells
- XLSX: read all sheets and stringify cells
- TXT: plain text read

### Step 4: Normalization
Text is standardized by:
- normalizing line breaks
- collapsing extra spaces/tabs
- reducing repeated blank lines

### Step 5: PII detection
Two combined channels:
- NER (PERSON entities from spaCy model)
- Regex (EMAIL, PHONE, AADHAAR, SSN)

Deduplication is applied to overlapping entities.

### Step 6: Masking
- Text masking tags used: [REDACTED_NAME], [REDACTED_EMAIL], [REDACTED_PHONE], [REDACTED_ID]
- File-type specific masking:
  - Image: blur faces (if YOLO model exists) and blackout OCR PII regions
  - PDF: redact found entity text via redaction annotations
  - PPTX/XLSX: replace PII text in content and write masked copies
  - TXT: save masked text copy

### Step 7: Intermediate artifacts
Generated for each file:
- Raw text file
- Cleaned (masked) text file
- Masked file artifact

### Step 8: Insights and findings
After masking, rule-based interpretation plus text heuristics produce 3 to 5 findings.

### Step 9: Structured output
A JSON object is generated per file:
- file_name
- file_type
- file_description
- key_findings

### Step 10: Report UI and downloads
Streamlit displays:
- structured report table (one row per file)
- bullet-point key findings
- masked preview
- detected entities
- intermediate raw and cleaned text
- per-file and full-report JSON downloads

## Architecture

### High-level architecture (component view)

Client Browser
  -> Streamlit UI (streamlit_app.py)
    -> Pipeline Orchestrator (FileCleansingPipeline in ai_pipeline.py)
      -> Extraction Layer
        -> OCR: pytesseract
        -> PDF: pdfplumber / PyMuPDF
        -> PPTX: python-pptx
        -> XLSX: pandas/openpyxl
      -> Detection Layer
        -> spaCy NER (trf/sm/blank fallback)
        -> Regex detectors
      -> Masking Layer
        -> Text masking tags
        -> OpenCV + YOLOv8 face blur
        -> PDF/PPTX/XLSX/TXT masked rewrites
      -> Insight Layer
        -> Description generator
        -> Rule-based key findings
      -> Output Layer
        -> outputs/raw_text
        -> outputs/clean_text
        -> outputs/masked
        -> outputs/json

### Data flow
1. Upload file
2. Extract text
3. Normalize text
4. Detect PII
5. Mask text and files
6. Generate findings from masked text
7. Persist artifacts and JSON
8. Render report and download options

## How to Run the Repository

## 1) Prerequisites

Install system dependencies:
- Python 3.11+ (3.13 works, but en_core_web_trf may need extra build tools)
- Tesseract OCR installed and available in PATH

Windows quick check:
- Run: tesseract --version

If command is missing, install Tesseract and restart terminal.

## 2) Create and use virtual environment

From repository parent folder:

Windows PowerShell:
- cd C:/Users/HARSH/Downloads/optive
- python -m venv .venv
- ./.venv/Scripts/Activate.ps1

If script execution is blocked:
- Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
- ./.venv/Scripts/Activate.ps1

## 3) Install dependencies

From project folder:
- cd C:/Users/HARSH/Downloads/optive/optive
- C:/Users/HARSH/Downloads/optive/.venv/Scripts/python.exe -m pip install -r requirements.txt

## 4) Install spaCy model

Preferred model:
- C:/Users/HARSH/Downloads/optive/.venv/Scripts/python.exe -m spacy download en_core_web_trf

If this fails on Windows (common with Python 3.13 toolchain constraints):
- C:/Users/HARSH/Downloads/optive/.venv/Scripts/python.exe -m spacy download en_core_web_sm

The pipeline will automatically fallback.

## 5) Optional: enable YOLO face blur

Place file in project root:
- yolov8n-face.pt

Expected location:
- C:/Users/HARSH/Downloads/optive/optive/yolov8n-face.pt

Without this file, face blur is skipped gracefully.

## 6) Run Streamlit app (recommended)

- cd C:/Users/HARSH/Downloads/optive/optive
- C:/Users/HARSH/Downloads/optive/.venv/Scripts/python.exe -m streamlit run streamlit_app.py

Open URL printed in terminal (usually http://localhost:8501).

## 7) Run Flask app (legacy)

- cd C:/Users/HARSH/Downloads/optive/optive
- C:/Users/HARSH/Downloads/optive/.venv/Scripts/python.exe app.py

Open http://127.0.0.1:5000.

## Output Artifacts and Report Downloads

For each processed input, the system writes:
- Masked file: outputs/masked
- Raw extracted text: outputs/raw_text
- Clean masked text: outputs/clean_text
- Structured JSON: outputs/json

Streamlit adds:
- Download full structured report as JSON
- Download each file report as JSON
- Download masked file artifact

## Security and Privacy Notes

- PII masking is deterministic based on NER plus regex patterns.
- Findings are generated only after masking, reducing sensitive leakage risk.
- Files are persisted locally in workspace folders; secure file-system access is recommended for production.
- This project is not a certified compliance product; validate patterns and controls for your regulatory environment.

## Troubleshooting

### Problem: No module named streamlit
Cause:
- Running system Python instead of project venv.

Fix:
- Use explicit interpreter:
  - C:/Users/HARSH/Downloads/optive/.venv/Scripts/python.exe -m streamlit run streamlit_app.py

### Problem: en_core_web_trf install fails
Cause:
- Missing Microsoft C++ Build Tools or wheel build constraints.

Fix:
- Install fallback model:
  - python -m spacy download en_core_web_sm
- Continue; pipeline fallback logic already handles this.

### Problem: OCR not detecting text
Checks:
- Verify Tesseract install: tesseract --version
- Ensure image quality/resolution is adequate
- Confirm pytesseract can access executable in PATH

### Problem: Face blur not happening
Cause:
- yolov8n-face.pt not present in project root.

Fix:
- Add the weights file at project root location.

### Problem: Streamlit exits immediately
Checks:
- Run from correct folder: C:/Users/HARSH/Downloads/optive/optive
- Run with venv Python path
- Confirm dependencies installed from requirements.txt

## Extending the Project

Recommended improvements:
- Add unit and integration tests for each extractor and masker
- Add async/batch job queue for large file sets
- Add object storage integration for production deployments
- Add authentication and role-based access
- Add confidence scoring for extraction and PII detection

## License
This project is licensed under MIT. See LICENSE.
