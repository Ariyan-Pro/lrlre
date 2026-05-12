"":
Enhanced grammar parser for Phase 2:
Handles: 
- Subject-Verb-Object (SVO):
- Subject-Verb-Object-IndirectObject (SVOIO):
- Subject-Verb-Complement (SVC):
- Possessive structures:
""":
:
import re:
:
class EnhancedGrammarParser:
    def __init__(self):
        self.patterns = {:
            'svo': r'^(\w+)\s+(\w+)\s+(\w+)$',  # John loves Mary
            'svoo': r'^(\w+)\s+(\w+)\s+(\w+)\s+to\s+(\w+)$',  # John gives book to Mary
            'svc': r'^(\w+)\s+(is|are|was|were)\s+(\w+)$',  # John is happy
            'possessive': r'^(\w+)\'s\s+(\w+)$',  # John's car
            'compound': r'^(\w+)\s+and\s+(\w+)\s+(\w+)\s+(\w+)$',  # John and Mary love cake
        }:
:
    def parse(self, tokens):
        """Parse tokens into grammatical structure""":
        text = ' '.join(tokens):
:
        # Check SVO pattern:
        if re.match(self.patterns['svo'], text):
            match = re.match(self.patterns['svo'], text):
            return {:
                'type': 'SVO',
                'subject': match.group(1),
                'verb': match.group(2),
                'object': match.group(3),
                'raw': text
            }:
:
        # Check SVOO pattern (ditransitive):
        elif re.match(self.patterns['svoo'], text):
            match = re.match(self.patterns['svoo'], text):
            return {:
                'type': 'SVOO',
                'subject': match.group(1),
                'verb': match.group(2),
                'direct_object': match.group(3),
                'indirect_object': match.group(4),
                'raw': text
            }:
:
        # Check SVC pattern (copula):
        elif re.match(self.patterns['svc'], text):
            match = re.match(self.patterns['svc'], text):
            return {:
                'type': 'SVC',
                'subject': match.group(1),
                'copula': match.group(2),
                'complement': match.group(3),
                'raw': text
            }:
:
        # Check possessive pattern:
        elif re.match(self.patterns['possessive'], text):
            match = re.match(self.patterns['possessive'], text):
            return {:
                'type': 'POSSESSIVE',
                'possessor': match.group(1),
                'possessed': match.group(2),
                'raw': text
            }:
:
        # Default to simple dependency parse:
        else:
            return self._simple_parse(tokens):
:
    def _simple_parse(self, tokens):
        """Fallback to simple parsing""":
        if len(tokens) < 2:
            return {'type': 'UNKNOWN', 'raw': ' '.join(tokens)}
:
        return {:
            'type': 'SIMPLE',
            'subject': tokens[0] if len(tokens) > 0 else None,
            'predicate': tokens[1] if len(tokens) > 1 else None,
            'object': tokens[2] if len(tokens) > 2 else None,
            'raw': ' '.join(tokens)
        }:
: