#!/user/bin/python
#-*-coding:UTF-8-*-
#��ȡinp�ļ�
#2Dһ�λ��߶��ε��ı���Cohesive��Ԫ���COH2D4
import sys
File_path='C:/Users/zhy/Desktop/'
Inp_name='Job-3.inp'
NEW_INPNAME='Test3.inp'
#CO_SET startswith
COSTARTS='*Elset, elset=CO_SET, instance=Part-1-1, generate'
Ori_inp=open(File_path+Inp_name,'r')
#��ȡ�ڵ��ż�������Ϣ
Node_dic={}
Inp_line=Ori_inp.readlines()
#Inp_val�����ж�
#���洢Ϊ�ֵ��ʽ������Ϊ����������������Ϊ�������
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


#�˳���Ĭ����Ҫ���cohesive��Ԫ������
Nodel=[]
Inp_value=0
#��ȡ��Ԫ�����
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
               Element_dic[Node1[0]].extend(Node1[1:5])   #�˴���extend����
       except:
           Inp_value=0

EL_EIGHT.sort()
EL_FOUR.sort()

#��ȡ�����cohesive��Ԫ�ĵ�Ԫ����
#�˴��趨�嵥Ԫ�Ľ����
#CO_ELSETΪ��Ҫ����cohesive�ĵ�Ԫ����
#CO_SETΪ�����ɵ�cohesive��Ԫ���������壩
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
        if ESET_value: #����������Ҫ����Cohesive��Ԫ
            try:
               Node1=[int(cor) for cor in Inp_line[i+1].split(',')]
               Num=Node1[1]-Node1[0]+1
               for k in range(Num):
                  S=Node1[0]+k
                  CO_ELSET.append(S)
            except:
               Inp_value=0
               break 

        else: #ĳ����Ԫ���ڲ���Cohesive��Ԫ
            try:
               Node1=[int(cor) for cor in Inp_line[i+1].split(',')]
               for NODE in Node1:
                   CO_ELSET.append(NODE)
            except:
               Inp_value=0
               Node1=0
               k=0
               break

#���cohesive��Ԫ�Ĳ���
#��1���γ�cohesive��Ԫ��㼯�����ҳ����ظ�����
#��2���ҳ��ظ���Ԫ�����������ݱ����γ�cohesive��Ԫ
CO_NODE=[]
for i in Element_dic.keys():
	CO_NODE.extend(Element_dic[i]) #��Ҫ���COHESIVE��Ԫ�ĵ�Ԫ�����������Ľڵ㼯


#Ѱ���ظ��ڵ���
CO_NODE_SORT=sorted(CO_NODE) #�����ڵ�Ԫ�ڵ�������

NODECO=[]
NODECO_DIC={} #ĳ����(�ظ��ڵ���),(ֵ:�ڵ��ظ�����)���ֵ�
for i in CO_NODE_SORT:
    if i not in NODECO_DIC.keys():
         NODECO_DIC[i]=[]
         if CO_NODE_SORT.count(i)>1:
            NODECO.append(i) #��û��ʵ�Ԫ��4�����������еĽڵ���
            NODECO_DIC[i].append(CO_NODE_SORT.count(i)) #��Ӧ���Cohesive��Ԫ�ĵ�Ԫ�������нڵ㼰���Ӧ���ظ����ִ����������ظ�2�κ�4�Σ�
           
#����ظ��ڵ�����Ӧ�ĵ�Ԫ��Ϣ,�������µĽ��
NEWNODE=max(Node_dic.keys()) #��ȡģ�ͻ���Part���Ľڵ��ŷ��������µĽڵ�
NODECO_NEW_DIC={} #�ظ��ڵ���������ɽڵ㼰��������Ԫ���ڵ�Ԫ�ڽڵ�λ�õļ�/ֵ�Ե����ֵ�
for i in NODECO: #Ĭ��i����4
    NODERE=NODECO_DIC[i][0]
    
    EL_RE=[]
    NEW_NODE=[]
    for EL in Element_dic.keys():
        if i in Element_dic[EL]:
            EL_RE.append(EL)
    EL_RE.sort() #��ð�����i���ظ��ڵ�ĵ�Ԫ���ڵĵ�Ԫ��ţ�������ΧһȦ��Ԫ���ڵ��ظ�����Ϊ2��

    NODECO_DIC[i].append(EL_RE) #�ֵ������µ�value

    NODECO_NEW_DIC[i]={}
