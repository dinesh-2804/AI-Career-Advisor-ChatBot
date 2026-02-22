import google.generativeai as genai
import os
from dotenv import load_dotenv
from config.settings import MODEL_NAME, TEMPERATURE, MAX_OUTPUT_TOKENS
from backend.logger import setup_logger

# Setup logger
logger = setup_logger()

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class GeminiClient:

    def __init__(self):
        self.model = genai.GenerativeModel(MODEL_NAME)

    def generate_response(self, prompt):
        try:
            logger.info("Gemini API call started.")

            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": TEMPERATURE,
                    "max_output_tokens": MAX_OUTPUT_TOKENS
                }
            )

            # ------------------ Response Validation ------------------

            if not response or not response.text:
                logger.warning("Empty response received from Gemini API.")
                return "⚠️ I couldn't generate a proper response. Please try rephrasing your question."

            cleaned_text = response.text.strip()

            # Remove excessive blank lines
            cleaned_text = "\n".join(
                line.strip() for line in cleaned_text.splitlines() if line.strip()
            )

            # Prevent extremely short meaningless responses
            if len(cleaned_text) < 20:
                logger.warning("Very short response detected.")
                return "⚠️ The response was too brief. Please try asking your question differently."

            # Trim overly long responses (safety guard)
            if len(cleaned_text) > 3000:
                logger.warning("Response too long. Trimming output.")
                cleaned_text = cleaned_text[:3000] + "\n\n⚠️ (Response trimmed for length)"

            logger.info("Gemini API call successful and response processed.")

            return cleaned_text

        except ValueError as ve:
            logger.error(f"ValueError during Gemini call: {str(ve)}")
            return "⚠️ Invalid input detected. Please check your question and try again."

        except ConnectionError as ce:
            logger.error(f"ConnectionError during Gemini call: {str(ce)}")
            return "⚠️ Network issue detected. Please check your internet connection."

        except Exception as e:
            logger.error(f"Unexpected Gemini API error: {str(e)}")
            return "⚠️ The system is temporarily unavailable. Please try again in a moment."