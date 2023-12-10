# Semantic implementation
from prettytable import PrettyTable
class Semantic:
    def __init__(self):
        self.currentScopeId = 0
        self.scopeStack = [0]
        self.definitionTable = []
        self.scopeTable = []
        self.memberTables = {}

    def formatType(self,T):
        if(T == "Numeric"):
            return "num"
        elif(T == "String"):
            return "str"
        else:
            return T

    def appendScope(self):
        self.advanceScope()
        self.scopeStack.append(self.currentScopeId)

    def popScope(self):
        self.lessScope()
        self.scopeStack.pop()

    def advanceScope(self):
        self.currentScopeId += 1
    def lessScope(self):
        self.currentScopeId -=1

    def insertST(self,N,T):
        for i in self.scopeTable:
            if N == i["Name"] and i["Scope"] == self.scopeStack[-1]:
                print(f"{N} already defined")
                exit()
        self.scopeTable.append({"Name":N,"Type":T,"Scope":self.scopeStack[-1]})        

    def insertFunctionST(self,N,T):
        for i in self.scopeTable:
            if N == i["Name"] and i["Scope"] == self.scopeStack[-2]:
                print(f"{N} already defined")
                exit()
        self.scopeTable.append({"Name":N,"Type":T,"Scope":self.scopeStack[-2]})

    
    def insertVarDTInST(self,T):
        for i in self.scopeTable:
            if i["Type"] == '-':
                i["Type"] = T

########################### END #########################################
########################### CLASS #########################################

    def insertDT(self,N,T,CM,P,AM):
        for i in self.definitionTable:
            if N == i["Name"] and i["Scope"] == self.scopeStack[-1]:
                print(f"{N} already defined")
                exit()
        self.definitionTable.append({"Name":N,"Type":T,"Scope":self.scopeStack[-1],"Parent":P,"AM":AM,"CM":CM})
        self.memberTables[N] = []
        if(T=="class"):
            self.insertDefaultConstructorInMT(N)

    def checkObjectAssignment(self, N, T):
        if len(self.definitionTable) == 0:
            print(f"{N}: No such class in the current scope")
            exit()

        var = self.getEntryFromDT(N)

        if var is not None:
            if N == T:
                if (var["Name"] == N or var["Parent"] == T) and var["CM"] != "abstract":
                    return var
            elif var["Parent"] is not None:
                return self.checkObjectAssignment(var["Parent"], T)

        print(f"{N}: Invalid type casting")
        exit()

    def checkParentClass(self,N):
        if(len(self.definitionTable) == 0):
            print(f"{N}: No such class in current scope")
            exit()
        for i in self.definitionTable:
            if N == i["Name"] and i["Scope"] in self.scopeStack:
                if(i["CM"] == "sealed"):
                    print(f"\n{N}: Cannot Inherit Sealed class")
                    exit()
                return
        print(f"{N}: No such class in current scope")
        exit()

    def insertDefaultConstructorInMT(self,N):
        self.insertMT(N,N+" --> -",'public',None,N)

    def getEntryFromDT(self,N):
        for i in self.definitionTable:
            if N == i["Name"] and i["Scope"] in self.scopeStack:
                return i
    
########################### END #########################################

########################### CLASS #########################################

    def insertMT(self,N,T,AM,TM,R):
        for i in self.memberTables[R]:
            if('-->' not in i["Type"] and '-->' not in T):
                if(i["Name"]==N):
                    print(f"{N} is already declared in {R}")
                    exit()
            else:
                if(i["Name"]==N and i["Type"].split("-->")[1].strip()==T.split("-->")[1].strip()):
                    print(f"{N} is already declared in {R}")
                    exit()
                pass
        self.memberTables[R].append({"Name":N,"Type":T,"AM":AM,"TM":TM})

    def insertVarDTInMT(self,T,R):
        for i in self.memberTables[R]:
            if i["Type"] == '-':
                i["Type"] = T
########################### END #########################################

