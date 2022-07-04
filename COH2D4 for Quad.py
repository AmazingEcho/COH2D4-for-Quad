#!/user/bin/python
#-*-coding:UTF-8-*-
# Read inp file
import sys
File_path='C:/Users/zhy/Desktop/'
Inp_name='Job-1.inp'
NEW_INPNAME='Test1.inp'
# CO_SET startswith
COSTARTS='*Elset, elset=CO_SET, instance=Part-1-1, generate'
Ori_inp=open(File_path+Inp_name,'r')
# Read node number and coordinate information
Node_dic={}
Inp_line=Ori_inp.readlines()
# Auxiliary judgment of Inp_val
# The nodes are stored in dictionary format, the node number is the index and its index content the node coordinates
Inp_value=0
Inp_value=0
for i in range(len(Inp_line)):
    if Inp_line[i].startswith('*Node'):
        Inp_value+=1
    if Inp_line[i].startswith('*Element'):
        Inp_value+=1
        break
    if Inp_value==1:
       try:
           Node1=[float(cor) for cor in Inp_line[i+1].split(',')]
           Node1[0]=int(Node1[0])
           Node_dic[Node1[0]]=[]
           Node_dic[Node1[0]].append(Node1[1])
           Node_dic[Node1[0]].append(Node1[2])
           Node_dic[Node1[0]].append(Node1[3])
       except:pass


# The region where the cohesive elements need to be added
Nodel=[]
Inp_value=0
# Read element nodes number
Element_dic={}
EL_EIGHT=[]
EL_FOUR=[]
for i in range(len(Inp_line)):
    if Inp_line[i].startswith('*Element'):
        Inp_value+=1
    if Inp_value==1:
       try:
           Node1=[int(cor) for cor in Inp_line[i+1].split(',')]
           Element_dic[Node1[0]]=[]
           if len(Node1)==9:
               EL_EIGHT.append(Node1[0])
               Element_dic[Node1[0]].extend(Node1[1:8])                           
           elif len(Node1)==5:
               EL_FOUR.append(Node1[0])
               Element_dic[Node1[0]].extend(Node1[1:5])   #此处用extend更好
       except:
           Inp_value=0

EL_EIGHT.sort()
EL_FOUR.sort()

Node1=[]
Inp_value=0
ESET_value=0
CO_ELSET=[]
for i in range(len(Inp_line)):
    if Inp_line[i].startswith(COSTARTS): 
        Inp_value+=1
        ESET_value=1
    if Inp_line[i].startswith('*Elset, elset=CO_SET, generate\n'):
        Inp_value+=1
        ESET_value=0
    if  Inp_value :
        if ESET_value: # The whole part needs to be embedded with Cohesive elements.
            try:
               Node1=[int(cor) for cor in Inp_line[i+1].split(',')]
               Num=Node1[1]-Node1[0]+1
               for k in range(Num):
                  S=Node1[0]+k
                  CO_ELSET.append(S)
            except:
               Inp_value=0
               break 

        else: # Some other parts
            try:
               Node1=[int(cor) for cor in Inp_line[i+1].split(',')]
               for NODE in Node1:
                   CO_ELSET.append(NODE)
            except:
               Inp_value=0
               Node1=0
               k=0
               break

# Steps to add cohesive elements
CO_NODE=[]
for i in Element_dic.keys():
	CO_NODE.extend(Element_dic[i]) 


# Find the number of repeat nodes
CO_NODE_SORT=sorted(CO_NODE) 

NODECO=[]
NODECO_DIC={}
for i in CO_NODE_SORT:
    if i not in NODECO_DIC.keys():
         NODECO_DIC[i]=[]
         if CO_NODE_SORT.count(i)>1:
            NODECO.append(i) 
            NODECO_DIC[i].append(CO_NODE_SORT.count(i))
           
