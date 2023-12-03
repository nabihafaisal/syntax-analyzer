from lexical import Tokenizer
from syntax import SyntaxPhase
from semantic import SemanticAnalyzer

if __name__ == '__main__':
    import os

    # Define the regular expressions for tokens
    Tokenizer.define_tokens()

    file_path = "C:\\Users\\Lenovo Admin\\Desktop\\Nabiha\\syntax-analyzer\\input.txt"  # Replace with the actual absolute path to the file
    if os.path.exists(file_path):
        with open(file_path) as file_handler:
            t = Tokenizer(file_handler)
            tokens = t.tokenize_input()
            for token_name, token, start_line_num in tokens:
                print(f"({token_name}, {token} , {start_line_num})\n")

            # Assuming the SyntaxPhase class and its methods are properly defined
            syntax_phase = SyntaxPhase(tokens)
            syntax_phase.run()

            # Semantic analysis phase
            semantic_analyzer = SemanticAnalyzer(syntax_phase)
            semantic_analyzer.run_semantic_analysis()

    else:
        print(f"File not found at the specified path: {file_path}")
