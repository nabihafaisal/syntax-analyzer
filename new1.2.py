import re

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
       'virtual','override', 'import', 'new', 'return', 'sealed', 'abstract','permits', 'this','super' ,'const','static']
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
    
    def get_prev_character(self):
        # Get the next character without advancing the file pointer
        curr_offset = self.file_handler.tell()
        self.file_handler.seek(curr_offset-1)
        ch = self.file_handler.read(1)
        if (ch == 'd'):
            print()
        self.file_handler.seek(curr_offset)
        return ch

    def get_next_character(self):
        # Get the next character without advancing the file pointer
        curr_offset = self.file_handler.tell()
        ch = self.file_handler.read(1)
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

            # Compare the token buffer with regular expressions for different tokens
            if self.token_buffer in Tokenizer.keywords:
                token = self.token_buffer
                token_name = self.token_buffer
                self.increment_pointer()
                continue

            if self.token_buffer in Tokenizer.datatypes:
                token = self.token_buffer
                token_name = 'DT'
                self.increment_pointer()
                continue

            if self.token_buffer in Tokenizer.logical_operators:
                token = self.token_buffer
                token_name = self.token_buffer
                self.increment_pointer()
                continue

            if self.token_buffer in Tokenizer.boolean_constants:
                token = self.token_buffer
                token_name = 'BOOLEAN'
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
                    if len(self.token_buffer) == 3 or len(self.token_buffer) == 4:
                        token = self.token_buffer
                        token_name = 'CHARACTER'
                        self.increment_pointer()
                    else:
                         token = self.token_buffer
                         token_name = 'Invalid Lexeme'
                         self.increment_pointer()
             
                if len(self.token_buffer) >=2 and self.token_buffer.startswith("'") and self.token_buffer.endswith("'"):
                    if len(self.token_buffer) == 4:
                        if self.token_buffer[1] == '\\' and self.token_buffer[2] == 'n':
                            token = self.token_buffer
                            token_name = 'CHARACTER'
                        elif self.token_buffer[1] == '\\' and self.token_buffer[2] == 't':
                            token = self.token_buffer
                            token_name = 'CHARACTER'
                        else:
                            token = self.token_buffer
                            token_name = 'Invalid Lexeme'
                    elif len(self.token_buffer) == 3 :
                        token = self.token_buffer
                        token_name = 'CHARACTER'
                        self.increment_pointer()
                    
                    else:
                        token = self.token_buffer
                        token_name = 'Invalid Lexeme'
                    self.increment_pointer()
                elif():
                    token = self.token_buffer
                    token_name = 'Invalid Lexeme'
                    self.increment_pointer()




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
                    token_name = 'INVALID  LEXEME'
                    self.increment_pointer()
                    continue



            if re.search(Tokenizer.comment, self.token_buffer) or (self.token_buffer.startswith('/*') and self.token_buffer.endswith('*/')):
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
                token_name = 'punctuators'
                self.increment_pointer()
                continue

            if self.token_buffer in Tokenizer.assignment:
                token = self.token_buffer
                token_name = 'Assignment'
                self.increment_pointer()
                continue



            if self.token_buffer in Tokenizer.relational_operators:
                token = self.token_buffer
                token_name = 'ROP'
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
                token_name = 'BOOLEAN'
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
             
# ... (your Tokenizer class and main code)

