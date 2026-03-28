import google.generativeai as genai
import os
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiAnalyzer:
    """Class to handle analysis of cleansed files using Google's Gemini AI"""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash-001"):
        """
        Initialize the Gemini analyzer
        
        Args:
            api_key (str, optional): Google Gemini API key. If not provided, 
                                   will try to get from GEMINI_API_KEY environment variable
            model_name (str): Name of the Gemini model to use
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model_name = model_name
        
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable or pass api_key parameter.")
        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(self.model_name)
        
        logger.info(f"Gemini Analyzer initialized successfully with model: {self.model_name}")
    
    def analyze_cleansed_content(self, content: str, file_type: str = "unknown") -> Dict[str, Any]:
        """
        Analyze cleansed content using Gemini AI
        
        Args:
            content (str): The cleansed text content to analyze
            file_type (str): Type of the original file (e.g., 'pdf', 'image', 'excel')
            
        Returns:
            dict: Analysis results including summary, insights, and recommendations
        """
        try:
            # Create a prompt for Gemini AI
            prompt = self._create_analysis_prompt(content, file_type)
            
            # Generate response from Gemini
            response = self.model.generate_content(prompt)
            
            # Extract the text response
            analysis_result = response.text if response.text else "No analysis available"
            
            return {
                "success": True,
                "analysis": analysis_result,
                "file_type": file_type,
                "content_length": len(content)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing content with Gemini: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "file_type": file_type,
                "content_length": len(content) if content else 0
            }
    
    def _create_analysis_prompt(self, content: str, file_type: str) -> str:
        """
        Create a detailed prompt for Gemini AI analysis
        
        Args:
            content (str): The content to analyze
            file_type (str): Type of the file
            
        Returns:
            str: Formatted prompt for Gemini AI
        """
        prompt = f"""
        Please analyze the following {file_type.upper()} document content and provide a comprehensive analysis:

        CONTENT TO ANALYZE:
        {content}

        Please provide your analysis in the following structured format:

        ## DOCUMENT OVERVIEW
        - Document type and purpose
        - Key topics or themes
        - Overall tone and style

        ## MAIN CONTENT SUMMARY
        - Brief summary of the main points
        - Key sections or chapters (if applicable)

        ## KEY INSIGHTS
        - Important findings or data points
        - Notable patterns or trends
        - Significant observations

        ## POTENTIAL USE CASES
        - How this document might be used
        - Target audience
        - Business or research applications

        ## RECOMMENDATIONS
        - Suggestions for further action
        - Areas for additional research
        - Potential improvements or considerations

        Please ensure your analysis is professional, thorough, and actionable.
        """
        
        return prompt
    
    def analyze_security_aspects(self, content: str) -> Dict[str, Any]:
        """
        Analyze security aspects of the content using Gemini AI
        
        Args:
            content (str): The content to analyze for security aspects
            
        Returns:
            dict: Security analysis results
        """
        try:
            prompt = f"""
            As a cybersecurity expert, please analyze the following document content for security implications:

            CONTENT:
            {content}

            Please provide your security analysis in the following format:

            ## SECURITY ASSESSMENT
            - Overall security posture
            - Identified risks or vulnerabilities
            - Compliance considerations

            ## DATA SENSITIVITY ANALYSIS
            - Types of data present
            - Sensitivity level assessment
            - Privacy implications

            ## RECOMMENDATIONS
            - Security best practices
            - Risk mitigation strategies
            - Policy recommendations

            Focus specifically on security and data protection aspects.
            """
            
            response = self.model.generate_content(prompt)
            security_analysis = response.text if response.text else "No security analysis available"
            
            return {
                "success": True,
                "security_analysis": security_analysis
            }
            
        except Exception as e:
            logger.error(f"Error analyzing security aspects with Gemini: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

# Flask integration function
def analyze_with_gemini(content: str, file_type: str = "unknown", api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyze content using Gemini AI
    
    Args:
        content (str): The content to analyze
        file_type (str): Type of the original file
        api_key (str, optional): Gemini API key
        
    Returns:
        dict: Analysis results
    """
    try:
        analyzer = GeminiAnalyzer(api_key=api_key, model_name="gemini-2.0-flash-001")
        return analyzer.analyze_cleansed_content(content, file_type)
    except Exception as e:
        logger.error(f"Error initializing Gemini analyzer: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
