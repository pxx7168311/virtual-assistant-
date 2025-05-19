
import spacy
from transformers import pipeline

class AIManager:
    def __init__(self):
        self.nlp_en = spacy.load("en_core_web_sm")
        self.nlp_multi = spacy.load("xx_ent_wiki_sm")
        self.generator_en = pipeline("text-generation", model="distilgpt2")
        try:
            self.generator_ar = pipeline("text-generation", model="akhooli/gpt2-small-arabic")
        except:
            self.generator_ar = None

    def detect_lang(self, text):
        for ch in text:
            if '\u0600' <= ch <= '\u06FF':
                return "ar"
        return "en"

    def analyze_text(self, text):
        lang = self.detect_lang(text)
        nlp = self.nlp_en if lang == "en" else self.nlp_multi
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return lang, entities

    def generate_text(self, prompt):
        lang = self.detect_lang(prompt)
        if lang == "ar" and self.generator_ar:
            result = self.generator_ar(prompt, max_length=50)
        else:
            result = self.generator_en(prompt, max_length=50)
        return result[0]['generated_text']