# Obtain the information of the element corresponding to the number of duplicate nodes, and generate new nodes
NEWNODE=max(Node_dic.keys()) 
NODECO_NEW_DIC={} 
for i in NODECO:
    NODERE=NODECO_DIC[i][0]
    
    EL_RE=[]
    NEW_NODE=[]
    for EL in Element_dic.keys():
        if i in Element_dic[EL]:
            EL_RE.append(EL)
    EL_RE.sort() 

    NODECO_DIC[i].append(EL_RE) # Dictionary add new value

    NODECO_NEW_DIC[i]={}

    NODECO_NEW_DIC[i].update({EL_RE[0]:[i,Element_dic[EL_RE[0]].index(i)]}) 
    
    for LS in range(len(EL_RE)-1):# Iterate over all elements containing the duplicate node except the smallest numbered element
        NEWNODE= NEWNODE+1 
        NODECO_NEW_DIC[i].update({EL_RE[LS+1]:[NEWNODE,Element_dic[EL_RE[LS+1]].index(i)]}) 
        Node_dic[NEWNODE]=[]
        Node_dic[NEWNODE]=Node_dic[i]


# Get the number of repeating edges and record

EDGEINEL={}
#for k in range(len(CO_ELSET)):
for k in range(1,CO_ELSET[1]+1):
            
        if len(Element_dic[k])==4: 
            a=(Element_dic[k][0],Element_dic[k][1])
            b=(Element_dic[k][1],Element_dic[k][2])
            c=(Element_dic[k][2],Element_dic[k][3])
            d=(Element_dic[k][3],Element_dic[k][0]) 
            EDGEINEL[k]=()
            EDGEINEL[k]=(a,)+(b,)+(c,)+(d,)
        if len(Element_dic[k])==8:
            a=(Element_dic[k][0],Element_dic[k][1])
            b=(Element_dic[k][1],Element_dic[k][2])
            c=(Element_dic[k][2],Element_dic[k][3])
            d=(Element_dic[k][3],Element_dic[k][4])
            e=(Element_dic[k][4],Element_dic[k][5])
            f=(Element_dic[k][5],Element_dic[k][6])
            g=(Element_dic[k][6],Element_dic[k][7])
            h=(Element_dic[k][7],Element_dic[k][0])
            EDGEINEL[k]=() # Dictionary of elements number/sides
            EDGEINEL[k]=(a,)+(b,)+(c,)+(d,)+(e,)+(f,)+(g,)+(h,)


# Find duplicate tuples in CO_EDGE
# The method of finding the normal to form a quadrilateral

k=0
ELEMENT_CO=max(Element_dic.keys()) # Define the starting number of the new cohesive element.

CO_SET_cohesive=[]
for EL in range(1,CO_ELSET[1]):
    k=EL+1
    for k in range(k,CO_ELSET[1]+1):
        EDGE1=EDGEINEL[EL]
        EDGE2=EDGEINEL[k]
        
        for ED1 in EDGE1:
            for ED2 in EDGE2:
                if sum(ED1)==sum(ED2)and abs(ED1[0]-ED1[1])==abs(ED2[0]-ED2[1]):# Two elements share a common edge
                    
                    NODE1=ED1[0]
                    NODE2=ED1[1] # Shared edge in element 1
                    #CO_ELSET[EL]
                    NODE3=ED2[0]
                    NODE4=ED2[1]# Shared edge in element 2
                    
                   
                    Loc=NODECO_NEW_DIC[NODE1][EL][1] 
                    Element_dic[EL][Loc]=NODECO_NEW_DIC[NODE1][EL][0] 
                    
                    NODE1=NODECO_NEW_DIC[NODE1][EL][0] 
                    Loc=NODECO_NEW_DIC[NODE2][EL][1] 
                    Element_dic[EL][Loc]=NODECO_NEW_DIC[NODE2][EL][0]
                    NODE2=NODECO_NEW_DIC[NODE2][EL][0]
                    
                    Loc=NODECO_NEW_DIC[NODE3][k][1] 
                    Element_dic[k][Loc]=NODECO_NEW_DIC[NODE3][k][0]
                    NODE3=NODECO_NEW_DIC[NODE3][k][0]
                    Loc=NODECO_NEW_DIC[NODE4][k][1]
                    Element_dic[k][Loc]=NODECO_NEW_DIC[NODE4][k][0]
                    NODE4=NODECO_NEW_DIC[NODE4][k][0]
                    ELEMENT_CO=ELEMENT_CO+1 
                    Element_dic[ELEMENT_CO]=[NODE2,NODE1,NODE4,NODE3] 
                    CO_SET_cohesive.append(ELEMENT_CO)  


