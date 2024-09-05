# DarijaAssistant Library

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

**DarijaAssistant** is a Python library designed to assist in translating Moroccan Darija (a dialect of Arabic) into English. It integrates two main functionalities:

1. **Assisted Translation**: The `DarijaAssistant` class provides additional support for translating words and sentences using a custom [word-distance algorithm](https://pypi.org/project/DarijaDistance/), offering assistance to improve translation accuracy, especially for difficult or ambiguous phrases.

2. **LLM Client**: A client that allows interaction with any language model (LLM) hosted at any URL. For enhanced usability, the library also provides built-in support for OpenAI’s GPT models, allowing users to easily integrate them by simply providing the OpenAI API key and the model name, making it work out of the box.

This library allows users to perform both raw and assisted translations, improving the contextual understanding of Moroccan Darija sentences through caching, normalization, and additional linguistic analysis.


## Installation

To install the library, run:

```bash
pip install DarijaAssistant
```

## Usage

### 1. Initializing the Translation model

You can choose between a model hosted at any URL or OpenAI. Here's how to initialize the client:

```python
from DarijaAssistant import LLMClient

# Example using OpenAI GPT model
llm_client = LLMClient(use_openai=True, openai_api_key="your_openai_api_key", openai_model="gpt-4o")

# Example using an LLM hosted at a specific URL
llm_client = LLMClient(llm_url="http://your-llm-url.com", use_openai=False)
```

### 2. Simple Translation

You can perform a direct translation using the LLM client.

```python
sentence = "law3lm asahbi"
# only uses OpenAI's gpt-4o
translation_without_assistance = llm_client.translate(sentence)
print(translation_without_assistance)

# [output]: The world, my friend.
```

### 3. Assisted Translation

For more context-aware translation, use the *DarijaAssistant* class. This will assist the translation process by leveraging a word-distance algorithm.

```python
from DarijaAssistant import DarijaAssistant

# Initialize DarijaAssistant with the LLM client
assistant = DarijaAssistant(llm_client=llm_client)

# Use assisted translation: OpenAI's gpt-4o + DarijaAssistant
sentence = "law3lm asahbi"
result = assistant.assist_and_translate(sentence)
print(result)

# [output]: I do not know my friend.
```

### 4. Example Translations

Here's the difference between GPT-4 translations and our approach, showing how each handles Darija sentences with and without specialized assistance.

| Darija Sentence    | GPT4o Translation Without Assistance | Assisted Translation     |
|--------------------|--------------------------------------|--------------------------|
| law3lm asahbi      | The world, my friend.                | I do not know my friend. |
| kbchlaba9ich       | I feel thirsty.                      | Fill my cup.             |
| 3rram dyal lbrahch | Brahch's pen.                        | Plenty of kids.          |
| chof 3la tfrnisa   | Check the outlet.                    | Look at the smile.       |

### 5. Expanding the Dictionary

You can add new words and translations using the DarijaDataManager from the DarijaDistance package, which the DarijaAssistant library relies on.

```python
from DarijaDistance.preprocess import DarijaDataManager

data_manager = DarijaDataManager()
data_manager.add_translations([('khona', 'brother')])
```

Now, the word "khona" will be recognized and translated as "brother" in future translations. This addition is persistent, meaning it will be saved to the library's data, not just the current session. As a result, future instances of DarijaAssistant will automatically recognize and apply this translation, without needing to re-add it.

### 6. Access to Word-Distance Methods

As a user of the DarijaAssistant library, you have access to all the methods from the [word-distance algorithm](https://pypi.org/project/DarijaDistance/), such as checking translation confidence, retrieving exact matches, and more.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or find a bug, please open an issue or submit a pull request to the Github repo.


## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/aissam-out/DarijaTranslatorAssistant/blob/main/License) file for more details.

## Contact

If you have any questions or feedback, you can find me on LinkedIn: [Aissam Outchakoucht](https://www.linkedin.com/in/aissam-outchakoucht/) or on X: [@aissam_out](https://x.com/aissam_out).