#EL_RE[0]����ĳ���ظ��ڵ�ı����С�ĵ�Ԫ���ظ��ڵ������λ��
    NODECO_NEW_DIC[i].update({EL_RE[0]:[i,Element_dic[EL_RE[0]].index(i)]}) #�����ڵ�dict��/ֵ�ԣ��ظ��ڵ����ڱ����С��Ԫ/�������ظ��ڵ�ı����С��Ԫ�ڵĸ��ظ��ڵ������λ�ã����µ�NODECO_NEW_DIC�ֵ���
    
    for LS in range(len(EL_RE)-1):#���˱����С��Ԫ�İ������ظ��ڵ�����е�Ԫ����
        NEWNODE= NEWNODE+1 #��Ԫ�����ɽڵ�����������
        NODECO_NEW_DIC[i].update({EL_RE[LS+1]:[NEWNODE,Element_dic[EL_RE[LS+1]].index(i)]}) #(�������ظ��ڵ�ĵ�Ԫ���/�ظ��ڵ�������ɽڵ㼰����������Ԫ�ڽڵ������λ��)��Ӧ�ļ�/ֵ�Ը��µ��µ��ֵ�
        Node_dic[NEWNODE]=[]
        Node_dic[NEWNODE]=Node_dic[i]


#��ȡ�ظ�����������¼
#��1�����ɱ���
#��2��Ѱ���ظ�����
#��1��
#CO_EDGE=()

EDGEINEL={}
#for k in range(len(CO_ELSET)):#�����Cohesive��Ԫ�ĵ�Ԫ����
for k in range(1,CO_ELSET[1]+1):#�����Cohesive��Ԫ�ĵ�Ԫ����
    #if CO_ELSET[k] in Element_dic: #
        #if len(Element_dic[k])==4: #һ��ƽ���ı��ε�Ԫ��
            #a=(Element_dic[CO_ELSET[k]][0],Element_dic[CO_ELSET[k]][1])
            #b=(Element_dic[CO_ELSET[k]][1],Element_dic[CO_ELSET[k]][2])
            #c=(Element_dic[CO_ELSET[k]][2],Element_dic[CO_ELSET[k]][3])
            #d=(Element_dic[CO_ELSET[k]][3],Element_dic[CO_ELSET[k]][0]) 
            ##CO_EDGE=CO_EDGE+(a,)+(b,)+(c,)+(d,) 
            #EDGEINEL[CO_ELSET[k]]=()
            #EDGEINEL[CO_ELSET[k]]=(a,)+(b,)+(c,)+(d,)  #ƽ�浥Ԫ�ڱ߼���=(a,b,c,d)
        #if len(Element_dic[CO_ELSET[k]])==8: #����ƽ���ı��ε�Ԫ
            #a=(Element_dic[CO_ELSET[k]][0],Element_dic[CO_ELSET[k]][1])
            #b=(Element_dic[CO_ELSET[k]][1],Element_dic[CO_ELSET[k]][2])
            #c=(Element_dic[CO_ELSET[k]][2],Element_dic[CO_ELSET[k]][3])
            #d=(Element_dic[CO_ELSET[k]][3],Element_dic[CO_ELSET[k]][4])
            #e=(Element_dic[CO_ELSET[k]][4],Element_dic[CO_ELSET[k]][5])
            #f=(Element_dic[CO_ELSET[k]][5],Element_dic[CO_ELSET[k]][6])
            #g=(Element_dic[CO_ELSET[k]][6],Element_dic[CO_ELSET[k]][7])
            #h=(Element_dic[CO_ELSET[k]][7],Element_dic[CO_ELSET[k]][0]) #�ɽڵ㰴�����ŵĵ�Ԫ��
            ##CO_EDGE=CO_EDGE+(a,)+(b,)+(c,)+(d,)+(e,)+(f,)+(g,)+(h,)
            #EDGEINEL[CO_ELSET[k]]=() #ƽ�浥Ԫ�ڵ�Ԫ���/�߼����ֵ�
            #EDGEINEL[CO_ELSET[k]]=(a,)+(b,)+(c,)+(d,)+(e,)+(f,)+(g,)+(h,) #=(a,b,c,d,e,f,g,h)
            
        if len(Element_dic[k])==4: #һ��ƽ���ı��ε�Ԫ��
            a=(Element_dic[k][0],Element_dic[k][1])
            b=(Element_dic[k][1],Element_dic[k][2])
            c=(Element_dic[k][2],Element_dic[k][3])
            d=(Element_dic[k][3],Element_dic[k][0]) 
            #CO_EDGE=CO_EDGE+(a,)+(b,)+(c,)+(d,) 
            EDGEINEL[k]=()
            EDGEINEL[k]=(a,)+(b,)+(c,)+(d,)  #ƽ�浥Ԫ�ڱ߼���=(a,b,c,d)
        if len(Element_dic[k])==8: #����ƽ���ı��ε�Ԫ
            a=(Element_dic[k][0],Element_dic[k][1])
            b=(Element_dic[k][1],Element_dic[k][2])
            c=(Element_dic[k][2],Element_dic[k][3])
            d=(Element_dic[k][3],Element_dic[k][4])
            e=(Element_dic[k][4],Element_dic[k][5])
            f=(Element_dic[k][5],Element_dic[k][6])
            g=(Element_dic[k][6],Element_dic[k][7])
            h=(Element_dic[k][7],Element_dic[k][0]) #�ɽڵ㰴�����ŵĵ�Ԫ��
            #CO_EDGE=CO_EDGE+(a,)+(b,)+(c,)+(d,)+(e,)+(f,)+(g,)+(h,)
            EDGEINEL[k]=() #ƽ�浥Ԫ�ڵ�Ԫ���/�߼����ֵ�
            EDGEINEL[k]=(a,)+(b,)+(c,)+(d,)+(e,)+(f,)+(g,)+(h,) #=(a,b,c,d,e,f,g,h)