# Generate a new inp file                    
File_path='C:/Users/zhy/Desktop/'
outfile=open(File_path+NEW_INPNAME,'w+')
outfile.close()
outfile=open(File_path+NEW_INPNAME,'a+')
# Document header writing
Heading=[]
Heading.append('*Heading')
Heading.append('** Job name: lis1: Model-1')
Heading.append('** Generated by: Abaqus/CAE 2021')
Heading.append('*Preprint, echo=NO, model=NO, history=NO, contact=NO')
Heading.append('**')
Heading.append('**PARTS')
Heading.append('**')
Heading.append('*Part, name=PART-1')
Heading.append('*Node')

for i in range(len(Heading)):
    print>>outfile,Heading[i]


# Write node number and node coordinate value
NODE_OUTPUT=sorted(Node_dic.items(),key=lambda e:e[0])
for i in range(len(NODE_OUTPUT)):
    
    print>>outfile, "%9d,   %.9f,   %.9f" % (NODE_OUTPUT[i][0],NODE_OUTPUT[i][1][0],NODE_OUTPUT[i][1][1])


# Determine the type of element
for i in Inp_line:
     if i.startswith('*Element, type'):
         for ie in i:
             try:
                 EL_STY=int(ie)
             except:
                 pass
         if EL_STY==4:
              print>>outfile,i,
              for EL in EL_FOUR:
                  print>>outfile,"%5d, %5d,  %5d,  %5d,   %5d" % (EL,Element_dic[EL][0],\
                                                                    Element_dic[EL][1],Element_dic[EL][2],Element_dic[EL][3])
         if EL_STY==8:
              print>>outfile,i,
              for EL in EL_EIGHT:
                  print>>outfile,"%5d, %5d,  %5d,  %5d,  %5d,  %5d,  %5d,  %5d,  %5d,   %5d" % (EL,Element_dic[EL][0],\
                                                                                                  Element_dic[EL][1],Element_dic[EL][2],Element_dic[EL][3],Element_dic[EL][4],Element_dic[EL][5],Element_dic[EL][6],Element_dic[EL][7],Element_dic[EL][8])

CO_TYPE='*Element, type=COH2D4'
print>>outfile,CO_TYPE
for EL in CO_SET_cohesive:
        
				 print>>outfile,"%5d, %5d,  %5d,  %5d,   %5d" % (EL,Element_dic[EL][0],\
                                                          Element_dic[EL][1],Element_dic[EL][2],Element_dic[EL][3])
# Write to original set of elements
COINP_SET='*Elset, elset=CO_SET, generate'
print>>outfile,COINP_SET
print>>outfile, "%d, %d, %d" % (CO_ELSET[0],CO_ELSET[1],CO_ELSET[2])

COINP_SET='*Elset, elset=CO_SET_cohesive, generate'
print>>outfile,COINP_SET
print>>outfile, "%d, %d, %d" % (min(CO_SET_cohesive),max(CO_SET_cohesive),1)

print>>outfile,'*End Part'
end=['**','** ASSEMBLY','**','*Assembly, name=Assembly','**','*Instance, name=PART-1-1, part=PART-1',\
     '*End Instance','**','*End Assembly']
for i in end:
    print>>outfile,i

outfile.close()
