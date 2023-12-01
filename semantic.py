class SemanticAnalyzer:
    def __init__(self, syntax_phase):
        self.tokens = syntax_phase.tokens
        self.index = 0
        self.MDTA = []
        self.FDTA = []
        self.CDTA = []
        self.Scope_Stack = []

    def run_semantic_analysis(self):
        # Start the semantic analysis
        self.semantic_analysis()

    def semantic_analysis(self):
        # Iterate through the syntax tree and perform semantic analysis
        while self.index < len(self.tokens):
            token_name, token, start_line_num = self.tokens[self.index]
            
            # Check for function or class declarations
            if token_name == 'DT' and self.tokens[self.index + 1][0] == 'ID':
                self.handle_declaration()

            # Check for other semantic rules as needed

            # Move to the next token
            self.index += 1

    def handle_declaration(self):
        # Handle variable or function declaration
        data_type = self.tokens[self.index][1]
        identifier = self.tokens[self.index + 1][1]

        # Check for function declaration
        if self.tokens[self.index + 2][1] == '(':
            self.handle_function_declaration(data_type, identifier)
        else:
            self.handle_variable_declaration(data_type, identifier)

    def handle_function_declaration(self, data_type, identifier):
        # Handle function declaration
        # You may want to add the function details to your function table (FDTA)
        # Example:
        function_details = {'Name': identifier, 'Type': data_type}
        self.FDTA.append(function_details)

        # Move to the next token after the function declaration
        # (Skip the function parameters for simplicity in this example)
        while self.tokens[self.index][1] != ')':
            self.index += 1
        self.index += 1  # Move past ')'

    def handle_variable_declaration(self, data_type, identifier):
        # Handle variable declaration
        # You may want to add the variable details to your symbol table
        # Example:
        variable_details = {'Name': identifier, 'Type': data_type}
        self.CDTA.append(variable_details)