class SyntaxPhase:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def run(self):
        if self.S():
            if self.tokens[self.index][0] == "$":
                print("No Syntax Error  :)")
                
            else:
                print(f"  :(   Syntax Error At Line No.: {self.tokens[self.index][2]} {self.tokens[self.index][0]}")
        else:
            print(f"  :(   Syntax Error At Line No.: {self.tokens[self.index][2]} {self.tokens[self.index][0]}")

   
    #DECLARATION
    def dec(self):
        if (
            self.tokens[self.index][0] == "DT"
            and self.tokens[self.index + 1][0] == "ID"
        ):
            self.index += 2
            if self.init():
                if self.list():
                    return True
        return False

    def dec2(self):
        if self.tokens[self.index][1] in ["=", ",", ";"]:
            if self.init():
                print("param1 passed")
                if self.list():
                    return True
        return False

    def init(self):
        if self.tokens[self.index][1] == "=":
            self.index += 1
            if self.OE():
                return True
          
        elif self.tokens[self.index][1] in [";", ","]:
            return True
        return False

    def fs(self):
        if self.tokens[self.index][0] == "static":
            self.index += 1
       
        elif self.tokens[self.index][0] == "DT":
            self.index += 1
        return False

    def list(self):
        if self.tokens[self.index][1] == ";":
            self.index += 1
            return True
        elif (
            self.tokens[self.index][1] == ","
            and self.tokens[self.index + 1][0] == "ID"
        ):
            self.index += 2
            if self.dec2():
                return True
        return False
     #BODY
    def body(self):
        if self.tokens[self.index][1] == "{":
            self.index += 1
            if self.MST():
                if self.tokens[self.index][1] == "}":
                    self.index += 1
                    return True
        return False
    def MST(self):
        if (
            self.tokens[self.index][0] in ["if", "while", "else", "for","this","super","ID","return","DT"]
        
        ):
            if self.SST():
                # print("token", self.tokens[self.index][1])
                return True
            if self.MST():
                return True
        elif self.tokens[self.index][1] == "}":
            return True
        return False

    def SST(self):
        if (
            self.tokens[self.index][0] in [
                "for",
                "while",
                "class",
                "if",

                "return",
                
                "DT",
                "void",
                "ID",
                "this",
                "super"
            ]
          
        ):
            if self.tokens[self.index][0] == "if":
                if self.if_else():
                    return True

                 
            elif self.tokens[self.index][0] == "while":
                if self.while_state():
                    return True
            
                       
            elif self.tokens[self.index][0] == "for":
                if self.for_loop():
                    return True
            elif self.tokens[self.index][0] == "return":
                if self.return_state():
                    return True
          
            elif self.tokens[self.index][0] in ["this", "super"]:
                if self.ts():
                    return True
            elif self.tokens[self.index][0] == "DT":
                self.index += 1
                if self.SST2():
                    return True
            
            elif self.tokens[self.index][0] == "void" and self.tokens[self.index+1][0] == "ID":
                self.index += 2
                if self.Function():
                    return True
                        
            elif self.tokens[self.index][0] == "ID":
                self.index += 1
                if self.SST1():
                    return True
            
            if self.tokens[self.index][0] == "class":
                if self.class_body():
                    return True          
        return False

    def obj2(self):
        if self.tokens[self.index][1] == "=":
            self.index += 1
            if self.tokens[self.index][0] == "new":
                self.index += 1
                if self.tokens[self.index][0] == "ID":
                    self.index += 1
                    if self.tokens[self.index][1] == "(":
                        self.index += 1
                        if self.arg():
                            if self.tokens[self.index][1] == ")":
                                self.index += 1
                                if self.tokens[self.index][1] == ";":
                                    self.index += 1
                                    return True
        return False

    def SST1(self):
        if (
            self.tokens[self.index][0] == "ID"
            or self.tokens[self.index][1] == "("
            or self.tokens[self.index][1] == "["
           
            or self.tokens[self.index][1] == "."
            or self.tokens[self.index][1] == "="
        ):
            if self.tokens[self.index][0] == "ID":
                self.index += 1
                if self.obj2():
                    return True
            elif self.pl():
                if self.tokens[self.index][1] == "=":
                    self.index += 1
                    if self.OE():
                        if self.tokens[self.index][1] == ";":
                            self.index += 1
                            return True
        return False

    def SST2(self):
        if self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.dec2():
                return True
            elif self.Function():
                return True    
            

        elif self.tokens[self.index][1] == "[":
            self.index += 1
            if self.tokens[self.index][1] == "]":
                self.index += 1
                if self.br():
                    if self.tokens[self.index][0] == "ID":
                        self.index += 1
                        if self.Arraydef():
                            if self.tokens[self.index][1] == ";":
                                self.index += 1
                                return True
        return False
     #FOR-LOOP
    def for_loop(self):
        if self.tokens[self.index][0] == "for":
            self.index += 1
            if self.tokens[self.index][0] == "ID":
                self.index += 1
                if self.tokens[self.index][0] == "in":
                    self.index += 1
                    if self.tokens[self.index][0] == "range":
                        self.index += 1
                        if self.tokens[self.index][1] == "(":
                            self.index += 1
                            if self.OE():
                                if self.tokens[self.index][1] == ")":
                                    self.index += 1
                                    if self.tokens[self.index][1] == ":":
                                        self.index += 1
                                        if self.body():
                                            return True
        return False
    def while_state(self):
        if self.tokens[self.index][0] == "while":
            self.index += 1
            if self.tokens[self.index][1] == "(":
                self.index += 1

                if self.OE():
                    if self.tokens[self.index][1] == ")":
                        self.index += 1

                        if self.body():
                            return True

        return False
    # IF-ELSE
    def if_else(self):
        if self.tokens[self.index][0] == "if":
            self.index += 1
            if self.tokens[self.index][1] == "(":
                self.index += 1
                if self.OE():
                    if self.tokens[self.index][1] == ")":
                        self.index += 1
                        if self.body():
                            if self.else_state():
                                return True
        return False
    def else_state(self):
        if self.tokens[self.index][0] == "else":
            self.index += 1
            if self.body():
                return True
        elif (
            self.tokens[self.index][0] in [
                "this", "super", "ID", "DT", "if", "while",
                 "for", "return",
                "}"
            ]
        ):
            return True
        return False
    #------------------------------------ class body------------------------------------------
    def class_body(self):
        if self.tokens[self.index][0] =='class':
            self.index += 1
            if self.tokens[self.index][0] =='ID':
                self.index += 1
                if self.tokens[self.index][0] =='{':
                    self.index += 1
                
                    if self.class_body1 ():
                        return True
                        
                    if self.tokens[self.index][0] =='}':
                        self.index += 1
                        return True
    
    def mode_inheritance(self):
        if self.tokens[self.index][0] == "class":
            self.index += 1
            if self.tokens[self.index][0] == "ID":
                self.index += 1
                if self.tokens[self.index][1] == ":":
                    self.index += 1
                    if self.access_modifier():
                        if self.tokens[self.index][0] == "ID":
                            self.index += 1
                            if self.tokens[self.index][1] == "{":
                                self.index += 1
                                if self.class_body():
                                    if self.tokens[self.index][1] == "}":
                                        self.index += 1
                                        if self.tokens[self.index][1] == ";":
                                            self.index += 1
                                            return True
        return False

        
    def access_modifier(self):
        if self.tokens[self.index][0] in ["public", "private", "protected"]:
            self.index += 1
            if self.tokens[self.index][1] == ":":
                self.index += 1
            return True
        return False
    def class_body1(self):
        
        if self.dec():
            if self.class_body1():
                   return True
        elif self.access_modifier():
            if self.dec():
                if self.class_modifier():
                    if self.class_body1():
                        return True            
            
        elif self.SST():
            if self.class_body1():
                   return True              



        return False   

    def class_modifier(self):
        if self.tokens[self.index][0] in ["static", "virtual", "const"]:
            self.index += 1
            return True
        return False
    # RETURN

    def return_state(self):
        if self.tokens[self.index][0] == "return":
            self.index += 1
            if self.return_state1():
                return True
        return False

    def return_state1(self):
        if self.tokens[self.index][1] == ";":
            self.index += 1
            return True
        elif self.OE():
            if self.tokens[self.index][1] == ";":
                self.index += 1
                return True
        return False
    #TS
    def ts(self):
        if self.tokens[self.index][0] == "this":
            self.index += 1
            if self.ts2():
                return True
        elif self.tokens[self.index][0] == "super":
            self.index += 1
            if self.ts2():
                return True
        return False

    def arg3(self):
        if self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.arg4():
                return True
        elif self.tokens[self.index][1] == ")":
            return True
        return False

    def arg4(self):
        if self.tokens[self.index][1] == ",":
            self.index += 1
            if self.tokens[self.index][0] == "ID":
                self.index += 1
                if self.arg3():
                    return True
        elif self.tokens[self.index][1] == ")":
            return True
        return False

    def ts2(self):
        if self.tokens[self.index][1] == ".":
            self.index += 1
            if self.tokens[self.index][0] == "ID":
                self.index += 1
                if self.SST1():
                    return True
        elif self.tokens[self.index][1] == "(":
            self.index += 1
            if self.arg3():
                if self.tokens[self.index][1] == ")":
                    self.index += 1
                    if self.tokens[self.index][1] == ";":
                        self.index += 1
                        return True
        return False
     # OBJECT DECLARATION
    def obj_dec(self):
        if (
            self.tokens[self.index][0] == "ID" and
            self.tokens[self.index + 1][0] == "ID" and
            self.tokens[self.index + 2][1] == "=" and
            self.tokens[self.index + 3][0] == "new" and
            self.tokens[self.index + 4][0] == "ID"
        ):
            self.index += 5
            if self.tokens[self.index][1] == "(":
                self.index += 1
                if self.arg():
                    if self.tokens[self.index][1] == ")":
                        self.index += 1
                        if self.tokens[self.index][1] == ";":
                            self.index += 1
                            return True
        return False
     # ASSIGNMENT

    def assign_st(self):
        if self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.pl():
                if self.tokens[self.index][1] == "=":
                    self.index += 1
                    if self.OE():
                        if self.tokens[self.index][1] == ";":
                            self.index += 1
                            return True
        return False

    def pl(self):
        if self.tokens[self.index][1] == "[":
            self.index += 1
            if self.OE():
                if self.tokens[self.index][1] == "]":
                    self.index += 1
                    if self.pl1():
                        return True
        elif self.tokens[self.index][0] == "ID" and self.tokens[self.index + 1][1] == ".":
            self.index += 2
            if self.pl1():
                return True
        elif self.tokens[self.index][1] == "(":
            self.index += 1
            if self.arg():
                if self.tokens[self.index][1] == ")":
                    self.index += 1
                    if self.pl2():
                        return True
        elif self.tokens[self.index][1] == "=":
            return True
        return False

    def pl1(self):
        if self.tokens[self.index][1] == "[":
            self.index += 1
            if self.OE():
                if self.tokens[self.index][1] == "]":
                    self.index += 1
                    if self.pl1():
                        return True
        elif self.tokens[self.index][0] == "ID" and self.tokens[self.index + 1][1] == ".":
            self.index += 2
            if self.pl1():
                return True
        elif self.tokens[self.index][1] == "(":
            self.index += 1
            if self.arg():
                if self.tokens[self.index][1] == ")":
                    self.index += 1
                    if self.pl1():
                        return True
        elif self.tokens[self.index][1] == "=":
            return True
        return False

    def pl2(self):
        if self.tokens[self.index][0] == "ID" and self.tokens[self.index + 1][1] == ".":
            self.index += 2
            if self.pl1():
                return True
        return False
     #FUNCTION-DECLARATION
    def Function(self):
        # if (self.tokens[self.index][0] == "void" or (self.tokens[self.index][0] == "DT" and self.tokens[self.index+1][0] == "ID")):
        #     self.index += 2
        if self.tokens[self.index][1] == "(":
            self.index += 1
            if self.param():
                if self.tokens[self.index][1] == ")":
                    self.index += 1
                    if self.body():
                        return True
                        
        return False

    # def func_ret_type(self):
    #     if self.tokens[self.index][0] == "void":
    #         self.index += 1
    #         return True
    #     elif self.tokens[self.index][0] == "DT":
    #         self.index += 1
    #         if self.br():
    #             return True
    #     elif self.tokens[self.index][0] == "ID":
    #         self.index += 1
    #         if self.br():
    #             return True
    #     return False

    # def fun_ID(self):
    #     if self.hid_method():
    #         return True
    #     elif self.fun2_body():
    #         return True
    #     return False

    # def hid_method(self):
    #     if self.tokens[self.index][0] == "hidden":
    #         self.index += 1
    #         if self.func_ret_type():
    #             if self.tokens[self.index][0] == "ID":
    #                 self.index += 1
    #                 if self.tokens[self.index][1] == "(":
    #                     self.index += 1
    #                     if self.param():
    #                         if self.tokens[self.index][1] == ")":
    #                             self.index += 1
    #                             if self.tokens[self.index][1] == ";":
    #                                 self.index += 1
    #                                 return True
    #     return False

    def param(self):
        if self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.br():
                if self.tokens[self.index][0] == "ID":
                    self.index += 1
                    if self.param1():
                        return True
        elif self.tokens[self.index][0] == "DT":
            self.index += 1
            if self.br():
                if self.tokens[self.index][0] == "ID":
                    self.index += 1
                    if self.param1():
                        return True
        elif self.tokens[self.index][1] == ")":
            return True
        return False

    def param1(self):
        if self.tokens[self.index][1] == ",":
            self.index += 1
            if self.param2():
                return True
        elif self.tokens[self.index][1] == ")":
            return True
        return False

    def param2(self):
        if self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.br():
                if self.tokens[self.index][0] == "ID":
                    self.index += 1
                    if self.param1():
                        return True
        elif self.tokens[self.index][0] == "DT":
            self.index += 1
            if self.br():
                if self.tokens[self.index][0] == "ID":
                    self.index += 1
                    if self.param1():
                        return True
        elif self.tokens[self.index][1] == ")":
            return True
        return False

    def fun2_body(self):
        if self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.tokens[self.index][1] == "(":
                self.index += 1
                if self.param():
                    if self.tokens[self.index][1] == ")":
                        self.index += 1
                        if self.body():
                            return True
        return False
    #FUNCTION CALLING
    def arg(self):
        if self.OE():
            if self.arg2():
                return True
        elif self.tokens[self.index][1] == ")":
            return True
        return False

    def arg2(self):
        if self.tokens[self.index][1] == ",":
            self.index += 1
            if self.OE():
                if self.arg2():
                    return True
        elif self.tokens[self.index][1] == ")":
            return True
        return False
     #OE
    # ///////////////////////////////////////EXPRESSION///////////////////////////////////
    def OE(self):
        if not self.AE():
            return False
        if not self.OE_prime():
            return False
        return True

    def OE_prime(self):
        if self.tokens[self.index][0] == 'or':
            self.index += 1
            if not self.AE():
                return False
            if not self.OE_prime():
                return False
        # handle epsilon
        return True

    def AE(self):
        if not self.RE():
            return False
        if not self.AE_prime():
            return False
        return True

    def AE_prime(self):
        if self.tokens[self.index][0] == 'and':
            self.index += 1
            if not self.RE():
                return False
            if not self.AE_prime():
                return False
        # handle epsilon
        return True

    def RE(self):
        if not self.E():
            return False
        if not self.RE_prime():
            return False
        return True

    def RE_prime(self):
        if self.tokens[self.index][0] == 'ROP':
            self.index += 1
            if not self.E():
                return False
            if not self.RE_prime():
                return False
        # handle epsilon
        return True

    def E(self):
        if not self.T():
            return False
        if not self.E_prime():
            return False
        return True

    def E_prime(self):
        if self.tokens[self.index][0] in ('PM', 'MDM') or self.tokens[self.index][1]=='=':
            self.index += 1
            if not self.T():
                return False
            if not self.E_prime():
                return False
        # handle epsilon
        return True

    def T(self):
        if not self.F():
            return False
        if not self.T_prime():
            return False
        return True

    def T_prime(self):
        if self.tokens[self.index][0] == 'MDM':
            self.index += 1
            if not self.F():
                return False
            if not self.T_prime():
                return False
        # handle epsilon
        return True

    def F(self):
        if self.tokens[self.index][0] =='ID':
            self.index += 1
            return True
        elif self.constant():
            return True
                
        elif self.tokens[self.index][0] == '(':
            self.index += 1
            if not self.OE():
                return False
            if self.tokens[self.index][0] != ')':
                return False
            self.index += 1
            return True
        elif self.tokens[self.index][0] == '!':
            self.index += 1
            if not self.F():
                return False
            return True
        # handle other cases for <F>
        return False
      

    def ts3(self):
        if (
            self.tokens[self.index][1] == "this" or self.tokens[self.index][1] == "super"
            or self.tokens[self.index][0] == "ID"
        ):
           
            if (
                self.tokens[self.index][1] == "this" and self.tokens[self.index + 1][1] == "."
            ):
                self.index = self.index + 2
                return True
            elif (
                self.tokens[self.index][1] == "super" and self.tokens[self.index + 1][1] == "."
            ):
                self.index = self.index + 2
                return True
            elif self.tokens[self.index][0] == "ID":
                return True
        return False

    def O(self):
        if (
            self.tokens[self.index][0] == "and"
            or self.tokens[self.index][0] == "MDM"
            or self.tokens[self.index][0] == "PM"
            or self.tokens[self.index][0] == "or"
            or self.tokens[self.index][0] == "ROP"
            or self.tokens[self.index][1] == ";"
            or self.tokens[self.index][1] == ","
            or self.tokens[self.index][1] == ")"
            or self.tokens[self.index][1] == "]"
            or self.tokens[self.index][1] == "}"
            or self.tokens[self.index][1] == "."
            or self.tokens[self.index][1] == "="
            or self.tokens[self.index][1] == "("
            or self.tokens[self.index][1] == "["
        ):
            if self.R():
                return True
        return False

    # def F(self):
    #     if (
    #          self.tokens[self.index][1] == "this" or self.tokens[self.index][1] == "super"
    #         or self.tokens[self.index][0] == "ID" or self.tokens[self.index][0] == "INTEGER"
    #         or self.tokens[self.index][0] == "FLOAT" or self.tokens[self.index][0] == "STRING"
    #         or self.tokens[self.index][0] == "BOOLEAN" or self.tokens[self.index][0] == "CHARACTER"
    #         or self.tokens[self.index][0] == "(" or self.tokens[self.index][1] == "!"
    #     ):
    #         if self.ts3():
    #             if self.tokens[self.index][0] == "ID":
    #                 self.index += 1
    #                 if self.O():
    #                     return True
    #         elif self.constant():
    #             return True
    #         elif self.tokens[self.index][1] == "(":
    #             self.index += 1
    #             if self.OE():
    #                 if self.tokens[self.index][1] == ")":
    #                     return True
    #         elif self.tokens[self.index][1] == "!":
    #             self.index += 1
    #             if self.tokens[self.index][1] == "(":
    #                 self.index += 1
    #                 if self.F():
    #                     if self.tokens[self.index][1] == ")":
    #                         self.index += 1
    #                         return True
    #     return False

    def R(self):
        if (
            self.tokens[self.index][1] == "("
            or self.tokens[self.index][1] == "."
            or self.tokens[self.index][1] == "["
            or self.tokens[self.index][1] == "="
        ):
            if self.tokens[self.index][1] == "[":
                self.index += 1
                if self.OE():
                    if self.tokens[self.index][1] == "]":
                        self.index += 1
                        if self.iconst():
                            if self.v():
                                return True
            elif self.tokens[self.index][1] == "(":
                self.index += 1
                if self.arg():
                    if self.tokens[self.index][1] == ")":
                        self.index += 1
                        if self.q():
                            return True
            elif self.R1():
                return True
            elif self.a():
                return True
        return False

    def a(self):
        if self.tokens[self.index][1] == "=":
            self.index += 1
            if self.OE():
                return True
        return False

    def v(self):
        if (
            self.tokens[self.index][0] == "and"
            or self.tokens[self.index][0] == "MDM"
            or self.tokens[self.index][0] == "PM"
            or self.tokens[self.index][0] == "or"
            or self.tokens[self.index][0] == "ROP"
            or self.tokens[self.index][1] == ";"
            or self.tokens[self.index][1] == ","
            or self.tokens[self.index][1] == ")"
            or self.tokens[self.index][1] == "]"
            or self.tokens[self.index][1] == "}"
            or self.tokens[self.index][1] == "."
            or self.tokens[self.index][1] == "="
        ):
            if self.init():
                return True
            elif self.R1():
                return True
            elif (
                self.tokens[self.index][0] == "and"
                or self.tokens[self.index][0] == "MDM"
                or self.tokens[self.index][0] == "PM"
                or self.tokens[self.index][0] == "or"
                or self.tokens[self.index][0] == "ROP"
                or self.tokens[self.index][1] == ";"
                or self.tokens[self.index][1] == ","
                or self.tokens[self.index][1] == ")"
                or self.tokens[self.index][1] == "]"
                or self.tokens[self.index][1] == "}"
            ):
                return True
        return False

    def q(self):
        if (
            self.tokens[self.index][0] == "and"
            or self.tokens[self.index][0] == "MDM"
            or self.tokens[self.index][0] == "PM"
            or self.tokens[self.index][0] == "or"
            or self.tokens[self.index][0] == "ROP"
            or self.tokens[self.index][1] == ";"
            or self.tokens[self.index][1] == ","
            or self.tokens[self.index][1] == ")"
            or self.tokens[self.index][1] == "]"
            or self.tokens[self.index][1] == "}"
        ):
            if self.R1():
                return True
            elif (
                self.tokens[self.index][0] == "and"
                or self.tokens[self.index][0] == "MDM"
                or self.tokens[self.index][0] == "PM"
                or self.tokens[self.index][0] == "or"
                or self.tokens[self.index][0] == "ROP"
                or self.tokens[self.index][1] == ";"
                or self.tokens[self.index][1] == ","
                or self.tokens[self.index][1] == ")"
                or self.tokens[self.index][1] == "]"
                or self.tokens[self.index][1] == "}"
            ):
                return True
        return False

    def R1(self):
        if self.tokens[self.index][1] == ".":
            self.index += 1
            if self.R2():
                return True
        return False

    def R2(self):
        if (
            self.tokens[self.index][0] == "ID"
            or self.tokens[self.index][0] == "new"
        ):
            if self.tokens[self.index][0] == "ID":
                self.index += 1
                if self.R3():
                    return True
            elif self.tokens[self.index][0] == "new":
                self.index += 1
                if self.tokens[self.index][0] == "ID":
                    self.index += 1
                    if self.tokens[self.index][0] == "(":
                        self.index += 1
                        if self.arg():
                            self.index += 1
                            if self.tokens[self.index][0] == ")":
                                self.index += 1
                                if self.R1():
                                    return True
        return False

    def R3(self):
        if (
            self.tokens[self.index][0] == "and"
            or self.tokens[self.index][0] == "MDM"
            or self.tokens[self.index][0] == "PM"
            or self.tokens[self.index][0] == "or"
            or self.tokens[self.index][0] == "ROP"
            or self.tokens[self.index][1] == ";"
            or self.tokens[self.index][1] == ","
            or self.tokens[self.index][1] == ")"
            or self.tokens[self.index][1] == "]"
            or self.tokens[self.index][1] == "}"
            or self.tokens[self.index][1] == "."
            or self.tokens[self.index][1] == "="
            or self.tokens[self.index][1] == "("
            or self.tokens[self.index][1] == "["
        ):
            if self.R():
                return True
            elif (
                self.tokens[self.index][1] == "and"
                or self.tokens[self.index][0] == "MDM"
                or self.tokens[self.index][0] == "PM"
                or self.tokens[self.index][1] == "or"
                or self.tokens[self.index][0] == "ROP"
                or self.tokens[self.index][1] == ";"
                or self.tokens[self.index][1] == ","
                or self.tokens[self.index][1] == ")"
                or self.tokens[self.index][1] == "]"
                or self.tokens[self.index][1] == "}"
            ):
                return True
        return False

    def constant(self):
        if self.tokens[self.index][0] == "INTEGER":
            self.index += 1
            return True
        elif self.tokens[self.index][0] == "FLOAT":
            self.index += 1
            return True
        elif self.tokens[self.index][0] == "BOOLEAN":
            self.index += 1
            return True
        elif self.tokens[self.index][0] == "CHARACTER":
            self.index += 1
            return True
        return False

        #class 
        
          
    #ARRAY-DEC
    def br(self):
        if self.tokens[self.index][1] == "[":
            self.index += 1
            if self.tokens[self.index][1] == "]":
                self.index += 1
                # if self.ar():
                return True
        elif self.tokens[self.index][0] in ["hidden", "ID"]:
            return True
        return False

    def ar(self):
        if(self.tokens[self.index][0]=="ID"):
            return True
        if self.tokens[self.index][1] == "[":
            self.index += 1
            if self.tokens[self.index][1] == "]":
                self.index += 1
                if(self.tokens[self.index][1] == "["):
                    return False
                return True
        return False

    def Arraydef(self):
        if self.tokens[self.index][1] == "=":
            self.index += 1
            if self.Arraydef1():
                return True
        elif self.tokens[self.index][1] == ";":
            return True
        return False

    def Arraydef1(self):
        if self.tokens[self.index][0] == "new":
            self.index += 1
            if self.tokens[self.index][0] == "DT":
                self.index += 1
                if self.tokens[self.index][1] == "[":
                    self.index += 1
                    if self.OE():
                        if self.tokens[self.index][1] == "]":
                            self.index += 1
                            if self.iconst():
                                return True
        elif self.b():
            return True
        return False

    def iconst(self):
        if self.tokens[self.index][1] == "[":
            self.index += 1
            if self.OE():
                if self.tokens[self.index][1] == "]":
                    self.index += 1
                    if self.iconst():
                        return True
        elif self.tokens[self.index][1] == ";":
            return True
        return False

    def val1(self):
        if self.tokens[self.index][1] == ",":
            self.index += 1
            if self.OE():
                if self.val1():
                    return True
        elif self.tokens[self.index][1] == "}":
            return True
        return False

    def val2(self):
        if self.tokens[self.index][1] == ",":
            self.index += 1
            if self.b():
                return True
        elif self.tokens[self.index][1] in [";", "}"]:
            return True
        return False

    def b(self):
        if self.tokens[self.index][1] == "{":
            self.index += 1
            if self.b1():
                if self.tokens[self.index][1] == "}":
                    self.index += 1
                    if self.val2():
                        return True
        return False

    def b1(self):
        if self.OE():
            if self.val1():
                return True
        elif self.tokens[self.index][1] == "{":
            self.index += 1
            if self.b1():
                if self.tokens[self.index][1] == "}":
                    self.index += 1
                    if self.val2():
                        return True
        elif self.tokens[self.index][1] == "}":
            return True
        return False
 

   

    def S(self):
        while self.tokens[self.index][0] != "$":
            if not(self.SST()):
                return False

        return True


if __name__ == '__main__':
    import os

    # Define the regular expressions for tokens
    Tokenizer.define_tokens()

    file_path = "./input.txt" # Replace with the actual absolute path to the file
    if os.path.exists(file_path):
        with open(file_path) as file_handler:
            t = Tokenizer(file_handler)
            tokens = t.tokenize_input()
            for token_name, token, start_line_num in tokens:
                print(f"({token_name}, {token} , {start_line_num})\n")

        # Assuming the SyntaxPhase class and its methods are properly defined
        syntax_phase = SyntaxPhase(tokens)
        syntax_phase.run()
    else:
        print(f"File not found at the specified path: {file_path}")


             
       
   
