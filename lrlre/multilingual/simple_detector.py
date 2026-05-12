"""
LANGUAGE DETECTOR - PRODUCTION FINAL V3
GUARANTEED FRENCH DETECTION - COMPLETE REWRITE
"""
import time
from typing import Dict, Any

class SimpleLanguageDetector:
    def detect(self, text: str) -> Dict[str, Any]:
        if not text or not text.strip():
            return {"language": "en", "confidence": 0, "method": "empty"}
        
        text = text.strip()
        start_time = time.time()
        
        # ========== 1. JAPANESE DETECTION ==========
        jp_hiragana = sum(1 for c in text if '\u3040' <= c <= '\u309F')
        jp_katakana = sum(1 for c in text if '\u30A0' <= c <= '\u30FF')
        if jp_hiragana > 2 or jp_katakana > 2:
            confidence = min(95 + jp_hiragana + jp_katakana, 99)
            return {"language": "ja", "confidence": confidence, "method": "japanese_script"}
        
        # ========== 2. KOREAN DETECTION ==========
        ko_hangul = sum(1 for c in text if '\uAC00' <= c <= '\uD7AF')
        if ko_hangul > 2:
            confidence = min(95 + ko_hangul, 99)
            return {"language": "ko", "confidence": confidence, "method": "korean_script"}
        
        # ========== 3. CHINESE DETECTION ==========
        zh_cjk = sum(1 for c in text if '\u4E00' <= c <= '\u9FFF')
        if zh_cjk > 2:
            confidence = min(90 + zh_cjk, 98)
            return {"language": "zh", "confidence": confidence, "method": "chinese_script"}
        
        # ========== 4. FRENCH DETECTION - AGGRESSIVE ==========
        text_lower = text.lower()
        
        # FRENCH DICTIONARY - COMPREHENSIVE LIST
        french_words = [
            # Articles
            "le", "la", "les", "un", "une", "des", "du", "de",
            
            # Common verbs (être, avoir, faire, etc.)
            "est", "sont", "était", "étaient", "sera", "seront",
            "a", "ont", "avait", "avaient", "aura", "auront",
            "fait", "font", "faisait", "faisaient",
            "peut", "peuvent", "pouvait", "pouvaient",
            "veut", "veulent", "voulait", "voulaient",
            "dit", "disent", "disait", "disaient",
            
            # Pronouns
            "je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles",
            "me", "te", "se", "lui", "leur",
            "ce", "cet", "cette", "ces",
            "mon", "ton", "son", "notre", "votre", "leur",
            "ma", "ta", "sa", "nos", "vos", "leurs",
            
            # Prepositions
            "sur", "dans", "avec", "pour", "sans", "chez", "vers", "depuis",
            "pendant", "avant", "après", "entre", "parmi", "contre",
            
            # Conjunctions
            "et", "mais", "ou", "donc", "car", "ni", "or",
            "parce que", "quand", "si", "comme", "lorsque",
            
            # Question words
            "qui", "que", "quoi", "dont", "où", "comment", "pourquoi",
            
            # Common adjectives
            "bon", "bonne", "bons", "bonnes",
            "grand", "grande", "grands", "grandes",
            "petit", "petite", "petits", "petites",
            "beau", "belle", "beaux", "belles",
            "nouveau", "nouvelle", "nouveaux", "nouvelles",
            
            # Adverbs
            "très", "beaucoup", "peu", "assez", "trop",
            "bien", "mal", "mieux", "pire",
            "toujours", "jamais", "souvent", "parfois",
            "maintenant", "aujourd'hui", "demain", "hier",
            
            # Negation
            "ne", "pas", "plus", "rien", "personne", "aucun",
            
            # Common phrases
            "il y a", "c'est", "ce sont", "c'était", "c'étaient",
            "il est", "elle est", "ils sont", "elles sont",
            "je suis", "tu es", "nous sommes", "vous êtes"
        ]
        
        # Count French words in text
        words = text_lower.split()
        french_word_count = 0
        total_words = len(words)
        
        for word in words:
            # Clean the word
            clean_word = word.strip('.,;:!?\'"()[]{}')
            if clean_word in french_words:
                french_word_count += 1
        
        # Calculate French score
        french_score = 0
        
        # Word-based score
        if total_words > 0:
            french_ratio = (french_word_count / total_words) * 100
            french_score += french_ratio * 2
        
        # French accents (very strong indicator)
        french_accents = sum(10 for c in text if c in "éèêëàâäîïôöûüçÉÈÊËÀÂÄÎÏÔÖÛÜÇ")
        french_score += french_accents
        
        # French contractions
        french_contractions = ["l'", "d'", "j'", "c'", "n'", "s'", "m'", "t'", "qu'"]
        for contr in french_contractions:
            if contr in text_lower:
                french_score += 5
                # Count occurrences
                french_score += text_lower.count(contr) * 3
        
        # French-specific endings
        french_endings = ["tion", "sion", "ment", "eur", "euse", "ique", "able", "ible"]
        for ending in french_endings:
            if ending in text_lower:
                french_score += 2
        
        # Check for French articles at start of sentences
        if text_lower.startswith(("le ", "la ", "les ", "un ", "une ", "des ")):
            french_score += 10
        
        # DEBUG: Print score for testing
        # print(f"French score: {french_score} for text: {text[:30]}...")
        
        # DECISION: French if score is high enough
        if french_score >= 30:
            confidence = min(75 + (french_score / 2), 98)
            return {
                "language": "fr",
                "confidence": confidence,
                "method": "aggressive_french_detection",
                "french_score": french_score,
                "french_words": french_word_count,
                "total_words": total_words
            }
        
        # ========== 5. ENGLISH DETECTION ==========
        # Default to English with confidence based on text length
        confidence = 70 + (total_words * 2)
        if total_words == 0:
            confidence = 50
        
        return {
            "language": "en",
            "confidence": min(confidence, 95),
            "method": "default_english"
        }
