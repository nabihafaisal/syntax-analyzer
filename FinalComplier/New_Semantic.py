# Semantic implementation
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
        self.scopeStack.pop()

    def advanceScope(self):
        self.currentScopeId += 1

    def insertST(self,N,T):
        for i in self.scopeTable:
            if N == i["Name"] and i["Scope"] == self.scopeStack[-1]:
                raise NameError(f"{N} already defined")
        self.scopeTable.append({"Name":N,"Type":T,"Scope":self.scopeStack[-1]})        

    def insertFunctionST(self,N,T):
        for i in self.scopeTable:
            if N == i["Name"] and i["Scope"] == self.scopeStack[-2]:
                raise NameError(f"{N} already defined")
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
                raise NameError(f"{N} already defined")
        self.definitionTable.append({"Name":N,"Type":T,"Scope":self.scopeStack[-1],"Parent":P,"AM":AM,"CM":CM})
        if(T=="class"):
            self.insertDefaultConstructorInST(N)
        self.memberTables[N] = []

    def checkParentInterface(self,N):
        if(len(self.definitionTable) == 0):
            raise NameError(f"{N}: No such interface in current scope")
        for i in self.definitionTable:
            if N == i["Name"] and i["Scope"] in self.scopeStack:
                if(i["Type"] != "Interface"):
                    raise NameError(f"\n{N}: Invalid parent")
                return
        raise NameError(f"{N}: No such interface in current scope")

    def checkParentClass(self,N):
        if(len(self.definitionTable) == 0):
            raise NameError(f"{N}: No such interface in current scope")
        for i in self.definitionTable:
            if N == i["Name"] and i["Scope"] in self.scopeStack:
                if(i["CM"] == "sealed"):
                    raise TypeError(f"\n{N}: Cannot Inherit Sealed class")
                return
        raise NameError(f"{N}: No such interface in current scope")

    def insertDefaultConstructorInST(self,N):
        self.insertST(N,N+" --> -")

    def getEntryFromDT(self,N):
        for i in self.definitionTable:
            if N == i["Name"] and i["Scope"] in self.scopeStack:
                return i
    
########################### END #########################################

########################### CLASS #########################################

    def insertMT(self,N,T,AM,TM,R):
        for i in self.memberTables[R]:
            if(i["Name"]==N):
                raise NameError(f"{N} is already declared in {R}")
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
                raise TypeError(f"Type Mismatched {T1} and {T2}")
        if(OP in ["<", ">", "!", ">=", "<=", "==", "!="]):
            if(T1 == T2 ):
                return {"T":"bool"}
            else:
                raise TypeError(f"Type Mismatched {T1} and {T2}")
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
        raise LookupError(f"{N} does not exists") 
    
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
        raise LookupError(f"Property or method {N} does not exists on type {Ref}") 
    
    def LookUpFunctionMT(self,Ref,N,T):
        try:
            for i in self.memberTables[Ref]:
                if(i["Name"] == N and i["AM"] == "public" and T in i["Type"]):
                    i["T"] = i["Type"].split("-->")[0].strip()
                    return i
            for i in self.getEntryFromDT(Ref)["Parent"].split("-"):
                return self.LookUpFunctionMT(i,N,T)
        except:
            pass
        raise LookupError(f"Method {N}() does not exists on type {Ref}") 
########################### LOOKUP #########################################

    def checkDT(self,DT):
        if(DT in ['num','str','bool','num[]','str[]','bool[]']):
            return True
        else:
            for i in self.definitionTable:
                if(i["Name"] == DT or i["Name"]+"[]" == DT):
                    return True
        return False

    def print(self):
        # return
        print("\nSCOPE TABLE")
        for i in self.scopeTable:
            print(i)
            
        print("\nDEFINITION TABLE")
        for i in self.definitionTable:
            print(i)
        
        print("\nMEMBER TABLE")
        for i in self.memberTables:
            print(i)
            for j in self.memberTables[i]:
                print(j)

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