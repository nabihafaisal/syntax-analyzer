import re
from SyntaxAnalyzer import SyntaxPhase
#####################LEXICAL################################3
class LexicalError(Exception):
    pass

class Tokenizer:
    @staticmethod
    def new_token_regex(regex):
        newline = r'\n'
        return f'^({regex})$(?!{newline})'

    @staticmethod
    def define_tokens():
        # Define regular expressions for various tokens
        letter = '[a-zA-Z]'
        digit = '[0-9]'
        non_zero_digit = '[1-9]'
        dot = '\.'
        newline = r'\n'
        # Regular expressions for different types of strings
        str_single_quotes = f"'[^'\n]*'?"
        str_double_quotes = f'"[^"\n]*"?'
        str_three_single_quotes = f"'''((?!''').|[\n])*(''')?"
        str_three_double_quotes = f'"""((?!""").|[\n])*(""")?'
        Tokenizer.escapeCodesForString = {"'": "__x20__", '"': "__x21__"}

        # Define Python keywords, operators, and delimiters
        Tokenizer.keywords = [ 'if', 'else', 'for', 'in','range', 'while', 'bool','constant',
         'enum' ]
        Tokenizer.datatypes=['int','float','char','string','bool']
      

        Tokenizer.openbrackets = ['(',  '{',  '[']
        Tokenizer.closebrackets = [')',  '}', ']']
     
        Tokenizer.OOP = ['class', 'private', 'public', 'protected', 'void', 'extends',
       'virtual','override', 'import', 'return', 'sealed', 'abstract','permits', 'this','super', 'static','new']
        Tokenizer.punctuators = [',', ';', ':', '.']
        Tokenizer.PM = ['+', '-']
        Tokenizer.MDM = ['*', '/', '%']
        Tokenizer.logical_operators = ['!', 'and', 'or']
        Tokenizer.assignment = ['=']
        Tokenizer.relational_operators = ['<', '>', '<=', '>=', '!=', '==']
        Tokenizer.assignment_operators = ['+=', '-=', '==', '*=', '%=']
    
        Tokenizer.boolean_constants = ['True', 'False']
        Tokenizer.inc_dec = ['--', '++']

        # Define regular expressions for different tokens
        Tokenizer.identifier = Tokenizer.new_token_regex(f'({letter}|_)({letter}|{digit}|_)*')
        Tokenizer.integer = Tokenizer.new_token_regex(f'{non_zero_digit}{digit}*|0')
        Tokenizer.float = Tokenizer.new_token_regex(f'({digit}+|(?={dot}{digit})){dot}({digit}+|(?<={digit}{dot}))')
        Tokenizer.string = Tokenizer.new_token_regex(f'{str_single_quotes}|{str_double_quotes}|'
                                                     f'{str_three_single_quotes}|{str_three_double_quotes}')
        Tokenizer.comment = Tokenizer.new_token_regex(f'(#[^\n]*)|(/\*([^*]|\*(?!/)|[\n])*(/\*+|//)?|/\*\*/)')
       




    # def __init__(self, file_handler):
    #     self.file_handler = file_handler
    #     self.line_num = 1
    #     self.col_num = 1
    #     self.start_line_num = 1
    #     self.start_col_num = 1
    #     self.token_buffer = ''

    # def increment_pointer(self):
    #     # Move the file pointer to the next character and update line and column numbers
    #     ch = self.file_handler.read(1)
    #     if ch == '\n':
    #         self.line_num += 1
    #         self.col_num = 1
    #     else:
    #         self.col_num += 1
    
    # def get_prev_character(self):
    #     # Get the next character without advancing the file pointer
    #     curr_offset = self.file_handler.tell()
    #     self.file_handler.seek(curr_offset-1)
    #     ch = self.file_handler.read(1)
    #     if (ch == 'd'):
    #         print()
    #     self.file_handler.seek(curr_offset)
    #     return ch

    # def get_next_character(self):
    #     # Get the next character without advancing the file pointer
    #     curr_offset = self.file_handler.tell()
    #     ch = self.file_handler.read(1)
    #     self.file_handler.seek(curr_offset)
    #     return ch

    # def get_next_token(self):
    #     # Initialize token position and type
    #     self.start_line_num = self.line_num
    #     self.start_col_num = self.col_num
    #     token = ''
    #     token_name = ''
    
        
    #     while True:
    #         ch = self.get_next_character()
    #         self.token_buffer += ch

    #         # Check if we have reached the end of the file
    #         if not ch:
    #             if token_name == 'INCOMPLETE STRING':
    #                 raise LexicalError('Incomplete string reached EOF')
    #             return token, token_name
         
            
    #         if self.token_buffer in Tokenizer.OOP:
    #             token = self.token_buffer
    #             token_name = self.token_buffer
    #             self.increment_pointer()
    #             continue

    #         # Compare the token buffer with regular expressions for different tokens
    #         if self.token_buffer in Tokenizer.keywords:
    #             token = self.token_buffer
    #             token_name = self.token_buffer
    #             self.increment_pointer()
    #             continue
    #         if self.token_buffer in Tokenizer.boolean_constants:
    #             token = self.token_buffer
    #             token_name = 'BOOLEAN'
    #             self.increment_pointer()
    #             continue
    #         if self.token_buffer in Tokenizer.logical_operators:
    #             token = self.token_buffer
    #             token_name = self.token_buffer
    #             self.increment_pointer()
    #             continue

    #         if self.token_buffer in Tokenizer.datatypes:
    #             token = self.token_buffer
    #             token_name = 'DT'
    #             self.increment_pointer()
    #             continue
        
      
            

    #         if re.search(Tokenizer.identifier, self.token_buffer):
    #             token = self.token_buffer
    #             token_name = 'ID'
    #             self.increment_pointer()
    #             continue

    #         if re.search(Tokenizer.integer, self.token_buffer):
    #             token = self.token_buffer
    #             token_name = 'INTEGER'
    #             self.increment_pointer()
    #             continue

    #         if re.search(Tokenizer.float, self.token_buffer):
    #             token = self.token_buffer
    #             token_name = 'FLOAT'
    #             self.increment_pointer()
    #             continue
    #         # if re.search(Tokenizer.string, self.token_buffer):
    #         #     if ((ch == '"' or ch == "'") and self.get_prev_character() == '\\'):
    #         #         code = Tokenizer.escapeCodesForString[ch]
    #         #         new_str = ""
    #         #         for i in range(len(self.token_buffer)-2):
    #         #             new_str += self.token_buffer[i]
    #         #         new_str += code
    #         #         self.token_buffer = new_str
    #         #         token = self.token_buffer
    #         #         self.increment_pointer()
    #         #         continue

    #         #     if len(self.token_buffer) >= 2 and self.token_buffer.startswith("'") and self.token_buffer.endswith("'"):
    #         #         if len(self.token_buffer) == 3:# or len(self.token_buffer) == 4:
    #         #             token = self.token_buffer
    #         #             token_name = 'CHARACTER'
    #         #             self.increment_pointer()
    #         #         else:
    #         #             raise LexicalError('Invalid character literal')

    #         #     elif len(self.token_buffer) >= 2 and self.token_buffer.startswith('"') and self.token_buffer.endswith('"'):
    #         #         escaped = False
    #         #         string_content = ''
    #         #         stringWithoutQoutes = self.token_buffer[1:-1]
    #         #         # Exclude the surrounding double quotes
    #         #         for i in range(len(stringWithoutQoutes)):
    #         #             # Exclude the surrounding double quotes
    #         #             ch = stringWithoutQoutes[i]
    #         #             if escaped:
    #         #                 # If we are in an escaped state, add the current character as-is, excluding the backslash
    #         #                 if ch != '\\':
    #         #                     string_content += '\\'
    #         #                 string_content += ch
    #         #                 escaped = False
    #         #             else:
    #         #                 if ch == '\\':
    #         #                     # If we encounter a backslash, set the escaped state
    #         #                     escaped = True
    #         #                     if (i == len(stringWithoutQoutes)-1):
    #         #                         # string_content += "\\"
    #         #                         escaped = not escaped
    #         #                 else:
    #         #                     # Otherwise, add the character to the string content
    #         #                     string_content += ch

    #         #         if not escaped:
    #         #             # If the last character was not part of an escape sequence, the string is complete
    #         #             # Print the string content without the backslash if it's just before the closing quotes
    #         #             keys = list(Tokenizer.escapeCodesForString.keys())
    #         #             values = list(Tokenizer.escapeCodesForString.values())
    #         #             for i in range(len(values)):
    #         #                 value = values[i]
    #         #                 key = keys[i]
    #         #                 string_content = string_content.replace(value, key)
    #         #             token = f'"{string_content}"'
    #         #             token_name = 'STRING'
    #         #             self.increment_pointer()
    #         #             continue

    #         #     elif len(self.token_buffer) >= 2 and self.token_buffer.startswith('"') and self.token_buffer.endswith('"') or \
    #         #             len(self.token_buffer) >= 6 and self.token_buffer.startswith("'''") and self.token_buffer.endswith("'''") or \
    #         #             len(self.token_buffer) >= 6 and self.token_buffer.startswith('"""') and self.token_buffer.endswith('"""'):
    #         #         token = self.token_buffer
    #         #         token_name = 'STRING'
    #         #         self.increment_pointer()
    #         #         continue

    #         #     else:
    #         #         token = self.token_buffer
    #         #         token_name = 'INCOMPLETE STRING'
    #         #         self.increment_pointer()
    #         #         continue

    #         if re.search(Tokenizer.string, self.token_buffer):
    #             if ((ch == '"' or ch == "'") and self.get_prev_character() == '\\'):
    #                 code = Tokenizer.escapeCodesForString[ch]
    #                 new_str = ""
    #                 for i in range(len(self.token_buffer)-2):
    #                     new_str += self.token_buffer[i]
    #                 new_str += code
    #                 self.token_buffer = new_str
    #                 token = self.token_buffer
    #                 self.increment_pointer()
    #                 continue

    #             if len(self.token_buffer) >= 2 and self.token_buffer.startswith("'") and self.token_buffer.endswith("'"):
    #                 if len(self.token_buffer) == 3 or len(self.token_buffer) == 4:
    #                     token = self.token_buffer
    #                     token_name = 'CHARACTER'
    #                     self.increment_pointer()
    #                 else:
    #                      token = self.token_buffer
    #                      token_name = 'Invalid Lexeme'
    #                      self.increment_pointer()
             
    #             if len(self.token_buffer) >=2 and self.token_buffer.startswith("'") and self.token_buffer.endswith("'"):
    #                 if len(self.token_buffer) == 4:
    #                     if self.token_buffer[1] == '\\' and self.token_buffer[2] == 'n':
    #                         token = self.token_buffer
    #                         token_name = 'CHARACTER'
    #                     elif self.token_buffer[1] == '\\' and self.token_buffer[2] == 't':
    #                         token = self.token_buffer
    #                         token_name = 'CHARACTER'
    #                     else:
    #                         token = self.token_buffer
    #                         token_name = 'Invalid Lexeme'
    #                 elif len(self.token_buffer) == 3 :
    #                     token = self.token_buffer
    #                     token_name = 'CHARACTER'
    #                     self.increment_pointer()
                    
    #                 else:
    #                     token = self.token_buffer
    #                     token_name = 'Invalid Lexeme'
    #                 self.increment_pointer()
    #             elif():
    #                 token = self.token_buffer
    #                 token_name = 'Invalid Lexeme'
    #                 self.increment_pointer()




    #             elif len(self.token_buffer) >= 2 and self.token_buffer.startswith('"') and self.token_buffer.endswith('"'):
    #                 escaped = False
    #                 string_content = ''
    #                 stringWithoutQoutes = self.token_buffer[1:-1]
    #                 # Exclude the surrounding double quotes
    #                 for i in range(len(stringWithoutQoutes)):
    #                     # Exclude the surrounding double quotes
    #                     ch = stringWithoutQoutes[i]
    #                     if escaped:
    #                         # If we are in an escaped state, add the current character as-is, excluding the backslash
    #                         if ch != '\\':
    #                             string_content += '\\'
    #                         string_content += ch
    #                         escaped = False
    #                     else:
    #                         if ch == '\\':
    #                             # If we encounter a backslash, set the escaped state
    #                             escaped = True
    #                             if (i == len(stringWithoutQoutes)-1):
    #                                 # string_content += "\\"
    #                                 escaped = not escaped
    #                         else:
    #                             # Otherwise, add the character to the string content
    #                             string_content += ch

    #                 if not escaped:
    #                     # If the last character was not part of an escape sequence, the string is complete
    #                     # Print the string content without the backslash if it's just before the closing quotes
    #                     keys = list(Tokenizer.escapeCodesForString.keys())
    #                     values = list(Tokenizer.escapeCodesForString.values())
    #                     for i in range(len(values)):
    #                         value = values[i]
    #                         key = keys[i]
    #                         string_content = string_content.replace(value, key)
    #                     token = f'"{string_content}"'
    #                     token_name = 'STRING'
    #                     self.increment_pointer()
    #                     continue

    #             elif len(self.token_buffer) >= 2 and self.token_buffer.startswith('"') and self.token_buffer.endswith('"') or \
    #                     len(self.token_buffer) >= 6 and self.token_buffer.startswith("'''") and self.token_buffer.endswith("'''") or \
    #                     len(self.token_buffer) >= 6 and self.token_buffer.startswith('"""') and self.token_buffer.endswith('"""'):
    #                 token = self.token_buffer
    #                 token_name = 'STRING'
    #                 self.increment_pointer()
    #                 continue

    #             else:
    #                 token = self.token_buffer
    #                 token_name = 'INVALID  LEXEME'
    #                 self.increment_pointer()
    #                 continue



    #         if re.search(Tokenizer.comment, self.token_buffer) or (self.token_buffer.startswith('/*') and self.token_buffer.endswith('*/')):
    #             token = self.token_buffer
    #             token_name = 'COMMENT'
    #             self.increment_pointer()
    #             continue

    #         if self.token_buffer in Tokenizer.openbrackets:
    #             token = self.token_buffer
    #             token_name = self.token_buffer
    #             self.increment_pointer()
    #             continue

    #         if self.token_buffer in Tokenizer.closebrackets:
    #             token = self.token_buffer
    #             token_name = self.token_buffer
    #             self.increment_pointer()
    #             continue

    #         if self.token_buffer in Tokenizer.PM:
    #             token = self.token_buffer
    #             token_name = 'PM'
    #             self.increment_pointer()
    #             continue

    #         if self.token_buffer in Tokenizer.MDM:
    #             token = self.token_buffer
    #             token_name = 'MDM'
    #             self.increment_pointer()
    #             continue

    #         if self.token_buffer in Tokenizer.punctuators:
    #             token = self.token_buffer
    #             token_name = 'PUNCTUATOR'
    #             self.increment_pointer()
    #             continue

    #         if self.token_buffer in Tokenizer.assignment:
    #             token = self.token_buffer
    #             token_name = 'Assignment'
    #             self.increment_pointer()
    #             continue

            
            
    #         if self.token_buffer in Tokenizer.relational_operators:
    #             token = self.token_buffer
    #             token_name = 'ROP'
    #             self.increment_pointer()
    #             continue

    #         if self.token_buffer in Tokenizer.assignment_operators:
    #             token = self.token_buffer
    #             token_name = 'ASSIGNMENT_OPERATOR'
    #             self.increment_pointer()
    #             continue

    #         if self.token_buffer in Tokenizer.inc_dec:
    #             token = self.token_buffer
    #             token_name = 'INCREMENT_DECREMENT'
    #             self.increment_pointer()
    #             continue
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.line_num = 1
        self.col_num = 1
        self.start_line_num = 1
        self.start_col_num = 1
        self.token_buffer = ''

    def increment_pointer(self):
        # Move the file pointer to the next character and update line and column numbers
        ch = self.file_handler.read(1)
        if ch == '\n':
            self.line_num += 1
            self.col_num = 1
        else:
            self.col_num += 1

    def get_next_character(self):
        # Get the next character without advancing the file pointer
        curr_offset = self.file_handler.tell()
        ch = self.file_handler.read(1)
        if (ch == 'd'):
            print()
        self.file_handler.seek(curr_offset)
        return ch

    def get_prev_character(self):
        # Get the next character without advancing the file pointer
        curr_offset = self.file_handler.tell()
        self.file_handler.seek(curr_offset-1)
        ch = self.file_handler.read(1)
        if (ch == 'd'):
            print()
        self.file_handler.seek(curr_offset)
        return ch

    def get_next_token(self):
        # Initialize token position and type
        self.start_line_num = self.line_num
        self.start_col_num = self.col_num
        token = ''
        token_name = ''

        while True:
            ch = self.get_next_character()
            self.token_buffer += ch

            # Check if we have reached the end of the file
            if not ch:
                if token_name == 'INCOMPLETE STRING':
                    raise LexicalError('Incomplete string reached EOF')
                return token, token_name

            if self.token_buffer in Tokenizer.OOP:
                token = self.token_buffer
                token_name = self.token_buffer
                self.increment_pointer()
                continue
                

            if self.token_buffer in Tokenizer.datatypes:
                token = self.token_buffer
                token_name = 'DT'
                self.increment_pointer()
                continue

            # Compare the token buffer with regular expressions for different tokens
            if self.token_buffer in Tokenizer.keywords:
                token = self.token_buffer
                token_name = self.token_buffer
                self.increment_pointer()
                continue

            if re.search(Tokenizer.identifier, self.token_buffer):
                token = self.token_buffer
                token_name = 'ID'
                self.increment_pointer()
                continue

            if re.search(Tokenizer.integer, self.token_buffer):
                token = self.token_buffer
                token_name = 'INTEGER'
                self.increment_pointer()
                continue

            if re.search(Tokenizer.float, self.token_buffer):
                token = self.token_buffer
                token_name = 'FLOAT'
                self.increment_pointer()
                continue

            if re.search(Tokenizer.string, self.token_buffer):
                if ((ch == '"' or ch == "'") and self.get_prev_character() == '\\'):
                    code = Tokenizer.escapeCodesForString[ch]
                    new_str = ""
                    for i in range(len(self.token_buffer)-2):
                        new_str += self.token_buffer[i]
                    new_str += code
                    self.token_buffer = new_str
                    token = self.token_buffer
                    self.increment_pointer()
                    continue

                if len(self.token_buffer) >= 2 and self.token_buffer.startswith("'") and self.token_buffer.endswith("'"):
                    if len(self.token_buffer) == 3:# or len(self.token_buffer) == 4:
                        token = self.token_buffer
                        token_name = 'CHARACTER'
                        self.increment_pointer()
                    else:
                        raise LexicalError('Invalid character literal')

                elif len(self.token_buffer) >= 2 and self.token_buffer.startswith('"') and self.token_buffer.endswith('"'):
                    escaped = False
                    string_content = ''
                    stringWithoutQoutes = self.token_buffer[1:-1]
                    # Exclude the surrounding double quotes
                    for i in range(len(stringWithoutQoutes)):
                        # Exclude the surrounding double quotes
                        ch = stringWithoutQoutes[i]
                        if escaped:
                            # If we are in an escaped state, add the current character as-is, excluding the backslash
                            if ch != '\\':
                                string_content += '\\'
                            string_content += ch
                            escaped = False
                        else:
                            if ch == '\\':
                                # If we encounter a backslash, set the escaped state
                                escaped = True
                                if (i == len(stringWithoutQoutes)-1):
                                    # string_content += "\\"
                                    escaped = not escaped
                            else:
                                # Otherwise, add the character to the string content
                                string_content += ch

                    if not escaped:
                        # If the last character was not part of an escape sequence, the string is complete
                        # Print the string content without the backslash if it's just before the closing quotes
                        keys = list(Tokenizer.escapeCodesForString.keys())
                        values = list(Tokenizer.escapeCodesForString.values())
                        for i in range(len(values)):
                            value = values[i]
                            key = keys[i]
                            string_content = string_content.replace(value, key)
                        token = f'"{string_content}"'
                        token_name = 'STRING'
                        self.increment_pointer()
                        continue

                elif len(self.token_buffer) >= 2 and self.token_buffer.startswith('"') and self.token_buffer.endswith('"') or \
                        len(self.token_buffer) >= 6 and self.token_buffer.startswith("'''") and self.token_buffer.endswith("'''") or \
                        len(self.token_buffer) >= 6 and self.token_buffer.startswith('"""') and self.token_buffer.endswith('"""'):
                    token = self.token_buffer
                    token_name = 'STRING'
                    self.increment_pointer()
                    continue

                else:
                    token = self.token_buffer
                    token_name = 'INCOMPLETE STRING'
                    self.increment_pointer()
                    continue

            if re.search(Tokenizer.comment, self.token_buffer):
                token = self.token_buffer
                token_name = 'COMMENT'
                self.increment_pointer()
                continue
            if self.token_buffer in Tokenizer.openbrackets:
                token = self.token_buffer
                token_name = self.token_buffer
                self.increment_pointer()
                continue
            if self.token_buffer in Tokenizer.closebrackets:
                token = self.token_buffer
                token_name = self.token_buffer
                self.increment_pointer()
                continue
            if self.token_buffer in Tokenizer.PM:
                token = self.token_buffer
                token_name = 'PM'
                self.increment_pointer()
                continue
            if self.token_buffer in Tokenizer.MDM:
                token = self.token_buffer
                token_name = 'MDM'
                self.increment_pointer()
                continue

            if self.token_buffer in Tokenizer.punctuators:
                token = self.token_buffer
                token_name = 'PUNCTUATOR'
                self.increment_pointer()
                continue
            if self.token_buffer in Tokenizer.assignment:
                token = self.token_buffer
                token_name = 'assignment'
                self.increment_pointer()
                continue
            if self.token_buffer in Tokenizer.logical_operators:
                token = self.token_buffer
                token_name = 'LOGICAL_OPERATOR'
                self.increment_pointer()
                continue
            if self.token_buffer in Tokenizer.assignment_operators:
                token = self.token_buffer
                token_name = 'ASSIGNMENT_OPERATOR'
                self.increment_pointer()
                continue
            if self.token_buffer in Tokenizer.inc_dec:
                token = self.token_buffer
                token_name = 'INCREMENT_DECREMENT'
                self.increment_pointer()
                continue
            if self.token_buffer in Tokenizer.boolean_constants:
                token = self.token_buffer
                token_name = 'BOOLEAN_CONSTANT'
                self.increment_pointer()
                continue
            if self.token_buffer in Tokenizer.relational_operators:
                token = self.token_buffer
                token_name = 'ROP'
                self.increment_pointer()
                continue
            
            

            # Check for lexical errors
            if token_name == 'INTEGER':
                if re.search('[a-zA-Z]', ch):
                    token = self.token_buffer
                    token_name = 'Invalid'
                    self.increment_pointer()

            if token_name == 'FLOAT':
                if re.search('[a-zA-Z]', ch):
                    token = self.token_buffer
                    token_name = 'Invalid'
                    self.increment_pointer()

            if token_name == 'INCOMPLETE STRING':
                if ch == '\n' and len(self.token_buffer) >= 3:
                    token = self.token_buffer
                    token_name = 'Invalid'
                    self.increment_pointer()

            # If there is no lexical error, return the token formed so far without consuming the current character
            self.token_buffer = ''
            return token, token_name
    def tokenize_input(self):
        # Tokenize the input
        tokens = []
        while True:
            try:
                while re.search('\s', t.get_next_character()):
                    self.increment_pointer()

                ch = t.get_next_character()

                if not ch:
                    # Add the end-of-input token
                    tokens.append(("$", "$" ,t.start_line_num+1))
                    return tokens

                token, token_name = t.get_next_token()
            
                tokens.append((token_name, token,t.start_line_num))
            except LexicalError as e:
                print(f'Lexical error: {e} - Line: {t.start_line_num} - Column: {t.start_col_num}')
                t.token_buffer = ''





  






if __name__ == '__main__':
    # Define the regular OEressions for tokens
    Tokenizer.define_tokens()

    with open('tokens.txt') as file_handler:
        t = Tokenizer(file_handler)
        tokens=t.tokenize_input()
        for token_name, token, start_line_num in tokens:
               print(f"({token_name}, {token} , {start_line_num})\n")
syntax_phase = SyntaxPhase(tokens)
some_link = syntax_phase.semantic.create_DT()
syntax_phase.run()

    

# syntax_phase.format_function_table()
# syntax_phase.format_class_table()
# syntax_phase.format_body_table(some_link) 

# # Display the formatted function table
# print("Function Table:")
# print(syntax_phase.formated_function[0])          


# print("Class Table:")
# print(syntax_phase.formated_function[1])

# print("Body Table:")
# print(syntax_phase.formated_function[2])   
       
   
