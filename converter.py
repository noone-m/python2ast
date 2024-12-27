

import sys
import subprocess
import ast
from graphviz import Digraph

class ASTVisualizer(ast.NodeVisitor):
    def __init__(self):
        self.graph = Digraph(format='png')
        self.node_id = 0
    
    def visit(self, node):
        node_id = self.node_id
        self.node_id += 1
        
        # Add the current node to the graph
        label = node.__class__.__name__
        self.graph.node(str(node_id), label)
        
        # Connect the current node to its children
        for child in ast.iter_child_nodes(node):
            child_id = self.visit(child)
            self.graph.edge(str(node_id), str(child_id))
        
        return node_id

def generate_ast_dot_file(source_code, output_dot_file):
    tree = ast.parse(source_code)
    visualizer = ASTVisualizer()
    visualizer.visit(tree)
    visualizer.graph.save(output_dot_file)
    print(f"Saved AST .dot file to {output_dot_file}")



# print(sys.argv) ['e:/deeplearning_course_notebooks/python2ast/converter.py', 'arg1']
if len(sys.argv) != 2:
    print("Usage: python converter.py <file_name.py> ")
    sys.exit(1)
file_name = sys.argv[1]
file_content = open(file_name,'r')
file_content = file_content.read()

generate_ast_dot_file(file_content, 'ast.dot')
command = ['dot', '-Tpng', 'ast.dot', '-o', 'ast.png']
result = subprocess.run(command, capture_output=True, text=True)
 # Check for errors 
if result.returncode != 0: 
    print("Error:", result.stderr) 
else:
    print("Generated ast.png successfully.")