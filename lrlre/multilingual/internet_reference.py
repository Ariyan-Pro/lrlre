"""
INTERNET REFERENCE SYSTEM - FIXED VERSION
Provides reference information for languages and scripts
"""
import unicodedata
from typing import Dict, List, Any, Optional

class InternetReferenceSystem:
    """Provides reference information about languages and writing systems"""
    
    def __init__(self):
        self.language_info = {
            'en': {
                'name': 'English',
                'script': 'Latin',
                'family': 'Germanic',
                'speakers': '1.5B',
                'countries': ['US', 'UK', 'Canada', 'Australia', 'New Zealand']
            },
            'fr': {
                'name': 'French',
                'script': 'Latin',
                'family': 'Romance',
                'speakers': '300M',
                'countries': ['France', 'Canada', 'Belgium', 'Switzerland']
            },
            'ja': {
                'name': 'Japanese',
                'script': 'Mixed (Hiragana, Katakana, Kanji)',
                'family': 'Japonic',
                'speakers': '125M',
                'countries': ['Japan']
            },
            'ko': {
                'name': 'Korean',
                'script': 'Hangul',
                'family': 'Koreanic',
                'speakers': '80M',
                'countries': ['South Korea', 'North Korea']
            },
            'zh': {
                'name': 'Chinese',
                'script': 'Hanzi',
                'family': 'Sinitic',
                'speakers': '1.3B',
                'countries': ['China', 'Taiwan', 'Singapore']
            }
        }
    
    def get_language_info(self, lang_code: str) -> Dict[str, Any]:
        """Get reference information for a language"""
        return self.language_info.get(lang_code, {
            'name': 'Unknown',
            'script': 'Unknown',
            'family': 'Unknown',
            'speakers': 'Unknown',
            'countries': []
        })
    
    def detect_script(self, text: str) -> List[str]:
        """Detect writing scripts used in text"""
        scripts = set()
        
        for char in text[:100]:  # Check first 100 chars
            code = ord(char)
            
            # Japanese
            if 0x3040 <= code <= 0x309F:
                scripts.add('Hiragana')
            elif 0x30A0 <= code <= 0x30FF:
                scripts.add('Katakana')
            # CJK (Chinese/Japanese Kanji)
            elif 0x4E00 <= code <= 0x9FFF:
                scripts.add('CJK')
            # Korean
            elif 0xAC00 <= code <= 0xD7AF:
                scripts.add('Hangul')
            # Latin (English/French)
            elif 0x0041 <= code <= 0x007A or 0x00C0 <= code <= 0x00FF:
                scripts.add('Latin')
        
        return list(scripts)
    
    def _has_mixed_scripts(self, text: str) -> bool:
        """Check if text contains mixed scripts"""
        scripts = self.detect_script(text)
        return len(scripts) > 1

# Test if run directly
if __name__ == "__main__":
    ref_system = InternetReferenceSystem()
    print("✅ Internet Reference System Loaded Successfully")
    
    # Test with sample text
    test_text = "Hello こんにちは"
    scripts = ref_system.detect_script(test_text)
    print(f"Scripts in '{test_text}': {', '.join(scripts)}")