########################### COMPARSION #########################################
    def Compare(self,T1,T2,OP):
        #REMOVE IT LATER
        if(T1=='null'):
            return  {"T":T1}
        print("compared")
        if(OP in ["+", "-", "/", "%", "*","^", "&&", "||"]):
            if(T1 == T2 and (T1 == "string") and OP == "+"):
                return {"T":T1}
            if(T1 == T2 and (T1 == "int" or T1 == 'float')):
                return {"T":T1}
            elif((T1 == "float" and T2 == "int") or (T2 == "float" and T1 == "int")):
                return {"T":"float"}
            else:
                print(f"Type Mismatched {T1} and {T2}")
                exit()
        if(OP in ["<", ">", "!", ">=", "<=", "==", "!="]):
            if(T1 == T2 ):
                return {"T":"bool"}
            else:
                print(f"Type Mismatched {T1} and {T2}")
                exit()
########################### COMPARSION #########################################

########################### LOOKUP #########################################
    def LookUpST(self,N,T):
        T = self.formatType(T)
        for i in self.scopeStack:
            for j in self.scopeTable:
                try:
                    if(j["Name"] == N and j["Type"].split("-->")[1].strip() == T and j["Scope"] == i ):
                        j["T"] = j["Type"].split("-->")[0].strip()
                        return j
                except:
                    if(j["Name"] == N and j["Scope"] == i):
                        if(T == ""):
                            return j
        print(f"{N} does not exists") 
        exit()
    
    def LookUpVarMT(self,Ref,N):
        # print('lookup')
        try:
            for i in self.memberTables[Ref]:
                if(i["Name"] == N and i["AM"] == "public"):
                    return i
            for i in self.getEntryFromDT(Ref)["Parent"].split("-"):
                return self.LookUpVarMT(i,N)
                # for j in self.memberTables[i]:
                #     if(j["Name"] == N and j["AM"] == "public"):
                #         return j
        except:
            pass
        print(f"Property or method {N} does not exists on type {Ref}") 
        exit()
    
    def LookUpFunctionMT(self,Ref,N,T):
        try:
            for i in self.memberTables[Ref]:
                if("-->" in i["Type"]):
                    if(i["Name"] == N and i["AM"] == "public" and i["Type"].split("-->")[1].strip() == T):
                        j = {**i,"T":i["Type"].split("-->")[0].strip()}
                        return j
            for i in self.getEntryFromDT(Ref)["Parent"].split("-"):
                return self.LookUpFunctionMT(i,N,T)
        except:
            pass
        print(f"Method {N}({''if T == '-' else T}) does not exists on type {Ref}") 
        exit()
########################### LOOKUP #########################################

    def checkDT(self,DT):
        if(DT in ['num','str','bool','num[]','str[]','bool[]']):
            return True
        else:
            for i in self.definitionTable:
                if(i["Name"] == DT or i["Name"]+"[]" == DT):
                    return True
        return False

    # def print(self):
    #     # return
    #     print("\nSCOPE TABLE")
    #     for i in self.scopeTable:
    #         print(i)
            
    #     print("\nDEFINITION TABLE")
    #     for i in self.definitionTable:
    #         print(i)
        
    #     print("\nMEMBER TABLE")
    #     for i in self.memberTables:
    #         print(i)
    #         for j in self.memberTables[i]:
    #             print(j)

######################### USELESS FUNCTIONS ############################################

    
    def create_DT(self):
       
      
       return []
    
    def add_default_constructor(self,name,link):
        default_constructor = {
            'name': name,
            'type': 'void',
            'type_modifier': None,
            'access_modifier': 'public',
            
        }
        link.append(default_constructor)
######################### USELESS FUNCTIONS ############################################
    def print(self):
        # SCOPE TABLE
        print("\nSCOPE TABLE")
        scope_table = PrettyTable(["Name", "Type", "Scope"])
        for i in self.scopeTable:
            scope_table.add_row([i["Name"], i["Type"], i["Scope"]])
        print(scope_table)

        # DEFINITION TABLE
        print("\nDEFINITION TABLE")
        definition_table = PrettyTable(["Name", "Type", "Scope", "Parent", "AM", "CM"])
        for i in self.definitionTable:
            definition_table.add_row([i["Name"], i["Type"], i["Scope"], i["Parent"], i["AM"], i["CM"]])
        print(definition_table)

        # MEMBER TABLE
        print("\nMEMBER TABLE")
        for class_name, member_table in self.memberTables.items():
            class_table = PrettyTable(["Name", "Type", "AM", "TM"])
            for member in member_table:
                class_table.add_row([member["Name"], member["Type"], member["AM"], member["TM"]])
            print(f"\n{class_name}")
            print(class_table)