#��2��
#Ѱ��CO_EDGE���ظ���Ԫ�飬�伴Ϊ��Ҫ��ӵ�Ԫ�ı�
#�����ߵķ����γ��ı���
#���Ϊ�ı��δ˴���Ҫ�޸�
k=0
ELEMENT_CO=max(Element_dic.keys()) #�����µ�Cohesive��Ԫ��ʼ���
#�洢cohesive element��Ԫ����
CO_SET_cohesive=[]
for EL in range(1,CO_ELSET[1]):
    k=EL+1
    for k in range(k,CO_ELSET[1]+1):
        EDGE1=EDGEINEL[EL]
        EDGE2=EDGEINEL[k]
        
        for ED1 in EDGE1:
            for ED2 in EDGE2:
                if sum(ED1)==sum(ED2)and abs(ED1[0]-ED1[1])==abs(ED2[0]-ED2[1]):#��ƽ�浥Ԫ����ĳ��(���ñߵĵ�Ԫ�ڵ���Ϣһ��)
                    #����µ�Ԫ�����;ɵ�Ԫ��������滻
                    NODE1=ED1[0]
                    NODE2=ED1[1] #���ñ��ڵ�Ԫ1��CO_ELSET[EL]���ڵĽڵ�
                    #CO_ELSET[EL]
                    NODE3=ED2[0]
                    NODE4=ED2[1]#���ñ��ڵ�Ԫ2��CO_ELSET[k]���ڵĽڵ�
                    
                    #CO_ELSET[k]
                    #CO_ELSET[EL]
                    #if NODE1 in Element_dic[CO_ELSET[EL]]:
                    #LOCλ�õķ���
                    #NODECO_NEW_DIC=�ֵ��е��ֵ䣺����Ϊ���ýڵ�ţ��ڲ��Ϊ��Ԫ�ţ��ֵ�ļ�Ϊĳ�����õĽڵ������ĵ�Ԫ
                    Loc=NODECO_NEW_DIC[NODE1][EL][1] #���ýڵ�NODE1�ڸõ�ԪEL�����ڵ㼯�е�����λ�ã���������ýڵ��ĳ����ԪEL��ĳ�����ýڵ�NODE1�ڸõ�Ԫ�ڵ�λ��
                        #if CO_ELSET[EL] in NODECO_NEW_DIC[NODE1].keys():
                    Element_dic[EL][Loc]=NODECO_NEW_DIC[NODE1][EL][0] #��Ԫ�����ڸ��¹��ýڵ�NODE1����ĳ����Ԫ�Ľڵ㼯�������µĹ��ýڵ��ŵĽڵ㼯��
                    
                    NODE1=NODECO_NEW_DIC[NODE1][EL][0] #��Ԫ�����ڸ��¹��ýڵ�NODE1����ĳ����Ԫ�ڸù��ýڵ�Ϊ�µĽڵ��NEWNODE
                    
                    #if NODE2 in Element_dic[CO_ELSET[EL]]:
                    Loc=NODECO_NEW_DIC[NODE2][EL][1] #���ýڵ�NODE2�ڸõ�ԪEL�����ڵ㼯�е�����λ��
                    #if CO_ELSET[EL] in NODECO_NEW_DIC[NODE2].keys():
                    Element_dic[EL][Loc]=NODECO_NEW_DIC[NODE2][EL][0]#��Ԫ�����ڸ��¹��ýڵ�NODE2����ĳ����Ԫ�Ľڵ㼯�������µĹ��ýڵ��ŵĽڵ㼯��
                    NODE2=NODECO_NEW_DIC[NODE2][EL][0]#��Ԫ�����ڸ��¹��ýڵ�NODE2����ĳ����Ԫ�ڸù��ýڵ�Ϊ�µĽڵ��NEWNODE
                    ##CO_ELSET[k]
                    #if NODE3 in Element_dic[CO_ELSET[k]]:
                    Loc=NODECO_NEW_DIC[NODE3][k][1] #���ýڵ�NODE3�ڸõ�ԪEL�����ڵ㼯�е�����λ��
                         #if CO_ELSET[k] in NODECO_NEW_DIC[NODE3].keys():
                    Element_dic[k][Loc]=NODECO_NEW_DIC[NODE3][k][0]#��Ԫ�����ڸ��¹��ýڵ�NODE3����ĳ����Ԫ�Ľڵ㼯�������µĹ��ýڵ��ŵĽڵ㼯��
                    NODE3=NODECO_NEW_DIC[NODE3][k][0]#��Ԫ�����ڸ��¹��ýڵ�NODE3����ĳ����Ԫ�ڸù��ýڵ�Ϊ�µĽڵ��NEWNODE
                    #if NODE4 in Element_dic[CO_ELSET[k]]:
                    Loc=NODECO_NEW_DIC[NODE4][k][1]#���ýڵ�NODE4�ڸõ�ԪEL�����ڵ㼯�е�����λ��
                        #if CO_ELSET[k] in NODECO_NEW_DIC[NODE4].keys():
                    Element_dic[k][Loc]=NODECO_NEW_DIC[NODE4][k][0]#��Ԫ�����ڸ��¹��ýڵ�NODE3����ĳ����Ԫ�Ľڵ㼯�������µĹ��ýڵ��ŵĽڵ㼯��
                    NODE4=NODECO_NEW_DIC[NODE4][k][0]#��Ԫ�����ڸ��¹��ýڵ�NODE3����ĳ����Ԫ�ڸù��ýڵ�Ϊ�µĽڵ��NEWNODE
                    ELEMENT_CO=ELEMENT_CO+1 #��Ԫ��Ÿ���
                    Element_dic[ELEMENT_CO]=[NODE2,NODE1,NODE4,NODE3] #��Ԫ���ϸ��£������µ�Ԫ��������������ڵ㼯
                    CO_SET_cohesive.append(ELEMENT_CO)  #������������Cohesive��Ԫ��CO_ELSETΪ������Cosesive��Ԫ��


