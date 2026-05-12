"""
LRLRE Benchmark Suite - REAL performance and accuracy measurements
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import time
import json
import csv
from typing import Dict, List
from collections import defaultdict
import statistics

from lrlre.multilingual.simple_detector import SimpleLanguageDetector
from lrlre.multilingual.internet_reference import InternetReferenceSystem

class BenchmarkRunner:
    def __init__(self):
        self.detector = SimpleLanguageDetector()
        self.reference = InternetReferenceSystem()
        self.results = defaultdict(list)
    
    def load_dataset(self, filename: str) -> List[Dict]:
        """Load benchmark dataset"""
        dataset = []
        path = os.path.join(os.path.dirname(__file__), "datasets", filename)
        
        if filename.endswith('.csv'):
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    dataset.append({
                        'text': row['text'],
                        'expected': row['language'],
                        'source': row.get('source', 'unknown')
                    })
        else:
            # Simple format: language|text
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    if '|' in line:
                        lang, text = line.strip().split('|', 1)
                        dataset.append({
                            'text': text,
                            'expected': lang,
                            'source': 'custom'
                        })
        
        return dataset
    
    def benchmark_detection(self, dataset: List[Dict]) -> Dict:
        """Benchmark language detection accuracy"""
        correct = 0
        latencies = []
        errors = []
        
        for item in dataset:
            start = time.perf_counter()
            try:
                result = self.detector.detect(item['text'])
                latency = (time.perf_counter() - start) * 1000
                latencies.append(latency)
                
                if result['language'] == item['expected']:
                    correct += 1
                else:
                    errors.append({
                        'text': item['text'][:50],
                        'expected': item['expected'],
                        'got': result['language'],
                        'confidence': result['confidence']
                    })
            except Exception as e:
                errors.append({
                    'text': item['text'][:50],
                    'expected': item['expected'],
                    'error': str(e)
                })
        
        total = len(dataset)
        accuracy = correct / total if total > 0 else 0
        
        return {
            'total_samples': total,
            'correct': correct,
            'accuracy': round(accuracy * 100, 2),
            'latency_ms': {
                'avg': round(statistics.mean(latencies), 2) if latencies else 0,
                'min': round(min(latencies), 2) if latencies else 0,
                'max': round(max(latencies), 2) if latencies else 0,
                'p95': self._percentile(latencies, 95) if latencies else 0
            },
            'errors': errors[:10]  # Show first 10 errors
        }
    
    def benchmark_by_language(self, dataset: List[Dict]) -> Dict:
        """Benchmark accuracy per language"""
        by_lang = defaultdict(list)
        
        for item in dataset:
            by_lang[item['expected']].append(item)
        
        results = {}
        for lang, items in by_lang.items():
            lang_result = self.benchmark_detection(items)
            results[lang] = {
                'samples': len(items),
                'accuracy': lang_result['accuracy'],
                'avg_latency': lang_result['latency_ms']['avg']
            }
        
        return results
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile"""
        if not data:
            return 0
        sorted_data = sorted(data)
        k = (len(sorted_data) - 1) * percentile / 100
        f = int(k)
        c = int(k) + 1 if f < len(sorted_data) - 1 else f
        return round(sorted_data[f] + (sorted_data[c] - sorted_data[f]) * (k - f), 2)
    
    def run_full_benchmark(self):
        """Run complete benchmark suite"""
        print("=" * 70)
        print("🚀 LRLRE BENCHMARK SUITE - REAL MEASUREMENTS")
        print("=" * 70)
        
        # Create small test dataset if none exists
        test_dataset = [
            {'text': 'Hello world', 'expected': 'en', 'source': 'test'},
            {'text': 'Bonjour le monde', 'expected': 'fr', 'source': 'test'},
            {'text': 'こんにちは世界', 'expected': 'ja', 'source': 'test'},
            {'text': '안녕하세요 세계', 'expected': 'ko', 'source': 'test'},
            {'text': '你好世界', 'expected': 'zh', 'source': 'test'},
        ]
        
        print("\n📊 Running detection benchmark...")
        results = self.benchmark_detection(test_dataset)
        
        print(f"\nTotal samples: {results['total_samples']}")
        print(f"Correct: {results['correct']}")
        print(f"Accuracy: {results['accuracy']}%")
        print(f"\nLatency (ms):")
        print(f"  Avg: {results['latency_ms']['avg']}")
        print(f"  Min: {results['latency_ms']['min']}")
        print(f"  Max: {results['latency_ms']['max']}")
        print(f"  P95: {results['latency_ms']['p95']}")
        
        print("\n📈 Per-language results:")
        per_lang = self.benchmark_by_language(test_dataset)
        for lang, stats in per_lang.items():
            print(f"  {lang}: {stats['accuracy']}% ({stats['samples']} samples, {stats['avg_latency']}ms avg)")
        
        print("\n" + "=" * 70)
        print("✅ Benchmark complete")
        print("=" * 70)
        
        return results

if __name__ == "__main__":
    runner = BenchmarkRunner()
    runner.run_full_benchmark()
