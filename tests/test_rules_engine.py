"""
Tests for the Rule Engine module.
"""
import pytest
from lrlre.inference.rules_engine import RuleEngine, Rule, Fact, create_default_rules


class TestRuleEngine:
    """Test cases for RuleEngine class."""
    
    def test_init_empty(self):
        """Test engine initialization with no rules."""
        engine = RuleEngine()
        assert len(engine.rules) == 0
        assert len(engine.facts) == 0
    
    def test_init_with_rules(self):
        """Test engine initialization with provided rules."""
        rules = create_default_rules()
        engine = RuleEngine(rules)
        assert len(engine.rules) == len(rules)
    
    def test_add_rule(self):
        """Test adding a rule to the engine."""
        engine = RuleEngine()
        
        def condition(ctx):
            return True
        
        def action(ctx):
            return {'predicate': 'test', 'args': []}
        
        engine.add_rule('test_rule', condition, action, priority=5, description='Test rule')
        
        assert len(engine.rules) == 1
        assert engine.rules[0].name == 'test_rule'
        assert engine.rules[0].priority == 5
    
    def test_add_fact(self):
        """Test adding a fact to the engine."""
        engine = RuleEngine()
        fact = engine.add_fact('knows', ['Alice', 'Bob'], confidence=0.9)
        
        assert len(engine.facts) == 1
        assert fact.predicate == 'knows'
        assert fact.args == ['Alice', 'Bob']
        assert fact.confidence == 0.9
    
    def test_query_facts(self):
        """Test querying facts by predicate."""
        engine = RuleEngine()
        engine.add_fact('knows', ['Alice', 'Bob'])
        engine.add_fact('knows', ['Bob', 'Charlie'])
        engine.add_fact('likes', ['Alice', 'pizza'])
        
        results = engine.query('knows')
        assert len(results) == 2
        
        results = engine.query('likes')
        assert len(results) == 1
    
    def test_forward_chain_symmetric(self):
        """Test forward chaining with symmetric relation rule."""
        engine = RuleEngine(create_default_rules())
        engine.add_fact('knows', ['Alice', 'Bob'], confidence=1.0)
        
        new_facts = engine.forward_chain()
        
        # Should infer Bob knows Alice
        assert len(new_facts) >= 1
        inferred_predicates = [f.predicate for f in new_facts]
        assert 'knows' in inferred_predicates
    
    def test_infer_with_graph_facts(self):
        """Test inference with facts from graph."""
        engine = RuleEngine(create_default_rules())
        
        graph_facts = [
            {'predicate': 'is_a', 'args': ['Dog', 'Mammal'], 'confidence': 0.95},
            {'predicate': 'located_in', 'args': ['Paris', 'France'], 'confidence': 0.9}
        ]
        
        result = engine.infer(graph_facts)
        
        assert 'inferences' in result
        assert 'inference_count' in result
        assert 'processing_time_ms' in result
    
    def test_backward_chain(self):
        """Test backward chaining."""
        engine = RuleEngine(create_default_rules())
        engine.add_fact('knows', ['Alice', 'Bob'])
        
        goal = {'predicate': 'knows', 'args': ['Alice', 'Bob']}
        success, proof_tree = engine.backward_chain(goal)
        
        assert success is True
        assert len(proof_tree) > 0
    
    def test_get_stats(self):
        """Test getting engine statistics."""
        engine = RuleEngine()
        engine.add_fact('test', ['a', 'b'])
        engine.add_fact('test', ['c', 'd'])
        
        stats = engine.get_stats()
        
        assert stats['base_facts'] == 2
        assert stats['rules'] == 0
        assert stats['total_facts'] == 2
    
    def test_clear(self):
        """Test clearing the engine."""
        engine = RuleEngine()
        engine.add_fact('test', ['a'])
        engine.infer()
        
        engine.clear()
        
        assert len(engine.facts) == 0
        assert len(engine.inferred_facts) == 0
    
    def test_rule_priority_ordering(self):
        """Test that rules are sorted by priority."""
        engine = RuleEngine()
        engine.add_rule('low', lambda ctx: True, lambda ctx: None, priority=1)
        engine.add_rule('high', lambda ctx: True, lambda ctx: None, priority=10)
        engine.add_rule('medium', lambda ctx: True, lambda ctx: None, priority=5)
        
        assert engine.rules[0].name == 'high'
        assert engine.rules[1].name == 'medium'
        assert engine.rules[2].name == 'low'
    
    def test_fact_timestamp(self):
        """Test that facts get timestamps."""
        import time
        engine = RuleEngine()
        
        before = time.time()
        fact = engine.add_fact('test', ['value'])
        after = time.time()
        
        assert before <= fact.timestamp <= after


class TestFact:
    """Test cases for Fact dataclass."""
    
    def test_fact_creation(self):
        """Test creating a fact."""
        fact = Fact(predicate='test', args=['a', 'b'])
        
        assert fact.predicate == 'test'
        assert fact.args == ['a', 'b']
        assert fact.confidence == 1.0
        assert fact.source == 'user'
    
    def test_fact_with_confidence(self):
        """Test creating a fact with custom confidence."""
        fact = Fact(predicate='test', args=[], confidence=0.75, source='inferred')
        
        assert fact.confidence == 0.75
        assert fact.source == 'inferred'


class TestCreateDefaultRules:
    """Test cases for default rules creation."""
    
    def test_create_default_rules(self):
        """Test creating default rules."""
        rules = create_default_rules()
        
        assert len(rules) >= 3
        rule_names = [r.name for r in rules]
        assert 'symmetric_relation' in rule_names
        assert 'transitive_location' in rule_names
        assert 'type_inheritance' in rule_names
