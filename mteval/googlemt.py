# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/04_googlemt.ipynb.

# %% auto 0
__all__ = ['googletranslate']

# %% ../nbs/04_googlemt.ipynb 8
import os
import six
from google.cloud import translate

class googletranslate:
    """Class to get translations from the Google Translate API"""

    def __init__(self):
        """ Constructor of googletranslate class. Load the credentials for the Google API"""
        # Google credentials need to be available in JSON file specified in the GOOGLE_APPLICATION_CREDENTIALS environment variable
        project_id = os.getenv('GOOGLE_PROJECT_ID')
        location = "global"
        
        self._translate_client = translate.TranslationServiceClient()
        self._parent = f"projects/{project_id}/locations/{location}"

    def translate_text(self,sourcelang, targetlang, text):
        """Function to translate text into the target language"""
        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        response = self._translate_client.translate_text(
            request={
                "parent": self._parent,
                "contents": [text],
                "mime_type": "text/plain",  # mime types: text/plain, text/html
                "source_language_code": sourcelang,
                "target_language_code": targetlang,
            }
        )

        return response.translations[0].translated_text