#######�����µ�inp�ļ�                    
File_path='C:/Users/zhy/Desktop/'
outfile=open(File_path+NEW_INPNAME,'w+')
outfile.close()
outfile=open(File_path+NEW_INPNAME,'a+')
#�ļ�ͷ����д
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
#Part��ؽڵ㼰��Ԫ��Ϣд��
#NODE
for i in range(len(Heading)):
    print>>outfile,Heading[i]

#NODE
#�ֵ䰴��keys��С��
#д��Part�еĽڵ��ż��ڵ�����ֵ
NODE_OUTPUT=sorted(Node_dic.items(),key=lambda e:e[0])
for i in range(len(NODE_OUTPUT)):
    #print>>outfile, "%9d,   %9f,   %9f,   %9f" % (NODE_OUTPUT[i][0],NODE_OUTPUT[i][1][0],NODE_OUTPUT[i][1][1],NODE_OUTPUT[i][1][2])
    print>>outfile, "%9d,   %.9f,   %.9f" % (NODE_OUTPUT[i][0],NODE_OUTPUT[i][1][0],NODE_OUTPUT[i][1][1])


#ELement�����жϵ�Ԫ������
for i in Inp_line:
     if i.startswith('*Element, type'):
         for ie in i:
             try:#ȷ����Ԫ����ΪCPE4
                 EL_STY=int(ie)
             except:
                 pass
         if EL_STY==4:#ȷ����Ԫ����ΪCPE4
              print>>outfile,i,
              for EL in EL_FOUR:
                  print>>outfile,"%5d, %5d,  %5d,  %5d,   %5d" % (EL,Element_dic[EL][0],\
                                                                    Element_dic[EL][1],Element_dic[EL][2],Element_dic[EL][3])
         if EL_STY==8:#ȷ����Ԫ����ΪCPE4
              print>>outfile,i,
              for EL in EL_EIGHT:
                  print>>outfile,"%5d, %5d,  %5d,  %5d,  %5d,  %5d,  %5d,  %5d,  %5d,   %5d" % (EL,Element_dic[EL][0],\
                                                                                                  Element_dic[EL][1],Element_dic[EL][2],Element_dic[EL][3],Element_dic[EL][4],Element_dic[EL][5],Element_dic[EL][6],Element_dic[EL][7],Element_dic[EL][8])

