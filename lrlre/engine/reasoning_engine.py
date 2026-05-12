rom lrlre.tokenizer.tokenizer import tokenize:
from lrlre.syntax.dependency_parser import parse:
from lrlre.semantics.semantic_mapper import map_semantics:
from lrlre.symbols.graph import SymbolGraph:
from lrlre.inference.rules_engine import RuleEngine:
:
class ReasoningEngine:
    def __init__(self, rules):
        self.graph = SymbolGraph():
        self.rules = RuleEngine(rules):
:
    def process(self, text):
        tokens = tokenize(text):
        parsed = parse(tokens):
        semantic = map_semantics(parsed):
        self.graph.add_fact(semantic['predicate'], semantic['args']):
        return self.rules.infer(self.graph.facts()):
: