import json
import logging
import requests
from openai import OpenAI

class LLMClient:
    """
    A class to handle interactions with either a generic language model (LLM) hosted in a remote server 
    or the OpenAI API for translation and other LLM-based tasks.
    
    Attributes:
        llm_url (str): The URL of the hosted LLM.
        use_openai (bool): A flag to indicate whether to use OpenAI or another LLM.
        openai_client (OpenAI): An instance of the OpenAI client.
        openai_model (str): The OpenAI model to be used for generating responses.
        openai_kwargs (dict): Additional keyword arguments to pass to the OpenAI API.
    """
    def __init__(self, llm_url="http://localhost:8000", use_openai=False, 
                 openai_api_key=None, openai_model="gpt-4o-mini", **openai_kwargs):
        """
        Initializes the LLMClient class, setting up either a connection to a remote LLM URL or OpenAI.

        Args:
            llm_url (str): The URL for the hosted LLM.
            use_openai (bool): A flag to use the OpenAI API or another LLM.
            openai_api_key (str): The API key for OpenAI, required if `use_openai` is True.
            openai_model (str): The OpenAI model to be used.
            **openai_kwargs: Additional keyword arguments for the OpenAI API client.

        Raises:
            ValueError: If OpenAI client initialization fails.
        """
        self.llm_url = llm_url
        self.use_openai = use_openai
        self.openai_client = None

        if self.use_openai and openai_api_key:
            try:
                self.openai_client = OpenAI(api_key=openai_api_key)
                self.openai_model = openai_model
                self.openai_kwargs = openai_kwargs
            except Exception as e:
                logging.error(f"Failed to initialize OpenAI client: {e}")
                raise ValueError("Failed to initialize OpenAI client.") from e

    def _handle_openai_response(self, response):
        """
        Handles the response from OpenAI by extracting the relevant content.

        Args:
            response (dict): The response object returned from the OpenAI API.

        Returns:
            str: The extracted content from the OpenAI response.

        Raises:
            ValueError: If the response format is not as expected.
        """
        try:
            return response.choices[0].message.content
        except (IndexError, AttributeError) as e:
            logging.error(f"Unexpected response format from OpenAI: {e}")
            raise ValueError("Unexpected response format from OpenAI.") from e

    def call_openai(self, prompt):
        """
        Sends a prompt to the OpenAI API and retrieves the result.

        Args:
            prompt (str): The text prompt to be translated by OpenAI.

        Returns:
            str: The translation provided by OpenAI.

        Raises:
            ValueError: If the OpenAI client is not initialized.
            Exception: If the API request to OpenAI fails.
        """
        if not self.openai_client:
            raise ValueError("OpenAI client is not initialized.")
        
        messages = [
            {
                "role": "system", 
                "content": "You are a translator from Moroccan dialect -Darija- to English. Only give the translation of the sentence. No extra information."},
            {"role": "user", "content": prompt}
        ]
        try:
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=messages,
                **self.openai_kwargs
            )
            return self._handle_openai_response(response)
        except Exception as e:
            logging.error(f"Unexpected error when calling OpenAI: {e}")
            raise e

    def call_generic_llm(self, prompt, api_key=None):
        """
        Sends a translation prompt to a remote hosted LLM and retrieves the result.

        Args:
            prompt (str): The text to be translated by the LLM.
            api_key (str): The API key for the LLM, if required.

        Returns:
            str: The translation provided by the LLM.

        Raises:
            requests.exceptions.RequestException: If a network-related error occurs.
            json.JSONDecodeError: If the response cannot be parsed as valid JSON.
            Exception: If an unexpected error occurs.
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            'Authorization': f'Bearer {api_key}' if api_key else ''
        }
        payload = {"prompt": prompt}

        try:
            response = requests.post(self.llm_url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json().get("translation", "Translation failed.")
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error when calling LLM: {e}")
            raise ValueError("Failed to retrieve translation from LLM.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error when calling LLM: {e}")
            raise ValueError("Network error when calling LLM.")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON response from LLM: {e}")
            raise ValueError("Failed to decode JSON response from LLM.")
        except Exception as e:
            logging.error(f"Unexpected error when calling LLM: {e}")
            raise e

    def translate(self, prompt, api_key=None):
        """
        Translates the given prompt using either OpenAI or another LLM, depending on configuration.

        Args:
            prompt (str): The text to be translated.
            api_key (str, optional): API key for the hosted LLM, if applicable.

        Returns:
            str: The translated result.

        Raises:
            Exception: If the translation process encounters an error.
        """
        try:
            if self.use_openai:
                return self.call_openai(prompt)
            else:
                return self.call_generic_llm(prompt, api_key)
        except Exception as e:
            logging.error(f"Translation failed: {e}")
            raise e

# Example usage
if __name__ == "__main__":
    try:
        llm_client = LLMClient(use_openai=True, openai_api_key="your_openai_api_key", openai_model="gpt-4")
        result = llm_client.translate("Translate this sentence.")
        print(result)
    except Exception as e:
        logging.error(f"Translation failed: {e}")
