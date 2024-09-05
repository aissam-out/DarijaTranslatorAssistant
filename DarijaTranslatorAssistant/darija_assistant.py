import json
import logging
from DarijaDistance.word_distance import WordDistance

logging.basicConfig(level=logging.WARNING)

class DarijaAssistant:
    """
    A class to assist with Darija to English translations, leveraging a language model client 
    and a custom WordDistance utility for word-based translation assistance.
    
    Attributes:
        use_json (bool): Determines if the response should be in JSON format.
        word_distance (WordDistance): An instance of the WordDistance class to manage word distances and translations.
        translation_cache (dict): A cache to store translations for faster lookup.
        exact_translation_cache (dict): A cache to store exact translations for faster lookup.
        llm_client (Optional): A language model client to handle more complex translations.
    """
    def __init__(self, llm_client=None, use_json=True, sum_threshold=100, distance_threshold=10, 
                 acceptance_threshold=20, max_words=3):
        """
        Initializes the DarijaAssistant class with thresholds and caching mechanisms.

        Args:
            llm_client: An instance of the LLM client for advanced translations. Defaults to None.
            use_json (bool): Flag to return translations as JSON strings. Defaults to True.
            sum_threshold (int): Threshold used in word distance calculations. Defaults to 100.
            distance_threshold (int): Distance threshold for word matching. Defaults to 10.
            acceptance_threshold (int): Acceptance threshold for word translation. Defaults to 20.
            max_words (int): Maximum number of words considered in translation context. Defaults to 3.
        """
        self.use_json = use_json
        self.word_distance = WordDistance(sum_threshold, distance_threshold, acceptance_threshold, max_words)
        self.translation_cache = {}
        self.exact_translation_cache = {}
        self.llm_client = llm_client

    # Provide access to the WordDistance methods
    def __getattr__(self, name):
        """
        Provides access to methods from the WordDistance class by delegation.
        
        Args:
            name (str): The name of the method to be delegated.

        Returns:
            method: The method from WordDistance if it exists.
        
        Raises:
            AttributeError: If the attribute is not found in both the current class and WordDistance.
        """
        try:
            return getattr(self.word_distance, name)
        except AttributeError as e:
            raise AttributeError(f"'DarijaAssistant' object has no attribute '{name}'") from e


    def _normalize_sentence(self, sentence):
        """
        Normalizes a sentence by replacing specific substrings and removing punctuation.

        Args:
            sentence (str): The input sentence to normalize.

        Returns:
            str: A normalized version of the input sentence.
        """
        replacements = {
            "ou": "o",
            "chch": "ch",
            "khkh": "kh",
            "ghgh": "gh",
            "x": "ch"
        }
        for old, new in replacements.items():
            sentence = sentence.replace(old, new)
        
        try:
            return self.word_distance.remove_punctuation(sentence)
        except Exception as e:
            logging.error(f"Error in sentence normalization: {e}")
            raise ValueError(f"Normalization failed: {e}")

    def lookup_translation(self, sentence):
        """
        Looks up word translations in the sentence using cached and WordDistance translations.

        Args:
            sentence (str): The input sentence for translation.

        Returns:
            str or dict: The translation result in JSON string format or dictionary, depending on 'use_json' flag.

        Raises:
            ValueError: If the input sentence is empty or invalid.
        """
        if not sentence:
            raise ValueError("Input sentence cannot be empty.")
        
        normalized_sentence = self._normalize_sentence(sentence)
        words = normalized_sentence.split()
        response = {}

        for word in words:
            if word in self.translation_cache:
                translation = self.translation_cache[word]
            else:
                translation = self.word_distance.lookup_translation_word(word)
                self.translation_cache[word] = translation

            if translation:
                response[word] = translation

        return json.dumps(response) if self.use_json else response

    def lookup_exact_translation(self, sentence):
        """
        Looks up exact word translations in the sentence using cached and WordDistance translations.

        Args:
            sentence (str): The input sentence for exact translation.

        Returns:
            str or dict: The exact translation result in JSON string format or dictionary, depending on 'use_json' flag.

        Raises:
            ValueError: If the input sentence is empty or invalid.
        """
        if not sentence:
            raise ValueError("Input sentence cannot be empty.")
        
        normalized_sentence = self._normalize_sentence(sentence)
        words = normalized_sentence.split()
        response = {}

        for word in words:
            if word in self.exact_translation_cache:
                translation = self.exact_translation_cache[word]
            else:
                translation = self.word_distance.get_all_exact_translations(word)
                self.exact_translation_cache[word] = translation

            if translation:
                response[word] = translation

        return json.dumps(response) if self.use_json else response

    def assist_and_translate(self, sentence, exact=False, custom_prompt=None):
        """
        Translates a Darija sentence to English using a language model client and translation assistance.

        Args:
            sentence (str): The input Darija sentence.
            exact (bool): Flag indicating whether to use exact translations.
            custom_prompt (str): An optional custom prompt to override the default translation prompt that is passed to the LLM.

        Returns:
            str: The final translation or an error message.

        Raises:
            ValueError: If the input sentence is empty or invalid.
        """
        if not sentence:
            raise ValueError("Input sentence cannot be empty.")
        try:
            # Determine which lookup method to use
            if exact:
                assistance = self.lookup_exact_translation(sentence)
            else:
                assistance = self.lookup_translation(sentence)
        except Exception as e:
            logging.error(f"Failed to look up translation: {e}")
            return "Translation failed."
        
        # Prepare the prompt for the LLM, allowing for user customization
        default_prompt = f"Translate from Darija to English using the sentence and the following assistance: #SENTENCE: {sentence}. #ASSISTANCE: {assistance}"
        prompt = custom_prompt if custom_prompt else default_prompt
        
        try:
            # Use the LLM client to perform the translation
            translation = self.llm_client.translate(prompt)
            return translation
        except Exception as e:
            logging.error(f"Failed to translate using LLM: {e}")
            return "Translation failed."

if __name__ == "__main__":
    try:
        from DarijaTranslatorAssistant.llm_client import LLMClient
        
        # Optionally initialize LLMClient
        llm_client = LLMClient(use_openai=True, openai_api_key="your_openai_api_key", openai_model="gpt-4")

        # Initialize DarijaAssistant with or without LLMClient
        darija_assistant = DarijaAssistant(llm_client=llm_client)

        # Perform a translation
        result = darija_assistant.assist_and_translate("Translate this Darija sentence.")
        print(result)
    except Exception as e:
        logging.error(f"Error in DarijaAssistant: {e}")