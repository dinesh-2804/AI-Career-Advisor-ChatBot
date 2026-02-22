from backend.gemini_client import GeminiClient
from backend.memory_manager import MemoryManager
from backend.prompt_manager import PromptManager
from backend.logger import setup_logger

# Setup logger
logger = setup_logger()


class CareerChatbot:

    def __init__(self):
        self.client = GeminiClient()
        self.prompt_manager = PromptManager()
        logger.info("CareerChatbot initialized.")

    def get_response(self, user_input):
        try:
            logger.info("Processing user input.")

            # ------------------ Trim Very Long User Input ------------------
            MAX_USER_INPUT_LENGTH = 1000

            if len(user_input) > MAX_USER_INPUT_LENGTH:
                logger.warning("User input too long. Trimming input.")
                user_input = user_input[:MAX_USER_INPUT_LENGTH]

            # Store user message
            MemoryManager.add_message("user", user_input)

            # ------------------ Build Prompt ------------------
            history = MemoryManager.get_history()
            prompt = self.prompt_manager.build_prompt(history, user_input)

            # ------------------ Prompt Size Guard ------------------
            MAX_PROMPT_LENGTH = 6000

            if len(prompt) > MAX_PROMPT_LENGTH:
                logger.warning("Prompt too large. Reducing history.")
                history = history[-4:]  # Keep only latest 4 messages
                prompt = self.prompt_manager.build_prompt(history, user_input)

            # ------------------ Call Gemini API ------------------
            response = self.client.generate_response(prompt)

            # Store assistant response
            MemoryManager.add_message("assistant", response)

            logger.info("Response successfully generated.")

            return response

        except Exception as e:
            logger.error(f"Chatbot processing error: {str(e)}")
            return "⚠️ Something unexpected happened. Please try again."