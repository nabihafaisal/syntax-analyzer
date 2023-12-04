###################SEMANTIC CLASS#####################################
class MainTable:
    def __init__(self):
        self.name = None
        self.type = None
        self.access_modifier = None
        self.category = None
        self.parent = None
        self.link = []

    def __str__(self):
        return f"\n MainTable" \
               f"name='{self.name}'," \
               f" type='{self.type}'," \
               f" access_modifiers='{self.access_modifier}'," \
               f" Category='{self.category}'," \
               f" link={self.link}" \
               f"\n"

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, MainTable):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

class FunctionTable:
    def __init__(self):
        self.name = None
        self.type = None
        self.scope = 0

    def __str__(self):
        return f"FunctionTable" \
               f" name='{self.name}'," \
               f" type='{self.type}'," \
               f" scope={self.scope}" \
               f" "

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, FunctionTable):
            return False
        return self.scope == other.scope and self.name == other.name

    def __hash__(self):
        return hash((self.name, self.scope))

class BodyTable:
    def __init__(self):
        self.name = None
        self.type = None
        self.access_modifier = None
        self.type_modifier = None

    def __str__(self):
        return f"\n BodyTable" \
               f" name='{self.name}'," \
               f" type='{self.type}'," \
               f" access_modifier='{self.access_modifier}'," \
               f" type_modifier='{self.type_modifier}'" \
               f"\n"

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, BodyTable):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)



class SemanticClass:
    def __init__(self):
        self.Am = "private"
        self.Tm = None
        self.Cat = None
        self.scopeno = 0
        self.scope = []
        self.mainTable = []
        self.functionTable = []

    def create_DT(self):
        return []

    def insert_MT(self, name, type, access_modifier, category, parent, link):
        maintable = {
            'name': name,
            'type': type,
            'access_modifier': access_modifier,
            'category': category,
            'parent': parent,
            'link': link
        }
        if maintable not in self.mainTable:
            self.mainTable.append(maintable)
          
            
            return True
        else:
            print(f"Redeclaration {maintable['type']}:{maintable['name']}")
            return False

    def insert_DT(self, name, type, typemodifier, accessmodifier, link):
        bodyTable = {
            'name': name,
            'type': type,
            'type_modifier': typemodifier,
            'access_modifier': accessmodifier,
            'link': link

        }
        if bodyTable not in link:
            link.append(bodyTable)
         
            return True
        else:
            print(f"Variable '{bodyTable['name']}' is already defined in this scope")
            return False

    def insert_FT(self, name, type):
        functionTable = {
            'name': name,
            'type': type,
            'scope': self.scopeno
        }
        if functionTable not in self.functionTable :
   
              
                    self.functionTable.append(functionTable)
                   
                    return True
        
        else:
            print(f"Variable '{functionTable['name']}' is already defined in this scope")
            return False
   

 



    



    def lookup_MT(self, name):
        for var in self.mainTable:
            if var['name'] == name:
                self.Am = var['access_modifier']
                self.Cat = var['category']
                return var['type']
        return "null"

    def lookup_att_DT(self, name, link):
        for var in link:
            if var['name'] == name:
                return var['type']
        return "null"

    def lookup_fn_DT(self, name, link):
        for var in link:
            if var['name'] == name:
                return var['type']
        return "null"

    def lookup_FT(self, name):
        for var in self.functionTable:
            if var['name'] == name:
                return var['type']
        return "null"

    def compatibility(self,T1, T2, opr):
        if T1 == "int" and T2 == "int":
            if opr == "*" or opr == "/" or opr == "+" or opr == "-":
                return "int"

        if (T1 == "int" and T2 == "float") or (T2 == "int" and T1 == "float"):
            if opr == "*" or opr == "/" or opr == "-" or opr == "+":
                return "float"

        if T1 == "string" and T2 == "string":
            if opr == "+":
                return "string"

        if T1 == "character" and T2 == "character":
            if opr == "+":
                return "Alpha"

        if (T1 == "string" and T2 == "character") or (T2 == "string" and T1 == "character"):
            if opr == "+":
                return "string"

        if opr == "or" or opr == "and":
            return "bool"

        if opr == "==" or opr == "!=" or opr == ">=" or opr == "<=" or opr == "<" or opr == ">":
            return "bool"

        return "type mismatched"


    def compatibility1(self):
        pass

    def createScope(self):
        self.scopeno+=1
        
        self.scope.append(self.scopeno)
       
      

    def destroyScope(self):
        self.scopeno-=1
        self.scope.pop()