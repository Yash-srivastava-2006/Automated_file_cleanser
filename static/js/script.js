// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        window.scrollTo({
            top: targetElement.offsetTop - 70,
            behavior: 'smooth'
        });
    });
});

// File upload form handling
const uploadForm = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const resultsContainer = document.getElementById('results');

// Update file input label when files are selected
fileInput.addEventListener('change', function() {
    const fileLabel = document.querySelector('.file-upload-label span');
    if (this.files.length > 0) {
        const fileNames = Array.from(this.files).map(file => file.name).join(', ');
        fileLabel.textContent = `${this.files.length} file(s) selected`;
    } else {
        fileLabel.textContent = 'Choose Files';
    }
});

// Handle file upload
uploadForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (fileInput.files.length === 0) {
        alert('Please select at least one file to upload.');
        return;
    }
    
    const formData = new FormData();
    for (let i = 0; i < fileInput.files.length; i++) {
        formData.append('files[]', fileInput.files[i]);
    }
    
    // Show loading indicator
    resultsContainer.innerHTML = `
        <div class="loading">
            <p>Processing files... This may take a moment.</p>
            <div class="spinner"></div>
        </div>
    `;
    
    // Send files to backend
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            resultsContainer.innerHTML = `<p class="error">Error: ${data.error}</p>`;
            return;
        }
        
        displayResults(data.results);
    })
    .catch(error => {
        resultsContainer.innerHTML = `<p class="error">Error uploading files: ${error.message}</p>`;
    });
});

// Display processing results
function displayResults(results) {
    if (results.length === 0) {
        resultsContainer.innerHTML = '<p>No files were processed.</p>';
        return;
    }
    
    let resultsHTML = '';
    
    results.forEach(result => {
        // Check if there's an OCR error
        let ocrError = '';
        if (result.cleansed_text && (result.cleansed_text.includes('Tesseract OCR is not installed') || 
            result.extracted_text.includes('Tesseract OCR is not installed'))) {
            ocrError = `
                <div class="error-message">
                    <h3>OCR Not Available</h3>
                    <p>To extract text from images, you need to install Tesseract OCR.</p>
                    <div class="install-instructions">
                        <h4>Installation Instructions:</h4>
                        <ol>
                            <li>Download Tesseract from: <a href="https://github.com/UB-Mannheim/tesseract/wiki" target="_blank" rel="noopener">Tesseract Windows Installer</a></li>
                            <li>Run the installer and follow the installation process</li>
                            <li>Make sure to check <strong>"Add to PATH"</strong> during installation</li>
                            <li>Restart this application after installation</li>
                        </ol>
                        <p><strong>After installation, please restart the application for changes to take effect.</strong></p>
                    </div>
                </div>
            `;
        }
        
        // Check if this is a security analysis result
        let securityAnalysis = '';
        if (result.cleansed_text && result.cleansed_text.includes('SECURITY ANALYSIS')) {
            securityAnalysis = `
                <div class="security-analysis">
                    <h4>Security Analysis</h4>
                    <p>This file has been analyzed for security-related information.</p>
                </div>
            `;
        }
        
        resultsHTML += `
            <div class="result-card">
                <div class="result-header">
                    <h3 class="result-title">${result.original_filename}</h3>
                    <div class="result-actions">
                        <a href="/download/cleansed/${result.cleansed_filename}" class="download-btn">Download Cleansed</a>
                        <button class="btn btn-secondary analyze-btn" data-filename="${result.cleansed_filename}">Transfer to Analyzer</button>
                        <button class="btn btn-secondary gemini-btn" data-filename="${result.cleansed_filename}">Gemini AI Analysis</button>
                    </div>
                </div>
                
                ${ocrError}
                ${securityAnalysis}
                
                <div class="file-info">
                    <p><strong>File Type:</strong> ${result.file_type || 'Unknown'}</p>
                    <p><strong>Status:</strong> Cleansed and ready for analysis</p>
                </div>
            </div>
        `;
    });
    
    resultsContainer.innerHTML = resultsHTML;
    
    // Add event listeners to analyze buttons
    document.querySelectorAll('.analyze-btn').forEach(button => {
        button.addEventListener('click', function() {
            const filename = this.getAttribute('data-filename');
            analyzeFile(filename, this);
        });
    });
    
    // Add event listeners to Gemini AI buttons
    document.querySelectorAll('.gemini-btn').forEach(button => {
        button.addEventListener('click', function() {
            const filename = this.getAttribute('data-filename');
            analyzeWithGemini(filename, this);
        });
    });
}

// Analyze a file
function analyzeFile(filename, button) {
    // Show loading indicator
    const originalText = button.textContent;
    button.textContent = 'Analyzing...';
    button.disabled = true;
    
    // Send request to analyze the file
    fetch(`/analyze/${filename}`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`Error: ${data.error}`);
            button.textContent = originalText;
            button.disabled = false;
            return;
        }
        
        // Show analysis results
        showAnalysisResults(data, filename);
        button.textContent = originalText;
        button.disabled = false;
    })
    .catch(error => {
        alert(`Error analyzing file: ${error.message}`);
        button.textContent = originalText;
        button.disabled = false;
    });
}

