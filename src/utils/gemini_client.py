import os
import google.generativeai as genai
from dotenv import load_dotenv
from .logger import setup_logger

load_dotenv()

gemini_logger = setup_logger('gemini_client', 'gemini_client.log')

def get_gemini_response(prompt):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        gemini_logger.info("Configuring Gemini API")
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        gemini_logger.info("Sending prompt to Gemini")
        
        response = model.generate_content(prompt)
        gemini_logger.info("Received response from Gemini")
        
        return response.text
        
    except Exception as e:
        gemini_logger.error(f"Gemini API error: {str(e)}")
        raise e