#д��cohesive��Ԫ���
#Element_dic[EL][5:8]��������άCohesive��Ԫ��ӣ��˴�Ϊ��
CO_TYPE='*Element, type=COH2D4'
print>>outfile,CO_TYPE
for EL in CO_SET_cohesive:
        #print>>outfile,"%5d, %5d,  %5d,  %5d,  %5d,  %5d,  %5d,  %5d,  %5d,   %5d" % (EL,Element_dic[EL][0],\
                                                                                        #Element_dic[EL][1],Element_dic[EL][2],Element_dic[EL][3],Element_dic[EL][4],Element_dic[EL][5],Element_dic[EL][6],Element_dic[EL][7],Element_dic[EL][8])
				 print>>outfile,"%5d, %5d,  %5d,  %5d,   %5d" % (EL,Element_dic[EL][0],\
                                                          Element_dic[EL][1],Element_dic[EL][2],Element_dic[EL][3])
#д��ԭ��Ԫ����
COINP_SET='*Elset, elset=CO_SET, generate'
print>>outfile,COINP_SET
print>>outfile, "%d, %d, %d" % (CO_ELSET[0],CO_ELSET[1],CO_ELSET[2])
#д��cohesive��Ԫ����
COINP_SET='*Elset, elset=CO_SET_cohesive, generate'
print>>outfile,COINP_SET
print>>outfile, "%d, %d, %d" % (min(CO_SET_cohesive),max(CO_SET_cohesive),1)
#д��β��

print>>outfile,'*End Part'
end=['**','** ASSEMBLY','**','*Assembly, name=Assembly','**','*Instance, name=PART-1-1, part=PART-1',\
     '*End Instance','**','*End Assembly']
for i in end:
    print>>outfile,i

outfile.close()