// Show analysis results
function showAnalysisResults(data, filename) {
    const analysisModal = document.createElement('div');
    analysisModal.className = 'analysis-modal';
    analysisModal.innerHTML = `
        <div class="analysis-modal-content">
            <div class="analysis-modal-header">
                <h2>Analysis Results</h2>
                <span class="close-modal">&times;</span>
            </div>
            <div class="analysis-modal-body">
                <div class="text-content">
                    <h4>Extracted Text:</h4>
                    <pre>${escapeHtml(data.extracted_text)}</pre>
                </div>
                <div class="text-content">
                    <h4>Final Output:</h4>
                    <pre>${escapeHtml(data.final_output)}</pre>
                </div>
                <div class="analysis-actions">
                    <a href="/download/processed/${data.analyzed_filename}" class="btn btn-primary">Download Analysis</a>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(analysisModal);
    
    // Add event listener to close modal
    analysisModal.querySelector('.close-modal').addEventListener('click', function() {
        document.body.removeChild(analysisModal);
    });
    
    // Close modal when clicking outside
    analysisModal.addEventListener('click', function(e) {
        if (e.target === analysisModal) {
            document.body.removeChild(analysisModal);
        }
    });
}

// Analyze a file with Gemini AI
function analyzeWithGemini(filename, button) {
    // Show loading indicator
    const originalText = button.textContent;
    button.textContent = 'Analyzing with AI...';
    button.disabled = true;
    
    // Send request to analyze the file with Gemini AI
    fetch(`/gemini-analyze/${filename}`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`Error: ${data.error}`);
            button.textContent = originalText;
            button.disabled = false;
            return;
        }
        
        // Show Gemini AI analysis results
        showGeminiAnalysisResults(data, filename);
        button.textContent = originalText;
        button.disabled = false;
    })
    .catch(error => {
        alert(`Error analyzing file with Gemini AI: ${error.message}`);
        button.textContent = originalText;
        button.disabled = false;
    });
}

// Show Gemini AI analysis results
function showGeminiAnalysisResults(data, filename) {
    const analysisModal = document.createElement('div');
    analysisModal.className = 'analysis-modal';
    analysisModal.innerHTML = `
        <div class="analysis-modal-content">
            <div class="analysis-modal-header">
                <h2>Gemini AI Analysis Results</h2>
                <span class="close-modal">&times;</span>
            </div>
            <div class="analysis-modal-body">
                <div class="text-content">
                    <h4>File Type:</h4>
                    <p>${data.file_type}</p>
                </div>
                <div class="text-content">
                    <h4>Gemini AI Analysis:</h4>
                    <pre>${escapeHtml(data.analysis)}</pre>
                </div>
                <div class="analysis-actions">
                    <a href="/download/processed/${data.gemini_filename}" class="btn btn-primary">Download AI Analysis</a>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(analysisModal);
    
    // Add event listener to close modal
    analysisModal.querySelector('.close-modal').addEventListener('click', function() {
        document.body.removeChild(analysisModal);
    });
    
    // Close modal when clicking outside
    analysisModal.addEventListener('click', function(e) {
        if (e.target === analysisModal) {
            document.body.removeChild(analysisModal);
        }
    });
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Contact form handling
const contactForm = document.getElementById('contactForm');

contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    
    // In a real application, you would send this data to your backend
    alert(`Thank you, ${name}! Your message has been received. We'll contact you at ${email} soon.`);
    
    // Reset form
    contactForm.reset();
});

// Simple spinner for loading indication
const style = document.createElement('style');
style.innerHTML = `
    .spinner {
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top: 4px solid #6c5ce7;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading {
        text-align: center;
        padding: 20px;
    }
    
    .error {
        color: #ff7675;
        text-align: center;
        padding: 20px;
    }
    
    .error-message {
        background: rgba(255, 118, 117, 0.2);
        border: 1px solid #ff7675;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
    }
    
    .error-message h3 {
        color: #ff7675;
        margin-top: 0;
    }
    
    .error-message a {
        color: #a29bfe;
        text-decoration: underline;
    }
    
    .install-instructions ol {
        margin: 10px 0;
        padding-left: 20px;
    }
    
    .install-instructions li {
        margin-bottom: 8px;
    }
    
    .install-instructions strong {
        color: #a29bfe;
    }
    
    .security-analysis {
        background: rgba(0, 184, 148, 0.2);
        border: 1px solid #00b894;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
    }
    
    .security-analysis h4 {
        color: #00b894;
        margin-top: 0;
    }
    
    .result-actions {
        display: flex;
        gap: 10px;
    }
    
    .file-info {
        background: rgba(0, 0, 0, 0.2);
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
    
    .analyze-btn {
        background: var(--warning-color);
        color: #2d3436;
        border: none;
        padding: 8px 16px;
        border-radius: 20px;
        cursor: pointer;
        font-weight: 600;
    }
    
    .analyze-btn:hover {
        background: #e1b12c;
        transform: translateY(-2px);
    }
    
    .analyze-btn:disabled {
        background: #7f8c8d;
        cursor: not-allowed;
        transform: none;
    }
    
    .analysis-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }
    
    .analysis-modal-content {
        background: #1a1a2e;
        border-radius: 10px;
        width: 90%;
        max-width: 800px;
        max-height: 90vh;
        overflow: hidden;
        border: 1px solid var(--secondary-color);
    }
    
    .analysis-modal-header {
        padding: 20px;
        border-bottom: 1px solid rgba(108, 92, 231, 0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .analysis-modal-header h2 {
        margin: 0;
        color: var(--secondary-color);
    }
    
    .close-modal {
        font-size: 2rem;
        cursor: pointer;
        color: var(--light-color);
    }
    
    .close-modal:hover {
        color: var(--secondary-color);
    }
    
    .analysis-modal-body {
        padding: 20px;
        max-height: 70vh;
        overflow-y: auto;
    }
    
    .analysis-actions {
        text-align: center;
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid rgba(108, 92, 231, 0.3);
    }
`;
document.head.appendChild(style);