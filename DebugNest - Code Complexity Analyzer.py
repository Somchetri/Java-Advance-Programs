import ast
import sys

class ComplexityAnalyzer:
    def __init__(self, threshold=10):
        self.threshold = threshold
        self.results = []
    
    def calculate_complexity(self, node):
        """Calculate cyclomatic complexity of a function"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity
    
    def analyze_file(self, code):
        """Analyze Python code and return complexity metrics"""
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return [{'error': f'Syntax Error: {e}'}]
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self.calculate_complexity(node)
                status = '⚠️ HIGH' if complexity > self.threshold else '✅ OK'
                
                self.results.append({
                    'function': node.name,
                    'line': node.lineno,
                    'complexity': complexity,
                    'status': status
                })
        
        return self.results
    
    def generate_report(self):
        """Generate a formatted complexity report"""
        if not self.results:
            return "No functions found to analyze."
        
        print("\n" + "="*60)
        print("CODE COMPLEXITY ANALYSIS REPORT")
        print("="*60 + "\n")
        
        for result in sorted(self.results, key=lambda x: x['complexity'], reverse=True):
            print(f"{result['status']} Function: {result['function']}")
            print(f"   Line: {result['line']} | Complexity: {result['complexity']}")
            if result['complexity'] > self.threshold:
                print(f"   💡 Suggestion: Consider refactoring to reduce complexity")
            print()

# Usage
sample_code = """
def complex_function(x, y, z):
    if x > 0:
        if y > 0:
            if z > 0:
                for i in range(10):
                    if i % 2 == 0:
                        print(i)
                    else:
                        continue
            else:
                return False
        elif y < 0:
            return None
    else:
        while x < 10:
            x += 1
    return True

def simple_function(a, b):
    return a + b
"""

analyzer = ComplexityAnalyzer(threshold=5)
analyzer.analyze_file(sample_code)
analyzer.generate_report()
