import pandas 
import numpy as np
import math  
import csv



csv_data = pandas.read_csv("data.csv")
s = {'Yes' : 1 , 'No' : 0 }
csv_data['Hun'] = csv_data['Hun'].map(s)
csv_data['Bar'] = csv_data['Bar'].map(s)
csv_data['Alt'] = csv_data['Alt'].map(s)
csv_data["Fri"] = csv_data["Fri"].map(s)
csv_data['Rain'] = csv_data['Rain'].map(s)
csv_data['Res'] = csv_data['Res'].map(s)
csv_data['Wait'] = csv_data['Wait'].map(s)



csvdata = []
for row in csv_data.values:
    csvdata.append(row)

class node:
    def __init__(self,a, childs, examples, parent, survived=None):
        self.a = a
        self.examples = examples
        self.childs = childs
        self.parent = parent
        self.survived = survived

def Entropy(childs):
    Y = 0
    N = 0
    result = 0 
    totalnumber = 0
    for j in range(len(childs)):
        totalnumber += len(childs[j].examples)
    for nd in childs:
        Y = 0
        N = 0
        for i in nd.examples:
            if i[10]==1:
                Y+=1
            else:
                N+=1
        if (N==0 or Y==0):
            result += 0
        else:
            result += (len(nd.examples)/totalnumber)*(Y/(Y+N)) *(math.log2((Y+N)/Y))
    return result
        





def Entropy1(Node):
    Y = 0
    N = 0
    for i in Node.examples:
        if i[10]==1:
            Y+=1
        else:
            N+=1
    if (N==0 or Y==0):
        return 0
    else:
        return (Y/(Y+N)) *(math.log2((Y+N)/Y))

        
                    
            
def gini_index(childs):
    Y = 0
    N = 0
    result = 0 
    totalnumber = 0
    for j in range(len(childs)):
        totalnumber += len(childs[j].examples)
    for nd in childs:
        for i in nd.examples:
            if i[10]==1:
                Y+=1
            N+=1
        if (N==0 or Y==0):
            result += 0
        else:
            result += (len(nd.examples)/totalnumber)*((Y/(Y+N))*(1-(Y/(Y+N))) + (N/(Y+N))*(1-(N/(Y+N))))
    return result

        
def Hun(Node):
    list1=[]
    list2=[]

    for e in Node.examples:
        if e[3] == 0:
            list1.append(e)
        elif e[3] == 1:
            list2.append(e)
    return [node(None,None,list1,Node),node(None,None,list2,Node)]

def Rain(Node):
    list1=[]
    list2=[]

    for e in Node.examples:
        if e[6] == 1:
            list1.append(e)
        elif e[6] == 0:
            list2.append(e)
    return [node(None,None,list1,Node),node(None,None,list2,Node)]

def Bar(Node):
    list1=[]
    list2=[]

    for e in Node.examples:
        if e[1] == 0:
            list1.append(e)
        elif e[1] == 1:
            list2.append(e)
    return [node(None,None,list1,Node),node(None,None,list2,Node)]

def Fri(Node):
    list1=[]
    list2=[]

    for e in Node.examples:
        if e[2] == 1:
            list1.append(e)
        elif e[2] == 0:
            list2.append(e)
    return [node(None,None,list1,Node),node(None,None,list2,Node)]

def Alt(Node):
    list1=[]
    list2=[]

    for e in Node.examples:
        if e[0] == 1:
            list1.append(e)
        elif e[0] == 0:
            list2.append(e)
    return [node(None,None,list1,Node),node(None,None,list2,Node)]

def Res(Node):
    list1=[]
    list2=[]

    for e in Node.examples:
        if e[7] == 1:
            list1.append(e)
        elif e[7] == 0:
            list2.append(e)
    return [node(None,None,list1,Node),node(None,None,list2,Node)]



def Patrons(Node):
    list1=[]
    list2=[]
    list3=[]
    for e in Node.examples:
        if(e[4]=="Some"):
            list1.append(e)
        elif(e[4]=="Full"):
            list2.append(e)
        elif(e[4] == "None"):
            list3.append(e)
    return [node(None,None,list1,Node),node(None,None,list2,Node),node(None,None,list3,Node)]  

def Est(Node):
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    for e in Node.examples:
        if(e[9] == "0-10"):
            list1.append(e)
        elif(e[9]=="10-30"):
            list2.append(e)
        elif( e[9]=="30-60"):
            list3.append(e)
        elif(e[9] == ">60"):
            list4.append(e)
      
        
    return [node(None,None,list1,Node)
            ,node(None,None,list2,Node)
            ,node(None,None,list3,Node)
            ,node(None,None,list4,Node)]
            




ListOfattributes = [Alt,Hun,Res, Est,Rain,Patrons,Fri,Bar]
Root = node(None,None,csvdata,None)

def whichquestion2ask(Node,ListOfattributes,Entropy):
    entropy = 1
    selectedQuestion = None
    for a in ListOfattributes:
        Node.childs = a(Node)
        e = Entropy(Node.childs)
        if e < entropy:
            entropy = e
            selectedQuestion = a

    Node.childs = selectedQuestion(Node)
    Node.a = selectedQuestion

    return Node


def check(Node):
    y = 0
    n = 0
    if (Node !=None and Node.examples != None):
        for i in Node.examples:
            if (i[10] == 1):
                y+=1
            else:
                n += 1 
        if y>n:
            return True
        elif n>y:
            return False
        else:
            if(Node.parent!=None):
                return check(Node.parent)
    if(Node.parent!=None):
        return check(Node.parent)
    else:
        return False


def makedecisiontree(node,attributes):
    if (len(attributes)==0):
        node.survived = check(node)
        return None
    if (len(node.examples ) ==0 ):
        node.survived = check(node.parent)
        return None
    node = whichquestion2ask(node,attributes,Entropy)
    for child in node.childs:
        makedecisiontree(child,list(filter(lambda s: s!= node.a,attributes)))
    return node

makedecisiontree(Root,ListOfattributes)


def harrass(Node):
    if((Node.childs)!=None):
        for ch in Node.childs:
            harrass(ch)

    else:
       
       if(Node.parent.childs!=None and (Entropy1(Node.parent) - Entropy(Node.parent.childs)) < 0.02):
           Node.parent.childs = None
           Node.parent.survived = check(Node.parent)
           return None
    
        
harrass(Root)


newnode = node(None,None,[csv_data.values[3]],None)


def isAlive(person,Root):
    childs = Root.a(person)
    j = 0
    selectedindex = 0
    for c in childs:
        j+=1
        if (len(c.examples)!=0):
            selectedindex = j-1
            break
    if(Root.childs!= None):
        if (Root.childs[selectedindex].childs == None):
            return Root.childs[selectedindex-1].survived
        else:
            return isAlive(person,Root.childs[selectedindex-1])    
        
isAlive(newnode,Root)



total = len(csv_data)
trues= 0
for i in range (len(csv_data)):
    state = None
    if (isAlive(node(None,None,[csv_data.values[i]],None),Root)):
        state = 1
    else:
        state = 0
    if (state==csv_data.values[i][-1]):
        trues+=1
print(trues/total)
