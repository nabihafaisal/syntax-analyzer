from Semantic import SemanticClass
from New_Semantic import Semantic
from prettytable import PrettyTable


#########################SYNTAX ANALYZER###########################

class SyntaxPhase:
    def __init__(self, tokens):
        self.T = None
        self.N = None
        self.Am = "private"
        self.Cat = None
        self.refDt = []
        self.Prnt = None
        self.Type = None
        self.cTm = None
        self.cName = None
        self.cType = None
        self.P = "null"
        self.Fname = None
        self.Ftype = None
        self.opr = None
        self.T1 = "null"
        self.T3 = "null"
        self.T2 = "null"
        self.semantic_class = SemanticClass()
        self.semantic = Semantic()
        self.tokens = tokens
        self.index = 0
        self.formated_function=[]
        self.current_token = None

        #########################################TYPECHECKING################################################       
        self._functionCall_ = {"N":"","PL":""}
        self._function_ = {"N":"","T":"","AM":"","TM":"","PL":""}
        self._CRef_ = ""
        self._exp_ = []#{"T":"","T1":"","T2":"","OP":""}]
        self._evaluatedType_ = None
        #########################################TYPECHECKING################################################       

    def compare(self):
        # try:
        if(len(self._exp_)>0):
            if(self._exp_[-1]["T"] != ""):
                if(self._evaluatedType_ == None):
                    var = self.semantic_class.Compare(self._exp_[-1]["T"],self.Class,self._exp_[-1]["OP"])
                else:
                    var = self.semantic_class.Compare(self._exp_[-1]["T"],self._evaluatedType_,self._exp_[-1]["OP"])
                self._exp_[-1]["T"] = var["T"]
                self._evaluatedType_ = None
            else:
                self._exp_[-1]["T"] = self._evaluatedType_
       

    def Dtempty(self):
        self.cName = None
        self.cTm = None
        self.cType = None
        self.Am = "private"
        self.P = None
      

    def run(self):
        if self.S0():
            if self.index< len(self.tokens):
                if self.tokens[self.index][0] == "$":
                    print("No Syntax Error  :)")
                 
                    
                    print(self.semantic_class.table,"\n")
                    print(self.semantic_class.Btable,"\n")

                   
               
                    print(self.semantic_class.Ftable,"\n")
                  
                    
                else:
                    print(f"  :(   Syntax Error At Line No.: {self.tokens[self.index][2]} {self.tokens[self.index][1]}")
            else:
                print("not reaching $")
        else:
            print(f"  :(   Syntax Error At Line No.: {self.tokens[self.index][2]} {self.tokens[self.index][1]}")
            # print(self.semantic_class.mainTable)
        self.semantic.print()
    def format_function_table(self):
        table = PrettyTable()
        table.field_names = ["Name", "Type", "Scope"]

        for entry in self.semantic_class.functionTable:
            table.add_row([entry["name"], entry["type"], entry["scope"]])

        self.formated_function.append(str(table))      

    def format_class_table(self):
        table = PrettyTable()
        table.field_names = ["Name", "Type", "Access Modifier", "Category", "Parent", "Link"]

        for entry in self.semantic_class.mainTable:
            table.add_row([entry["name"], entry["type"], entry["access_modifier"],
                           entry["category"], entry["parent"], entry["link"]])

        self.formated_function.append(str(table))

    def format_body_table(self,refDt):
        table = PrettyTable()
        table.field_names = ["Name", "Type", "Access Modifier", "Type Modifier","link"]

        for entry in self.refDt:
            table.add_row([entry["name"], entry["type"], entry["access_modifier"], entry["type_modifier"]],entry ["link"])
        

        self.formated_function.append(str(table))     
       

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index][1]
            # self.current_line = self.tokens[self.index]["Line"]
            # self.current_col = self.tokens[self.index]["Col"]
            self.Class = self.tokens[self.index][0]
        else:
            self.current_token = None


    #####################################DECLARATION############################
    # def dec(self):
    #     if (
    #         self.tokens[self.index][0] == "DT"):
    #         self.T=self.tokens[self.index][1]
    #         self.index+=1
    #         if(self.tokens[self.index][0] == "ID"):
    #             self.N=self.tokens[self.index][1]
               
                

              

    #             self.index += 1
             
    #         if self.init():
    #             if self.list():
    #                 return True
    #     return False

    def dec2(self):
        if self.tokens[self.index][1] in ["=", ",", ";"]:
            if self.init():
               
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

    # def fs(self):
    #     if self.tokens[self.index][0] == "static":
    #         self.cTm=self.tokens[self.index][1]
    #         self.index += 1
       
    #     elif self.tokens[self.index][0] == "DT":
    #         self.T=self.tokens[self.index][1]
    #         self.index += 1
    #     return False

    def list(self):
        if self.tokens[self.index][1] == ";":
         
          
            self.index += 1
           
            
            return True
        elif (
            self.tokens[self.index][1] == ","):
            self.index+=1
            
          
            if(self.tokens[self.index][0] == "ID"):
                self.N=self.tokens[self.index][1]
                self.index += 1

            if self.dec2():
                return True
        return False
    

    ############################################ #BODY#########################
    def body(self):
        if self.tokens[self.index][1] == "{":
            
            self.index += 1
            
            if self.MST():
               
                if self.tokens[self.index][1] == "}":
                    
                    self.index += 1
                    self.semantic_class.destroyScope()

                    return True
        return False
    ############################### MST ###########
    def MST(self):
        if (
            self.tokens[self.index][0] in ["if", "while", "else", "for","this","super","ID","return","DT"]
        
        ):
            if self.SST():
                # print("token", self.tokens[self.index][1])
                if self.MST():
                    return True
        elif self.tokens[self.index][1] == "}":
            return True
        return False
    ###################################### SST#####################################
    def SST(self):
        if (
            self.tokens[self.index][0] in [
                "for",
                "while",
            
                "if",

                "return",
                "void",
               
                "DT",
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
                self.T=self.tokens[self.index][1]
                self.index += 1
                if self.SST2():
                    return True
            elif self.tokens[self.index][0] == "void" and self.tokens[self.index+1][0]=="ID":
                self.T=self.tokens[self.index][1]
                self.N=self.tokens[self.index+1][1]
                self.index += 2
                if self.Function():
                    return True
            elif self.tokens[self.index][0] == "ID":
                self.N=self.tokens[self.index][1]
                self.T=""#self.semantic_class.lookup_MT(self.N)
                if self.T=="null":
                    print("Undeclared "+self.N)
                else:
                    self.Prnt=self.N
                self.index += 1
                if self.SST1():
                    return True
        return False
    
    ############################### OBJECT DECLARATION ##############################
    def obj2(self):
        if self.tokens[self.index][1] == "=":
            self.index += 1
            if self.tokens[self.index][0] == "new":
                self.index += 1
                if self.tokens[self.index][0] == "ID":
                    self.N=self.tokens[self.index][1]
                    self.T=""#self.semantic_class.lookup_MT(self.N)
                    if self.T=="null":
                        print("Undeclared "+self.N)
                    else:
                        self.Prnt=self.N
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
        # if (
        #     self.tokens[self.index][0] == "ID"
        #     or self.tokens[self.index][1] == "("
        #     or self.tokens[self.index][1] == "["
           
        #     or self.tokens[self.index][1] == "."
        #     or self.tokens[self.index][1] == "="
        # ):
        if self.tokens[self.index][0] == "ID":
            self.N1=self.tokens[self.index][1]
            self.semantic.insertST(self.N1,self.N)####NEW SEMANTIC########self.semantic_class.insert_FT(self.N1,self.N)
            # if self.T=="null":
            #     print("Undeclared "+self.N)
            # else:
            #     self.Prnt=self.N
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
            self.N=self.tokens[self.index][1]
            # if(self.N!=None and self.T!=None):
            #     self.semantic_class.insert_FT(self.N,self.T)
            #     self.N=None
           
            
            self.index += 1
           
            if self.dec2():
                if(self.N!=None and self.T!=None):
                    self.semantic.insertST(self.N,self.T)####NEW SEMANTIC########self.semantic_class.insert_FT(self.N,self.T)
                    self.N=None
                

              
                
                return True
            elif self.Function():
                return True
        elif self.tokens[self.index][1] == "[":
            self.T+=self.tokens[self.index][1]
            self.index += 1
            if self.tokens[self.index][1] == "]":
                self.T+=self.tokens[self.index][1]
                self.index += 1
                if self.br():
                    if self.tokens[self.index][0] == "ID":
                        self.N=self.tokens[self.index][1]
                        self.semantic.insertST(self.N,self.T)####NEW SEMANTIC########self.semantic_class.insert_FT(self.N,self.T)
                        self.index += 1
                        if self.Arraydef():
                            if self.tokens[self.index][1] == ";":
                                self.index += 1
                                return True
        return False
     ############################################## FOR-LOOP ######################################
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
                            self.semantic_class.createScope()
                            if self.OE():
                                if(self.N!=None):
                                    self.semantic.insertST(self.N,self.T)####NEW SEMANTIC########self.semantic_class.insert_FT(self.N,self.T)
                                if self.tokens[self.index][1] == ")":
                                    self.index += 1
                                    if self.tokens[self.index][1] == ":":
                                        self.index += 1
                                        if self.body():
                                            #self.semantic_class.destroyScope()
                                            self.N=None
                                            self.T=None
                                            return True
        return False
    
    ############################################### WHILE LOOP############################
    def while_state(self):
        if self.tokens[self.index][0] == "while":
            self.index += 1
            if self.tokens[self.index][1] == "(":
                self.semantic_class.createScope()
                self.index += 1

                if self.OE():
                    if (self.N!=None):
                        self.semantic.insertST(self.N,self.T)####NEW SEMANTIC########self.semantic_class.insert_FT(self.N,self.T)
                    if self.tokens[self.index][1] == ")":
                        self.index += 1

                        if self.body():
                        

                            #self.semantic_class.destroyScope()
                            self.N=None
                            self.T=None
                            return True

        return False
    
    ##################################### IF-ELSE ######################################
    def if_else(self):
        if self.tokens[self.index][0] == "if":
            self.index += 1
            if self.tokens[self.index][1] == "(":
                self.semantic_class.createScope()
                self.index += 1
                if self.OE():
                    if (self.N != None):
                        self.semantic.insertST(self.N,self.T)####NEW SEMANTIC########self.semantic_class.insert_FT(self.N,self.T)
                    if self.tokens[self.index][1] == ")":
                        self.index += 1
                        if self.body():
                            #self.semantic_class.destroyScope()
                            self.N=None
                            self.T=None
                            if self.else_state():
                                return True
        return False
    def else_state(self):
        if self.tokens[self.index][0] == "else":
            self.index += 1
            self.semantic_class.createScope()
            if self.body():
                if (self.N!=None):
                    self.semantic.insertST(self.N,self.T)####NEW SEMANTIC########self.semantic_class.insert_FT(self.N,self.T)
                    #self.semantic_class.destroyScope()
                self.N=None
                self.T=None
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
    ############################################### RETURN #################################
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
    ##################################################### TS#######################################
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
    

     ################################################## OBJECT DECLARATION ####################################
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
    
     ######################################################## ASSIGNMENT###############################

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
    
     #################################### FUNCTION-DECLARATION#########################
   


    def func_ret_type(self):
        if self.tokens[self.index][0] == "void":
            self.T=self.tokens[self.index][1]
             
            self.index += 1
            return True
        elif self.tokens[self.index][0] == "DT":
            self.T=self.tokens[self.index][1]
            self.index += 1
            if self.br():
                return True
        elif self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.br():
                return True
        return False

    def fun_ID(self):
        if self.hid_method():
            return True
        elif self.fun2_body():
            return True
        return False
    
    ##################################### ABSTRACT METHOD ################################# 
    def hid_method(self):
        if self.tokens[self.index][0] == "abstract":
            self.cTm=self.tokens[self.index][0]
            self.index += 1
            if self.func_ret_type():
                if self.tokens[self.index][0] == "ID":
                    self.N=self.tokens[self.index][1]

                    self.index += 1
                    if self.tokens[self.index][1] == "(":
                        self.index += 1
                        if self.param():
                            if self.tokens[self.index][1] == ")":
                                self.semantic.insertMT(self.N,self.T,self.Am,self.cTm,self.refDt[0]["name"])####NEW SEMANTIC########self.semantic_class.insert_DT(self.N,self.T,self.Am,self.cTm,self.refDt)
                                self.index += 1
                                if self.tokens[self.index][1] == ";":
                                    self.index += 1
                                    return True
        return False
      ######################################### FUNCTION #########################################
    def Function(self):
      
        if self.tokens[self.index][1] == "(":
            self.index += 1
            self.semantic_class.createScope()
            if self.param():
                if self.tokens[self.index][1] == ")":
                    self.index += 1
                    self.semantic.insertST(self.N,self.T)####NEW SEMANTIC########self.semantic_class.insert_FT(self.N,self.P)
                    
                    if self.body():
                       # self.semantic_class.destroyScope()
                        self.N=None
                        self.P="null"
                        return True
        
        return False

    def param(self):
        if self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.br():
                if self.tokens[self.index][0] == "ID":
                    self.index += 1
                    if self.param1():
                        return True
                    
        elif self.tokens[self.index][0] == "DT":
            self.P=self.T+"-->"
            self.T=self.tokens[self.index][1]
            self.P+=self.T
            self.index += 1
            if self.br():
                if self.tokens[self.index][0] == "ID":
                    self.N1=self.tokens[self.index][1]
                    self.index += 1
                    self.semantic.insertST(self.N1,self.T)####NEW SEMANTIC########self.semantic_class.insert_FT(self.N1,self.T)
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
            self.N=self.tokens[self.index][1]
            self.Ftype=""#self.semantic_class.lookup_MT(self.N)
            if self.Ftype==None:
                print("Undeclared:  "+self.N)
            self.P+="," +self.N
            self.index += 1
            if self.br():
                if self.tokens[self.index][0] == "ID":
                    self.Fname=self.tokens[self.index][1]
                    self.semantic.insertST(self.Fname, self.Ftype)####NEW SEMANTIC########if not self.semantic_class.insert_FT(self.Fname, self.Ftype):
                    # print("Redeclaration")

                    self.index += 1
                    if self.param1():
                        return True
        elif self.tokens[self.index][0] == "DT":
            
            self.T=self.tokens[self.index][1]
            self.P+=","+self.T
         

            self.index += 1
            if self.br():
                if self.tokens[self.index][0] == "ID":
                    self.N1=self.tokens[self.index][1]
                    self.semantic.insertST(self.N1,self.T)####NEW SEMANTIC########self.semantic_class.insert_FT(self.N1,self.T)
                    # if not self.semantic_class.insert_FT(self.N,self.P):
                    #     print("Redeclaration")
                    self.index += 1
                    if self.param1():
                        return True
        elif self.tokens[self.index][1] == ")":
            

            return True
        return False

    def fun2_body(self):
        if self.tokens[self.index][0] == "ID":
            self.cName=self.tokens[self.index][1]
            self.index += 1
            
            if self.tokens[self.index][1] == "(":
                self.semantic_class.createScope()
                self.index += 1
                if self.param():
                    if self.tokens[self.index][1] == ")":
                        
                        self.index += 1
                        
                        self.semantic.insertMT(self.cName,self.T,self.Am,self.cTm,self.refDt[0]["name"])####NEW SEMANTIC########if not self.semantic_class.insert_DT(self.cName,self.P,self.cTm,self.Am,self.refDt):
                                
                        #         print("Function Reclaration")
                        
                        self.Dtempty()
                        if self.body():
                           
                            return True
        return False
    ########################################FUNCTION CALLING#######################################
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
    
     ################################################# OE ####################################

    # def Exp(self):
    #     # print("Exp")
    #     #self.OE.append({"T":"","T1":"","T2":"","OP":""})
    #     if (self.AE()):
    #         if (self.OE()):
    #             #self.evaluatedType = self.OE.pop()["T"]
    #             return True
    #     return False

    # def AE(self):
    #     # print("AE")
    #     if (self.RE()):
    #         if (self.AE_()):
    #             return True
    #     return False

    # def OE(self):
    #     # print("OE")
    #     # if (self.tokens[self.index][1] in ";,)]"):
    #     #     return True
    #     if (self.tokens[self.index][1] == "&&"):
    #         self.index+=1
    #         if (self.AE()):
    #             if (self.OE()):
    #                 return True
    #     return False

    # def AE_(self):
    #     # print("AE_")
    #     if (self.tokens[self.index][1] == "&&"):
    #         return True
    #     if (self.tokens[self.index][1] == "||"):
    #         self.index+=1
    #         if (self.RE()):
    #             if (self.AE_()):
    #                 return True
    #     return False

    # def RE(self):
    #     # print("RE")
    #     if (self.E()):
    #         if (self.RE_()):
    #             return True
    #     return False

    # def RE_(self):
    #     # print("RE_")
    #     if (self.tokens[self.index][1] == "||" or self.tokens[self.index][1] == "&&"):
    #         return True
    #     if (self.tokens[self.index][1] [">=", "<=", "==", ">", "<", "!="]):
    #         self.opr=self.tokens[self.index][1]
    #         self.index+=1
    #         if (self.E()):
    #             if (self.RE_()):
    #                 return True
    #     return False

    # def E(self):
    #     # print("E")
    #     if (self.TI()):
    #         if (self.E_()):
    #             return True
    #     return False

    # def E_(self):
    #     # print("E_")
    #     if (self.tokens[self.index][1] in [">=", "<=", "==", ">", "<", "!="] or self.tokens[self.index][1] == "||" or self.tokens[self.index][1] == "&&"):
    #         return True
    #     if (self.tokens[self.index][1] in "+-"):
    #         self.opr=self.tokens[self.index][1]
    #         self.index+=1
    #         if (self.TI()):
    #             if (self.E_()):
    #                 return True
    #     return False

    # def TI(self):
    #     # print("T")
    #     if (self.F()):
    #         if (self.T_()):
    #             return True
    #     return False

    # def T_(self):
    #     # print("T_")
    #     if (self.tokens[self.index][1] in "+-" or self.tokens[self.index][1] in [">=", "<=", "==", ">", "<", "!="] or self.tokens[self.index][1] == "||" or self.tokens[self.index][1] == "&&"):
    #         return True
    #     if (self.tokens[self.index][1] in "*/"):
    #         self.tokens[self.index][1]
    #         self.index+=1
    #         if (self.F()):
    #             if (self.T_()):
    #                 return True
    #     return False

    # def F(self):
    #     # print("F")
    #     return self.Vals()

    # def Vals(self):
    #     # print("Vals")
    #     if (self.constant()):
    #         #self.compare()
    #         self.index+=1
    #         return True
    #     # if (self.arr()):
    #     #     return True
    #     # if (self.FuncVarLF()):
    #     #     # self.advance()
    #     #     return True
    #     if (self.obj2()):
    #         return True
    #     if (self.tokens[self.index][1]=="("):
    #         self.index+=1
    #         if (self.OE()):
    #             if (self.tokens[self.index][1] == ")"):
    #                # self.compare()
    #                 self.index+=1
    #                 return True
    #     if (self.tokens[self.index][1] == "!"):
    #         self.index+=1
    #         return self.Vals()
    #     return False


    def constant(self):
        if self.tokens[self.index][0] == "INTEGER":
            self.index += 1
            self.T1="int"
            return self.T1
        elif self.tokens[self.index][0] == "FLOAT":
            self.index += 1
            self.T1="float"
            return self.T1
        elif self.tokens[self.index][0] == "BOOLEAN":
            self.index += 1
            self.T1="bool"
            return self.T1
        elif self.tokens[self.index][0] == "CHARACTER":
            self.index += 1
            self.T1="character"
            return self.T1
        elif self.tokens[self.index][0] == "STRING":
            self.index += 1
            self.T1="string"
            return self.T1
       
       
        
            
        return False
    def OE(self):
        self._exp_.append({"T":"","T1":"","T2":"","OP":""})
        if not self.AE():
            return False
        if not self.OE_prime():
            return False
        self._evaluatedType_ = self._exp_.pop()["T"]
        return True

    def OE_prime(self):
        if self.tokens[self.index][0] == 'or':
            self.opr=self.tokens[self.index][0]
           
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
            self.opr=self.tokens[self.index][0]
            
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
            self.opr=self.tokens[self.index][1]
            ##########################TYPE CHECKING#############################
            self._exp_[-1]["OP"] = self.opr
            ##########################TYPE CHECKING#############################
   
            self.index += 1
            if not self.E():
                return False
            if not self.RE_prime():
                return False
        # handle epsilon
        return True

    def E(self):
        if not self.TI():
            return False
        if not self.E_prime():
            return False
        return True

    def E_prime(self):
        if (self.tokens[self.index][0] in ('PM') or self.tokens[self.index][1]=='='):
            self.opr=self.tokens[self.index][1]
            # self.T2=self.semantic_class.Compare(self.T,self.T1,self.opr)

            ##########################TYPE CHECKING#############################
            self._exp_[-1]["OP"] = self.opr
            ##########################TYPE CHECKING#############################

            self.index += 1
            if not self.TI():
                return False
            if not self.E_prime():
                return False
        # handle epsilon
        return True

    def TI(self):
        if not self.F():
            return False
        if not self.T_prime():
            return False
        return True

    def T_prime(self):
        if self.tokens[self.index][0] == 'MDM':
            self.opr=self.tokens[self.index][1]
            self.index += 1
            ##########################TYPE CHECKING#############################
            self._exp_[-1]["OP"] = self.opr
            ##########################TYPE CHECKING#############################
            self.T2=self.semantic_class.Compare(self.T,self.T1,self.opr)
            if not self.F():
                return False
            if not self.T_prime():
                return False
        # handle epsilon
        return True

    def F(self):
        if self.tokens[self.index][0] =='ID':
            # self.N=self.tokens[self.index][1]
            N=self.tokens[self.index][1]
            self.T1=""#self.semantic_class.lookup_FT(N)
            self._evaluatedType_ = self.T1
            self.compare()
            if (self.T=="null"):
               print("UNDECLARED")
            self.index += 1
            # self.tokens[self.index][1] = self.tokens[self.index][1]
            if(self.FuncVar()):
                return True
            else:
                return False
            return True
        elif self.constant():
            self._evaluatedType_ = self.T1
            self.compare()
            return True   
        elif self.tokens[self.index][0] == '(':
            self.index += 1
            if not self.OE():
                return False
            if self.tokens[self.index][0] != ')':
                return False
            self.compare()
            self.index += 1
            return True
        elif self.tokens[self.index][0] == '!':
            self.index += 1
            if not self.F():
                return False
        return True
  # handle ReferenceAccesser cases for <F>
        return False
    
    ################################################ ARRAY-DEC ##################################

    def br(self):
        if self.tokens[self.index][1] == "[":
            self.T+=self.tokens[self.index][1]
            self.index += 1
            if self.tokens[self.index][1] == "]":
                self.T+=self.tokens[self.index][1]
                self.index += 1
                
                return True
        elif self.tokens[self.index][0] in ["abstract", "ID"]:
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
 
    ################################################ CLASS #################################
    def class_state(self):
        if self.tokens[self.index][0] == "abstract":
            self.Cat=self.tokens[self.index][1]
            self.index += 1
            if self.tokens[self.index][0] == "class":
                self.T="class"
                self.index += 1
                if self.tokens[self.index][0] == "ID":
                    self.N=self.tokens[self.index][1]
                    self.index += 1
                    if self.inherit():
                        self.refDt=self.semantic_class.create_DT()
                        self.semantic_class.add_default_constructor(self.N,self.refDt)
                        
                        self.semantic.insertDT(self.N,self.T,self.Cat,self.Prnt,self.Am)####NEW SEMANTIC########self.semantic_class.insert_MT(self.N,self.T,self.Am,self.Cat,self.Prnt,self.refDt)
                        if self.tokens[self.index][0] == "{":
                            self.semantic_class.createScope()
                            self.index += 1
                            if self.C1():
                                return True
        elif self.seal():
            if self.tokens[self.index][0] == "class":
                self.T="class"
                self.index += 1
                if self.tokens[self.index][0] == "ID":
                    self.N=self.tokens[self.index][1]
                    self.index += 1
                    if self.inherit():
                        # self.refDt=self.semantic_class.create_DT()
                        # self.semantic_class.add_default_constructor(self.N,self.refDt)
                        self.semantic.insertDT(self.N,self.T,self.Cat,self.Prnt,self.Am)####NEW SEMANTIC########self.semantic_class.insert_MT(self.N,self.T,self.Am,self.Cat,self.Prnt,self.refDt)
                       
                        if self.tokens[self.index][1] == "{":
                            self.semantic_class.createScope()
                            self.index += 1
                            if self.D1():
                                return True
        return False
    
    ######################################## SEALED #############################################
    def seal(self):
        if self.tokens[self.index][0] == "sealed":
            self.Cat=self.tokens[self.index][1]
            self.index += 1
            return True
        elif self.tokens[self.index][0] == "class":
            self.T=self.tokens[self.index][1]
            return True
        else:
            return False
    ################################################ INHERITS ####################################
    def inherit(self):
        if (self.tokens[self.index][0] == "extends" ):
            self.index+=1
            if( self.tokens[self.index][0] == "ID"):
                self.N1=self.tokens[self.index][1]
                self.T=""#self.semantic_class.lookup_MT(self.N1)
                if (self.T == "null"):
                    print("Undeclared: " + self.N1)
                elif (self.T == "class" and self.Cat == "sealed"):
                    print("sealed class cannot be inherited")
                else:
                    self.Prnt = self.N1
                    self.index += 1
            return True
        
        elif self.tokens[self.index][1] == "{":
            self.semantic_class.createScope()
            return True
        return False

    def C1(self):
        if self.tokens[self.index][1] == "}":
            self.semantic_class.destroyScope()
            self.index += 1
            if self.S0():
                return True
        elif self.hid_CB():
            return True
        return False   
    def hid_CB(self):
        if self.tokens[self.index][1] == "public":
            self.Am=self.tokens[self.index][1]
            self.index += 1
            if self.A1():
                return True
        elif self.tokens[self.index][1] == "private":
            self.Am=self.tokens[self.index][1]
            self.index += 1
            if self.A2():
                if self.C1():
                    return True
        elif self.tokens[self.index][1] == "protected":
            self.Am=self.tokens[self.index][1]
            self.index += 1
            if self.A2():
                if self.C1():
                    return True
        elif self.A8():
            if self.C1():
                return True
        return False

    def A1(self):
        if self.tokens[self.index][0] == "static":
            self.cTm=self.tokens[self.index][1]
            self.index += 1
            # if self.A3():
            #     return True
        # elif self.tokens[self.index][1] == "final":
        #     self.index += 1
        #     if self.A18():
        #         if self.C1():
        #             return True
        elif self.A18():
            if self.C1():
                return True
        return False

    def A2(self):
        if self.tokens[self.index][0] == "static":
            self.cTm=self.tokens[self.index][1]
            self.index += 1
            if self.A7():
                return True
        elif self.tokens[self.index][1] == "virtual" :
            self.index += 1
            if self.A18():
                return True
        elif self.A18():
            return True
        return False
  

    # def A3(self):
    #     if self.tokens[self.index][1] == "final":
    #         self.index += 1
    #         if self.A18():
    #             if self.C1():
    #                 return True
    #     elif self.A19():
    #         return True
    #     return False

    def A19(self):
        if self.tokens[self.index][0] == "void":
            self.T=self.tokens[self.index][1]
            self.index += 1
            if self.A5():
                return True
        elif self.tokens[self.index][0] == "DT":
            self.T = self.tokens[self.index][1]
            self.index += 1
            if self.A20():
                if self.C1():
                    return True
        elif self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.A21():
                if self.C1():
                    return True
        return False

    def A5(self):
        if self.tokens[self.index][0] == "main":
            self.index += 1
            if self.A6():
                return True
        elif self.A13():
            if self.C1():
                return True
        return False
    #func
    def A6(self):
        if self.tokens[self.index][0] == "(":
            self.index += 1
            if self.tokens[self.index][0] == ")":
                self.index += 1
                if self.body():
                    if self.C():
                        return True
        return False
    #virtual func
    def A7(self):
        if (self.tokens[self.index][1] == "virtual" or
        self.tokens[self.index][1] == "override"):
            self.index += 1
            if self.A18():
                return True
        elif self.A18():
            return True
        return False
    #static and virtual
    def A8(self):
        if self.tokens[self.index][0] == "static":
            self.cTm=self.tokens[self.index][1]
            self.index += 1
            if self.A9():
                return True
        elif (self.tokens[self.index][1] == "virtual" or
        self.tokens[self.index][1] == "override"):
            self.cTm=self.tokens[self.index][1]
            self.index += 1
            if self.A18():
                return True
        elif self.A4():
            return True
        return False

    def A9(self):
        if (self.tokens[self.index][1] == "virtual" or
        self.tokens[self.index][1] == "override"):
            self.cTm=self.tokens[self.index][1]
            
            self.index += 1
            if self.A18():
                return True
        elif self.A18():
            return True
        return False

    def A4(self):
        if self.tokens[self.index][0] == "void":
            self.T=self.tokens[self.index][1]
            self.index += 1
            if self.A13():
                return True
        elif self.tokens[self.index][0] == "DT":
            self.T=self.tokens[self.index][1]
            self.index += 1
            if self.A10():
                return True
        elif self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.A14():
                return True
        elif self.hid_method():
            return True
        return False

    def A10(self):
        if self.tokens[self.index][0] == "[":
            self.index += 1
            if self.tokens[self.index][0] == "]":
                self.index += 1
                if self.br():
                    if self.A11():
                        return True
        elif self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.A16():
                return True
        elif self.A12():
            return True
        return False

    def A12(self):
        if self.hid_method():
            return True
        return False

    def A11(self):
        if self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.A15():
                return True
        elif self.A12():
            return True
        return False

    def A14(self):
        if self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.A17():
                return True
        elif self.tokens[self.index][0] == "[":
            self.index += 1
            if self.tokens[self.index][0] == "]":
                self.index += 1
                if self.br():
                    if self.A13():
                        return True
        elif self.A12():
            return True
        return False

    def A15(self):
        if self.tokens[self.index][0] == "(":
            self.index += 1
            if self.param():
                if self.tokens[self.index][0] == ")":
                    self.index += 1
                    if self.body():
                        return True
        elif self.Arraydef():
            if self.tokens[self.index][1] == ";":
                self.index += 1
                return True
        return False

    def A16(self):
        if self.tokens[self.index][0] == "(":
            self.index += 1
            if self.param():
                if self.tokens[self.index][0] == ")":
                    self.semantic.insertMT(self.cName,self.T,self.Am,self.cTm,self.refDt[0]["name"])####NEW SEMANTIC########if not self.semantic_class.insert_DT(self.cName,self.P,self.cTm,self.Am,self.refDt):
                       
                    #     print("Function Declaration")
                    self.Dtempty()


                    
                    self.index += 1
                    if self.body():
                       
                        return True
                    
        elif self.init():
            self.semantic.insertMT(self.cName,self.T,self.Am,self.cTm,self.refDt[0]["name"])####NEW SEMANTIC######## if not self.semantic_class.insert_DT(self.cName,self.T,self.cTm,self.Am,self.refDt):
                       
            #             print("ReDeclaration")
            self.Dtempty()
            if self.list():
                return True
        return False

    def A17(self):
        if self.tokens[self.index][0] == "(":
            self.index += 1
            if self.param():
                if self.tokens[self.index][0] == ")":
                    self.index += 1
                    if self.body():
                        return True
        elif self.tokens[self.index][1] == "=":
            self.index += 1
            if self.tokens[self.index][0] == "new":
                self.index += 1
                if self.tokens[self.index][0] == "ID":
                    self.index += 1
                    if self.tokens[self.index][0] == "(":
                        self.index += 1
                        if self.arg():
                            if self.tokens[self.index][0] == ")":
                                self.index += 1
                                if self.tokens[self.index][1] == ";":
                                    self.index += 1
                                    return True
        return False

    def A13(self):
        if self.fun2_body():
            return True
        return False

    def A18(self):
        if self.tokens[self.index][0] == "void":
            self.T=self.tokens[self.index][1]
            self.index += 1
            if self.A13():
                return True
        elif self.tokens[self.index][0] == "DT":
            self.T=self.tokens[self.index][1]
            self.index += 1
            if self.A20():
                return True
        elif self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.A21():
                return True
        return False

    def A20(self):
        if self.tokens[self.index][0] == "[":
            self.index += 1
            if self.tokens[self.index][0] == "]":
                self.index += 1
                if self.br():
                    if self.A13():
                        return True
        elif self.tokens[self.index][0] == "ID":
            self.cName=self.tokens[self.index][1]
            self.index += 1
            if self.A16():
                return True
        elif self.A12():
            return True
        return False

    def A21(self):
        if self.tokens[self.index][0] == "[":
            self.index += 1
            if self.tokens[self.index][0] == "]":
                self.index += 1
                if self.br():
                    if self.A13():
                        return True
   
 
    def C(self):
        if self.tokens[self.index][0] == "}":
            self.index += 1
            if self.S2():
                return True
        elif self.HCB():
            return True
        return False

    def D1(self):
        if self.tokens[self.index][0] == "}":
            self.semantic_class.destroyScope()
            self.index += 1
            if self.S0():
                return True
        elif self.S_CB():
            return True
        return False

    def S_CB(self):
        if self.tokens[self.index][1] == "public":
            self.Am=self.tokens[self.index][1]
            self.index += 1
            if self.B1():
                return True
        elif self.tokens[self.index][1] == "private":
            self.Am=self.tokens[self.index][1]
            self.index += 1
            if self.B2():
                if self.D1():
                    return True
        elif self.tokens[self.index][1] == "protected":
            self.Am=self.tokens[self.index][1]
            self.index += 1
            if self.B2():
                if self.D1():
                    return True
        elif self.B7():
            if self.D1():
                return True
        return False

    def B1(self):
        if self.tokens[self.index][0] == "static":
            self.cTm=self.tokens[self.index][1]
            self.index += 1
            if self.B3():
                return True
        elif (self.tokens[self.index][1] == "virtual" or
        self.tokens[self.index][1] == "override"):
            self.cTm=self.tokens[self.index][1]
            self.index += 1
            if self.B4():
                if self.D1():
                    return True
        elif self.B4():
            if self.D1():
                return True
        return False

    def B3(self):
        if (self.tokens[self.index][1] == "virtual" or
        self.tokens[self.index][1] == "override"):
            self.cTm=self.tokens[self.index][1]
            self.index += 1
            if self.B4():
                if self.D1():
                    return True
        elif self.B13():
            return True
        return False

    def B13(self):
        if self.tokens[self.index][0] == "void":
            self.T=self.tokens[self.index][1]
            self.index += 1
            if self.B5():
                return True
        elif self.tokens[self.index][0] == "DT":
            self.T=self.tokens[self.index][1]
            self.index += 1
            if self.B9():
                if self.D1():
                    return True
        elif self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.B11():
                if self.D1():
                    return True
        return False

    def B5(self):
        if self.tokens[self.index][0] == "main":
            self.index += 1
            if self.B6():
                return True
        elif self.B10():
            if self.D1():
                return True
        return False

    def B6(self):
        if self.tokens[self.index][0] == "(":
            self.index += 1
            if self.tokens[self.index][0] == ")":
                self.index += 1
                if self.body():
                    if self.D():
                        return True
        return False

    def B2(self):
        if self.tokens[self.index][0] == "static":
            self.cTm=self.tokens[self.index][1]
            self.index += 1
            if self.B8():
                return True
        elif (self.tokens[self.index][1] == "virtual" or
        self.tokens[self.index][1] == "override"):
            self.cTm=self.tokens[self.index][1]
            self.index += 1
            if self.B4():
                return True
        elif self.B4():
            return True
        return False

    def B8(self):
        if (self.tokens[self.index][1] == "virtual" or
        self.tokens[self.index][1] == "override"):
            self.cTm=self.tokens[self.index][1]
            self.index += 1
            if self.B4():
                return True
        elif self.B4():
            return True
        return False

    def B4(self):
        if self.tokens[self.index][0] == "void":
            self.T=self.tokens[self.index][1]
            self.index += 1
            if self.B10():
                return True
        elif self.tokens[self.index][0] == "DT":
            self.T=self.tokens[self.index][1]
            self.index += 1
            if self.B9():
                return True
        elif self.tokens[self.index][0] == "ID":
            self.cName=self.tokens[self.index][1]
            self.index += 1
            if self.B11():
                return True
        return False

    def B9(self):
        if self.tokens[self.index][0] == "[":
            self.index += 1
            if self.tokens[self.index][0] == "]":
                self.index += 1
                if self.br():
                    if self.B10():
                        return True
        elif self.tokens[self.index][0] == "ID":
            self.cName=self.tokens[self.index][1]
            self.index += 1
            if self.A16():
                return True
        return False

    def B11(self):
        if self.B10():
            return True
        elif self.tokens[self.index][0] == "[":
            self.index += 1
            if self.tokens[self.index][0] == "]":
                self.index += 1
                if self.br():
                    if self.B10():
                        return True
        return False

    def B12(self):
        if self.tokens[self.index][0] == "(":
            self.index += 1
            if self.param():
                if self.tokens[self.index][0] == ")":
                    self.index += 1
                    if self.body():
                        return True
        return False

    def B10(self):
        if self.fun2_body():
            return True
        return False

    def B19(self):
        if self.B12():
            return True
        elif self.tokens[self.index][1] == "=":
            self.index += 1
            if self.tokens[self.index][0] == "new":
                self.index += 1
                if self.tokens[self.index][0] == "ID":
                    self.index += 1
                    if self.tokens[self.index][0] == "(":
                        self.index += 1
                        if self.arg():
                            if self.tokens[self.index][0] == ")":
                                self.index += 1
                                if self.tokens[self.index][0] == ";":
                                    self.index += 1
                                    return True
        return False

    def B7(self):
        if self.tokens[self.index][0] == "static":
            self.cTm=self.tokens[self.index][1]
            self.index += 1
            if self.B14():
                return True
        elif (self.tokens[self.index][1] == "virtual" or
        self.tokens[self.index][1] == "override"):
            self.cTm=self.tokens[self.index][1]
            self.index += 1
            if self.B4():
                return True
        elif self.B15():
            return True
        return False

    def B14(self):
        if (self.tokens[self.index][1] == "virtual" or
        self.tokens[self.index][1] == "override"):
            self.cTm=self.tokens[self.index][1]
            self.index += 1
            if self.B4():
                return True
        if self.B4():
            return True
        return False

    def B15(self):
        if self.tokens[self.index][0] == "void":
            self.T=self.tokens[self.index][1]
            self.index += 1
            if self.B10():
                return True
        elif self.tokens[self.index][0] == "DT":
            self.T=self.tokens[self.index][1]
            self.index += 1
            if self.B16():
                return True
        elif self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.B17():
                return True
        return False

    def B16(self):
        if self.tokens[self.index][0] == "[":
            self.index += 1
            if self.tokens[self.index][0] == "]":
                self.index += 1
                if self.br():
                    if self.B18():
                        return True
        elif self.tokens[self.index][0] == "ID":
            self.cName=self.tokens[self.index][1]
            self.index += 1
            if self.A16():
                return True
        return False

    def B18(self):
        if self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.A15():
                return True
        return False

    def B17(self):
        if self.tokens[self.index][0] == "[":
            self.index += 1
            if self.tokens[self.index][0] == "]":
                self.index += 1
                if self.br():
                    if self.B10():
                        return True
        elif self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.B19():
                return True
        elif self.B12():
            return True
        return False
   

    def S1(self):
        if self.tokens[self.index][0] == "abstract":
            self.Cat=self.tokens[self.index][0]
            self.index += 1
            if self.tokens[self.index][0] == "class":
                self.T=self.tokens[self.index][0]
                self.index += 1
                if self.tokens[self.index][0] == "ID":
                    self.N=self.tokens[self.index][1]
                    self.index += 1
                    if self.inherit():
                        if self.tokens[self.index][0] == "{":
                            self.semantic_class.createScope()
                            self.index += 1
                            if self.C():
                                return True
        elif self.seal():
            if self.tokens[self.index][0] == "class":
                self.T=self.tokens[self.index][0]
                self.index += 1
                if self.tokens[self.index][0] == "ID":
                    self.N=self.tokens[self.index][1]
                    self.index += 1
                    if self.inherit():
                        if self.tokens[self.index][0] == "{":
                            self.index += 1
                            if self.D():
                                return True
        elif self.tokens[self.index][0] == "class":
            self.T=self.tokens[self.index][0]
            self.index += 1
            if self.tokens[self.index][0] == "ID":
                self.N=self.tokens[self.index][1]
                self.index += 1
                if self.inherit():
                    if self.tokens[self.index][0] == "{":
                        self.semantic_class.createScope()
                        self.index += 1
                        if self.D():
                            return True
        return False

    def S2(self):
        if self.S1():
            return True
        elif self.tokens[self.index][0] == "$":
            return True
        return False

    def D(self):
        if self.tokens[self.index][0] == "}":
            self.semantic_class.destroyScope()
            self.index += 1
            if self.S2():
                return True
        elif self.CB():
            return True
        return False

    def HCB(self):
        if self.tokens[self.index][1] == "public":
            self.Am=self.tokens[self.index][1]
            self.index += 1
            if self.A2():
                if self.C():
                    return True
        elif self.tokens[self.index][1] == "private":
            self.Am=self.tokens[self.index][1]
            self.index += 1
            if self.A2():
                if self.C():
                    return True
        elif self.tokens[self.index][1] == "protected":
            self.Am=self.tokens[self.index][1]
            self.index += 1
            if self.A2():
                if self.C():
                    return True
        elif self.A8():
            if self.C():
                return True
        return False

    def CB(self):
        if self.tokens[self.index][1] == "public":
            self.Am=self.tokens[self.index][1]
            self.index += 1
            if self.B2():
                if self.D():
                    return True
        elif self.tokens[self.index][1] == "private":
            self.Am=self.tokens[self.index][1]
            self.index += 1
            if self.B2():
                if self.D():
                    return True
        elif self.tokens[self.index][1] == "protected":
            self.Am=self.tokens[self.index][1]
            self.index += 1
            if self.B2():
                if self.D():
                    return True
        elif self.B7():
            if self.D():
                return True
        return False

 ########################################### ENUM ######################################################
    
    def enum(self):
        if self.tokens[self.index][0] == "enum" and self.tokens[self.index+1][0]=="ID" and self.tokens[self.index+2][1]=="{":
            self.index+=3
            if self.E_B():
                    
                    
             
                    return True
     



        return False
    def E_B(self):
        if self.tokens[self.index][0]=="ID" and self.tokens[self.index+1][1]=="}":
            self.index+=2
            return True
        elif self.tokens[self.index][0]=="ID" and self.tokens[self.index+1][1]==",":
            self.index+=2
            if self.E_B():
                return True
      
        return False
    def enum_call(self):
        if self.tokens[self.index][0] == "ID":
            self.index += 1
            if self.tokens[self.index][0] == "ID":
                self.index += 1
                if self.tokens[self.index][1] == "=":
                    self.index += 1
                    if self.tokens[self.index][0] == "ID":
                        self.index += 1
                        if self.tokens[self.index][1] == ".":
                            self.index += 1
                            if self.tokens[self.index][0] == "ID":
                                self.index += 1
                                if self.tokens[self.index][1] == ";":
                                    self.index += 1
                                    return True
        return False
  

            

       










    ##############STARTING###########
    def S(self):
            if self.class_state():
                return True
            elif self.SST():
                return True
           
            elif self.enum():
                return True
            # self.semantic.print()   
            return False

    def S0(self):
            while self.tokens[self.index][0] != "$":
                if not(self.S()):
                   return False
            # self.semantic.print()   
            
            return True
    
    ###########################################OBJECT AND ARRAY IMPLEMENTATION################################################
    
    def FuncVar(self):
        # print("FuncVar")
        if (self.tokens[self.index][1] in ";,)]ϵ+-" or self.tokens[self.index][1] in [">=", "<=", "==", ">", "<", "!="] or self.tokens[self.index][1] == "||" or self.tokens[self.index][1] == "&&"):
            # var = self.semantic.LookUpST(self.getPreviousToken(),"")
            # self._evaluatedType_ = var["Type"]
            # self.compare()

            return True
        # if (self.tokens[self.index][1] in ";,)]ϵ"):
        #     return True
        # if (self.tokens[self.index][1] == ";"):
        #     return True
        if (self.tokens[self.index][1] == "("):
            if (self.FunctionCall()):
                return True
        if (self.tokens[self.index][1] in ".["):
            # var = self.semantic.LookUpST(self.getPreviousToken(),"")
            # self._evaluatedType_ = var["Type"]
            # self.compare()
            if (self.ReferenceAccess()):
                return True
        return False

    def FunctionCall(self):
        # print("FunctionCall")
        if (self.tokens[self.index][1] == ";"):
            return True
        if (self.tokens[self.index][1] == "("):
            # self._functionCall_["N"] = self.getPreviousToken()
            self.advance()
            if (self.Params()):
                if (self.tokens[self.index][1] == ")"):
                    # var = self.semantic.LookUpST(self._functionCall_["N"],self._functionCall_["PL"])
                    # self._evaluatedType_ = var["T"]
                    self._functionCall_["N"] = ""
                    self._functionCall_["PL"] = ""

                    # self.compare()
                    self.advance()
                    if (self.ReferenceAccess()):
                        return True
        return False

    def New_(self):
        # print("New_")
        if (self.ReferenceAccess()):
            return True
        if (self.tokens[self.index][1] == "("):
            # self._functionCall_["N"] = self.getPreviousToken()
            self.advance()
            if (self.Params()):
                if (self.tokens[self.index][1] == ")"):
                    # var = self.semantic.LookUpFunctionMT(self._CRef_,self._functionCall_["N"],self._functionCall_["PL"])
                    # self._evaluatedType_ = var["T"]
                    # self._CRef_ = self._evaluatedType_
                    self.advance()
                    if (self.ReferenceAccess()):
                        return True
        return False

    def arrayAccess(self):
        # print("arrayAccess")
        if (self.tokens[self.index][1] == "["):
            #LOOKUP USING REF IMPLEMENTED HERE
            if(self._CRef_ != ""):
                if(self._functionCall_["N"] == ""):
                    # var = self.semantic.LookUpVarMT(self._CRef_,self.getPreviousToken())
                    # self._evaluatedType_ = var["Type"]
                    pass
                else:
                    # var = self.semantic.LookUpFunctionMT(self._CRef_,self._functionCall_["N"],self._functionCall_["PL"])
                    # self._evaluatedType_ = var["T"]
                    self._functionCall_["N"] = ""
                    self._functionCall_["PL"] = ""
                # pass
            self._CRef_ = self._evaluatedType_
            #LOOKUP USING REF IMPLEMENTED HERE
            # if("[]" not in self._evaluatedType_):
            #     raise IndexError(f"Indexing can not be applied to type {self._evaluatedType_}")
            
            self.advance()
            if (self.OE()):
                # self.advance()
                # self.tokens[self.index][1] = self.tokens[self.index][1]
                # if(self._evaluatedType_ not in ["Numeric","num"] ):
                #     raise KeyError(f"Invalid Key at Line:{self.current_line}, column:{self.current_col}")
                if (self.tokens[self.index][1] == "]"):
                    self.advance()
                    # self._evaluatedType_ = self._CRef_[0:(len(self._CRef_)-2)] if self.tokens[self.index][1] != "[" else self._CRef_
                    self._CRef_ = ""
                    return self.ReferenceAccess()
        return False

    def MemberAccess(self):
        # print("MemberAccess")
        if (self.tokens[self.index][1] == "."):
            if(self._CRef_ != ""):
                if(self._functionCall_["N"] == ""):
                    # var = self.semantic.LookUpVarMT(self._CRef_,self.getPreviousToken())
                    pass
                    # self._evaluatedType_ = var["Type"]
                else:
                    # var = self.semantic.LookUpFunctionMT(self._CRef_,self._functionCall_["N"],self._functionCall_["PL"])
                    # self._evaluatedType_ = var["T"]
                    self._functionCall_["N"] = ""
                    self._functionCall_["PL"] = ""
                
            self._CRef_ = self._evaluatedType_
            self.advance()
            if (self.Class == "ID"):
                self.advance()
                return self.New_()
        return False

    def ReferenceAccess(self):
        # print("ReferenceAccess")
        if (self.tokens[self.index][1] in ";=)]," or self.tokens[self.index][1] in ["+", "-", "/", "%", "*",
                         "^","<", ">", "!", ">=", "<=", "==", "!=", "&&", "||"]):
            #CHECK CLASS REFERENCE HERE
            if(self._CRef_ != ""):
                if(self._functionCall_["N"] == ""):
                    # var = self.semantic.LookUpVarMT(self._CRef_,self.getPreviousToken())
                    # self._evaluatedType_ = var["Type"]
                    pass
                else:
                    # var = self.semantic.LookUpFunctionMT(self._CRef_,self._functionCall_["N"],self._functionCall_["PL"])
                    # self._evaluatedType_ = var["T"]
                    self._functionCall_["N"] = ""
                    self._functionCall_["PL"] = ""
            # self.compare()
            return True

        if (self.tokens[self.index][1] == "["):
            return self.arrayAccess()
        elif (self.MemberAccess()):
        # self._CRef_ = self._evaluatedType_
        # if(self.MemberAccess()):
            return True
            # return self.MemberAccess()
        return False


    def Params(self):
        # print("Params")
        if (self.tokens[self.index][1] == ")"):
            self._functionCall_["PL"] = "-"
            return True
        if (self.OE()):
            if(self._functionCall_["PL"] == ""):
                self._functionCall_["PL"] = self.formatType(self._evaluatedType_)
            else:
                self._functionCall_["PL"] += ","+self.formatType(self._evaluatedType_)
            if (self.ParamList()):
                return True
        return False

    def ParamList(self):
        # print("ParamList")
        if (self.tokens[self.index][1] == ")"):
            return True

        if (self.tokens[self.index][1] == ","):
            self.advance()
            if (self.Params()):
                return True
        return False

    ###########################################OBJECT AND ARRAY IMPLEMENTATION################################################