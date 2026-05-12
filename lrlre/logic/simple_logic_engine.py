"""
SIMPLE LOGIC ENGINE - FIXED VERSION
Provides logical inference capabilities for the LRLRE system
"""
from typing import Dict, List, Any, Optional
import time

class SimpleLogicEngine:
    """Simple rule-based logic engine for inferences"""
    
    def __init__(self):
        self.rules = []
        self.facts = []
        self._initialize_default_rules()
    
    def _initialize_default_rules(self):
        """Initialize default inference rules"""
        self.rules = [
            {
                'name': 'location_implies_presence',
                'condition': lambda fact: fact['predicate'] == 'is_on',
                'conclusion': lambda fact: {
                    'type': 'presence',
                    'conclusion': f"{fact['subject']} is present on {fact['object']}",
                    'confidence': 0.9
                }
            },
            {
                'name': 'liking_implies_preference',
                'condition': lambda fact: fact['predicate'] == 'likes',
                'conclusion': lambda fact: {
                    'type': 'preference',
                    'conclusion': f"{fact['subject']} prefers {fact['object']}",
                    'confidence': 0.85
                }
            },
            {
                'name': 'transitive_location',
                'condition': lambda fact: fact['predicate'] == 'is_on' and len(self.facts) > 1,
                'conclusion': lambda fact: {
                    'type': 'transitive',
                    'conclusion': f"Anything on {fact['subject']} is also associated with {fact['object']}",
                    'confidence': 0.7
                }
            }
        ]
    
    def add_fact(self, subject: str, predicate: str, object: str, confidence: float = 1.0):
        """Add a fact to the engine"""
        fact = {
            'subject': subject,
            'predicate': predicate,
            'object': object,
            'confidence': confidence,
            'timestamp': time.time()
        }
        self.facts.append(fact)
        return fact
    
    def infer(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Run inference on current facts"""
        start_time = time.time()
        
        inferences = []
        
        # Apply each rule to each fact
        for fact in self.facts[-10:]:  # Check last 10 facts for performance
            for rule in self.rules:
                try:
                    if rule['condition'](fact):
                        conclusion = rule['conclusion'](fact)
                        inferences.append({
                            'rule': rule['name'],
                            'fact': fact,
                            'conclusion': conclusion['conclusion'],
                            'type': conclusion['type'],
                            'confidence': conclusion['confidence'] * fact['confidence']
                        })
                except:
                    continue  # Skip rules that don't apply
        
        processing_time = (time.time() - start_time) * 1000
        
        return {
            'inferences': inferences[:5],  # Return top 5
            'inference_count': len(inferences),
            'processing_time_ms': round(processing_time, 2)
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics"""
        return {
            'facts': len(self.facts),
            'rules': len(self.rules),
            'inference_capable': len(self.rules) > 0
        }

def test_logic_engine():
    """Test function for the logic engine"""
    engine = SimpleLogicEngine()
    
    # Add test facts
    engine.add_fact("cat", "is_on", "mat")
    engine.add_fact("cat", "likes", "fish")
    
    # Run inference
    result = engine.infer()
    
    print("=" * 60)
    print("LOGIC ENGINE TEST RESULTS")
    print("=" * 60)
    
    print(f"\nFacts loaded: {engine.get_stats()['facts']}")
    print(f"Rules available: {engine.get_stats()['rules']}")
    
    print("\nInferences generated:")
    for inf in result['inferences'][:2]:
        print(f"  • {inf['type']}: {inf['conclusion']} (Conf: {inf['confidence']:.2f})")
    
    print(f"\nProcessing: {result['processing_time_ms']}ms")
    print("=" * 60)

if __name__ == "__main__":
    test_logic_engine()
