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
                if self.br():
                    return True
        elif self.tokens[self.index][0] in ["hidden", "ID"]:
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

