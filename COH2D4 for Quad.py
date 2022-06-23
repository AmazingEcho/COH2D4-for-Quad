#!/user/bin/python
#-*-coding:UTF-8-*-
#读取inp文件
#2D一次或者二次的四边形Cohesive单元添加COH2D4
import sys
File_path='C:/Users/zhy/Desktop/'
Inp_name='Job-3.inp'
NEW_INPNAME='Test3.inp'
#CO_SET startswith
COSTARTS='*Elset, elset=CO_SET, instance=Part-1-1, generate'
Ori_inp=open(File_path+Inp_name,'r')
#读取节点编号及坐标信息
Node_dic={}
Inp_line=Ori_inp.readlines()
#Inp_val辅助判断
#结点存储为字典格式，结点号为索引，其索引内容为结点坐标
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


#此程序默认需要添加cohesive单元的区域
Nodel=[]
Inp_value=0
#读取单元结点编号
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

#读取需添加cohesive单元的单元集合
#此处需定义单元的结点编号
#CO_ELSET为需要生成cohesive的单元集合
#CO_SET为新生成的cohesive单元（命名不清）
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
        if ESET_value: #整个部件需要插入Cohesive单元
            try:
               Node1=[int(cor) for cor in Inp_line[i+1].split(',')]
               Num=Node1[1]-Node1[0]+1
               for k in range(Num):
                  S=Node1[0]+k
                  CO_ELSET.append(S)
            except:
               Inp_value=0
               break 

        else: #某个单元集内插入Cohesive单元
            try:
               Node1=[int(cor) for cor in Inp_line[i+1].split(',')]
               for NODE in Node1:
                   CO_ELSET.append(NODE)
            except:
               Inp_value=0
               Node1=0
               k=0
               break

#添加cohesive单元的步骤
#（1）形成cohesive单元结点集，并找出其重复次数
#（2）找出重复单元变数，并根据边数形成cohesive单元
CO_NODE=[]
for i in Element_dic.keys():
	CO_NODE.extend(Element_dic[i]) #需要添加COHESIVE单元的单元集合所包含的节点集


#寻找重复节点数
CO_NODE_SORT=sorted(CO_NODE) #集合内单元节点重排序

NODECO=[]
NODECO_DIC={} #某个键(重复节点编号),(值:节点重复次数)的字典
for i in CO_NODE_SORT:
    if i not in NODECO_DIC.keys():
         NODECO_DIC[i]=[]
         if CO_NODE_SORT.count(i)>1:
            NODECO.append(i) #获得基质单元除4个定点外所有的节点编号
            NODECO_DIC[i].append(CO_NODE_SORT.count(i)) #对应添加Cohesive单元的单元集的所有节点及其对应的重复出现次数（包括重复2次和4次）
           
#获得重复节点数对应的单元信息,并生成新的结点
NEWNODE=max(Node_dic.keys()) #获取模型或者Part最大的节点编号方便生成新的节点
NODECO_NEW_DIC={} #重复节点剥离新生成节点及其所属单元及在单元内节点位置的键/值对的新字典
for i in NODECO: #默认i大于4
    NODERE=NODECO_DIC[i][0]
    
    EL_RE=[]
    NEW_NODE=[]
    for EL in Element_dic.keys():
        if i in Element_dic[EL]:
            EL_RE.append(EL)
    EL_RE.sort() #获得包含第i个重复节点的单元集内的单元编号（包括外围一圈单元，节点重复次数为2）

    NODECO_DIC[i].append(EL_RE) #字典增加新的value

    NODECO_NEW_DIC[i]={}
#EL_RE[0]包含某个重复节点的编号最小的单元内重复节点的索引位置
    NODECO_NEW_DIC[i].update({EL_RE[0]:[i,Element_dic[EL_RE[0]].index(i)]}) #括号内的dict键/值对（重复节点所在编号最小单元/包含该重复节点的编号最小单元内的该重复节点的索引位置）更新到NODECO_NEW_DIC字典中
    
    for LS in range(len(EL_RE)-1):#除了编号最小单元的包含该重复节点的所有单元遍历
        NEWNODE= NEWNODE+1 #单元新生成节点编号重新生成
        NODECO_NEW_DIC[i].update({EL_RE[LS+1]:[NEWNODE,Element_dic[EL_RE[LS+1]].index(i)]}) #(包含该重复节点的单元编号/重复节点的新生成节点及其在所属单元内节点的索引位置)对应的键/值对更新到新的字典
        Node_dic[NEWNODE]=[]
        Node_dic[NEWNODE]=Node_dic[i]


#获取重复边数数并记录
#（1）生成边数
#（2）寻找重复边数
#（1）
#CO_EDGE=()

EDGEINEL={}
#for k in range(len(CO_ELSET)):#拟插入Cohesive单元的单元集合
for k in range(1,CO_ELSET[1]+1):#拟插入Cohesive单元的单元集合
    #if CO_ELSET[k] in Element_dic: #
        #if len(Element_dic[k])==4: #一次平面四边形单元的
            #a=(Element_dic[CO_ELSET[k]][0],Element_dic[CO_ELSET[k]][1])
            #b=(Element_dic[CO_ELSET[k]][1],Element_dic[CO_ELSET[k]][2])
            #c=(Element_dic[CO_ELSET[k]][2],Element_dic[CO_ELSET[k]][3])
            #d=(Element_dic[CO_ELSET[k]][3],Element_dic[CO_ELSET[k]][0]) 
            ##CO_EDGE=CO_EDGE+(a,)+(b,)+(c,)+(d,) 
            #EDGEINEL[CO_ELSET[k]]=()
            #EDGEINEL[CO_ELSET[k]]=(a,)+(b,)+(c,)+(d,)  #平面单元内边集合=(a,b,c,d)
        #if len(Element_dic[CO_ELSET[k]])==8: #二次平面四边形单元
            #a=(Element_dic[CO_ELSET[k]][0],Element_dic[CO_ELSET[k]][1])
            #b=(Element_dic[CO_ELSET[k]][1],Element_dic[CO_ELSET[k]][2])
            #c=(Element_dic[CO_ELSET[k]][2],Element_dic[CO_ELSET[k]][3])
            #d=(Element_dic[CO_ELSET[k]][3],Element_dic[CO_ELSET[k]][4])
            #e=(Element_dic[CO_ELSET[k]][4],Element_dic[CO_ELSET[k]][5])
            #f=(Element_dic[CO_ELSET[k]][5],Element_dic[CO_ELSET[k]][6])
            #g=(Element_dic[CO_ELSET[k]][6],Element_dic[CO_ELSET[k]][7])
            #h=(Element_dic[CO_ELSET[k]][7],Element_dic[CO_ELSET[k]][0]) #由节点按次序编号的单元边
            ##CO_EDGE=CO_EDGE+(a,)+(b,)+(c,)+(d,)+(e,)+(f,)+(g,)+(h,)
            #EDGEINEL[CO_ELSET[k]]=() #平面单元内单元编号/边集合字典
            #EDGEINEL[CO_ELSET[k]]=(a,)+(b,)+(c,)+(d,)+(e,)+(f,)+(g,)+(h,) #=(a,b,c,d,e,f,g,h)
            
        if len(Element_dic[k])==4: #一次平面四边形单元的
            a=(Element_dic[k][0],Element_dic[k][1])
            b=(Element_dic[k][1],Element_dic[k][2])
            c=(Element_dic[k][2],Element_dic[k][3])
            d=(Element_dic[k][3],Element_dic[k][0]) 
            #CO_EDGE=CO_EDGE+(a,)+(b,)+(c,)+(d,) 
            EDGEINEL[k]=()
            EDGEINEL[k]=(a,)+(b,)+(c,)+(d,)  #平面单元内边集合=(a,b,c,d)
        if len(Element_dic[k])==8: #二次平面四边形单元
            a=(Element_dic[k][0],Element_dic[k][1])
            b=(Element_dic[k][1],Element_dic[k][2])
            c=(Element_dic[k][2],Element_dic[k][3])
            d=(Element_dic[k][3],Element_dic[k][4])
            e=(Element_dic[k][4],Element_dic[k][5])
            f=(Element_dic[k][5],Element_dic[k][6])
            g=(Element_dic[k][6],Element_dic[k][7])
            h=(Element_dic[k][7],Element_dic[k][0]) #由节点按次序编号的单元边
            #CO_EDGE=CO_EDGE+(a,)+(b,)+(c,)+(d,)+(e,)+(f,)+(g,)+(h,)
            EDGEINEL[k]=() #平面单元内单元编号/边集合字典
            EDGEINEL[k]=(a,)+(b,)+(c,)+(d,)+(e,)+(f,)+(g,)+(h,) #=(a,b,c,d,e,f,g,h)


#（2）
#寻找CO_EDGE中重复的元组，其即为需要添加单元的边
#用求法线的方法形成四边形
#如果为四边形此处需要修改
k=0
ELEMENT_CO=max(Element_dic.keys()) #定义新的Cohesive单元起始编号
#存储cohesive element单元集合
CO_SET_cohesive=[]
for EL in range(1,CO_ELSET[1]):
    k=EL+1
    for k in range(k,CO_ELSET[1]+1):
        EDGE1=EDGEINEL[EL]
        EDGE2=EDGEINEL[k]
        
        for ED1 in EDGE1:
            for ED2 in EDGE2:
                if sum(ED1)==sum(ED2)and abs(ED1[0]-ED1[1])==abs(ED2[0]-ED2[1]):#两平面单元共用某边(共用边的单元节点信息一致)
                    #完成新单元创建和旧单元中坐标的替换
                    NODE1=ED1[0]
                    NODE2=ED1[1] #共用边在单元1（CO_ELSET[EL]）内的节点
                    #CO_ELSET[EL]
                    NODE3=ED2[0]
                    NODE4=ED2[1]#共用边在单元2（CO_ELSET[k]）内的节点
                    
                    #CO_ELSET[k]
                    #CO_ELSET[EL]
                    #if NODE1 in Element_dic[CO_ELSET[EL]]:
                    #LOC位置的放置
                    #NODECO_NEW_DIC=字典中的字典：外层键为共用节点号，内层键为单元号；字典的键为某个共用的节点所属的单元
                    Loc=NODECO_NEW_DIC[NODE1][EL][1] #共用节点NODE1在该单元EL所含节点集中的索引位置：含多个共用节点的某个单元EL的某个共用节点NODE1在该单元内的位置
                        #if CO_ELSET[EL] in NODECO_NEW_DIC[NODE1].keys():
                    Element_dic[EL][Loc]=NODECO_NEW_DIC[NODE1][EL][0] #单元集合内更新共用节点NODE1所属某个单元的节点集（采用新的共用节点编号的节点集）
                    
                    NODE1=NODECO_NEW_DIC[NODE1][EL][0] #单元集合内更新共用节点NODE1所属某个单元内该共用节点为新的节点号NEWNODE
                    
                    #if NODE2 in Element_dic[CO_ELSET[EL]]:
                    Loc=NODECO_NEW_DIC[NODE2][EL][1] #共用节点NODE2在该单元EL所含节点集中的索引位置
                    #if CO_ELSET[EL] in NODECO_NEW_DIC[NODE2].keys():
                    Element_dic[EL][Loc]=NODECO_NEW_DIC[NODE2][EL][0]#单元集合内更新共用节点NODE2所属某个单元的节点集（采用新的共用节点编号的节点集）
                    NODE2=NODECO_NEW_DIC[NODE2][EL][0]#单元集合内更新共用节点NODE2所属某个单元内该共用节点为新的节点号NEWNODE
                    ##CO_ELSET[k]
                    #if NODE3 in Element_dic[CO_ELSET[k]]:
                    Loc=NODECO_NEW_DIC[NODE3][k][1] #共用节点NODE3在该单元EL所含节点集中的索引位置
                         #if CO_ELSET[k] in NODECO_NEW_DIC[NODE3].keys():
                    Element_dic[k][Loc]=NODECO_NEW_DIC[NODE3][k][0]#单元集合内更新共用节点NODE3所属某个单元的节点集（采用新的共用节点编号的节点集）
                    NODE3=NODECO_NEW_DIC[NODE3][k][0]#单元集合内更新共用节点NODE3所属某个单元内该共用节点为新的节点号NEWNODE
                    #if NODE4 in Element_dic[CO_ELSET[k]]:
                    Loc=NODECO_NEW_DIC[NODE4][k][1]#共用节点NODE4在该单元EL所含节点集中的索引位置
                        #if CO_ELSET[k] in NODECO_NEW_DIC[NODE4].keys():
                    Element_dic[k][Loc]=NODECO_NEW_DIC[NODE4][k][0]#单元集合内更新共用节点NODE3所属某个单元的节点集（采用新的共用节点编号的节点集）
                    NODE4=NODECO_NEW_DIC[NODE4][k][0]#单元集合内更新共用节点NODE3所属某个单元内该共用节点为新的节点号NEWNODE
                    ELEMENT_CO=ELEMENT_CO+1 #单元编号更新
                    Element_dic[ELEMENT_CO]=[NODE2,NODE1,NODE4,NODE3] #单元集合更新，创建新单元及并赋予其包含节点集
                    CO_SET_cohesive.append(ELEMENT_CO)  #区别于欲插入Cohesive单元的CO_ELSET为真正的Cosesive单元集


#######生成新的inp文件                    
File_path='C:/Users/zhy/Desktop/'
outfile=open(File_path+NEW_INPNAME,'w+')
outfile.close()
outfile=open(File_path+NEW_INPNAME,'a+')
#文件头的书写
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
#Part相关节点及单元信息写入
#NODE
for i in range(len(Heading)):
    print>>outfile,Heading[i]

#NODE
#字典按照keys大小排
#写入Part中的节点编号及节点坐标值
NODE_OUTPUT=sorted(Node_dic.items(),key=lambda e:e[0])
for i in range(len(NODE_OUTPUT)):
    #print>>outfile, "%9d,   %9f,   %9f,   %9f" % (NODE_OUTPUT[i][0],NODE_OUTPUT[i][1][0],NODE_OUTPUT[i][1][1],NODE_OUTPUT[i][1][2])
    print>>outfile, "%9d,   %.9f,   %.9f" % (NODE_OUTPUT[i][0],NODE_OUTPUT[i][1][0],NODE_OUTPUT[i][1][1])


#ELement首先判断单元的类型
for i in Inp_line:
     if i.startswith('*Element, type'):
         for ie in i:
             try:#确定单元类型为CPE4
                 EL_STY=int(ie)
             except:
                 pass
         if EL_STY==4:#确定单元类型为CPE4
              print>>outfile,i,
              for EL in EL_FOUR:
                  print>>outfile,"%5d, %5d,  %5d,  %5d,   %5d" % (EL,Element_dic[EL][0],\
                                                                    Element_dic[EL][1],Element_dic[EL][2],Element_dic[EL][3])
         if EL_STY==8:#确定单元类型为CPE4
              print>>outfile,i,
              for EL in EL_EIGHT:
                  print>>outfile,"%5d, %5d,  %5d,  %5d,  %5d,  %5d,  %5d,  %5d,  %5d,   %5d" % (EL,Element_dic[EL][0],\
                                                                                                  Element_dic[EL][1],Element_dic[EL][2],Element_dic[EL][3],Element_dic[EL][4],Element_dic[EL][5],Element_dic[EL][6],Element_dic[EL][7],Element_dic[EL][8])

#写入cohesive单元结点
#Element_dic[EL][5:8]适用于三维Cohesive单元添加，此处为空
CO_TYPE='*Element, type=COH2D4'
print>>outfile,CO_TYPE
for EL in CO_SET_cohesive:
        #print>>outfile,"%5d, %5d,  %5d,  %5d,  %5d,  %5d,  %5d,  %5d,  %5d,   %5d" % (EL,Element_dic[EL][0],\
                                                                                        #Element_dic[EL][1],Element_dic[EL][2],Element_dic[EL][3],Element_dic[EL][4],Element_dic[EL][5],Element_dic[EL][6],Element_dic[EL][7],Element_dic[EL][8])
				 print>>outfile,"%5d, %5d,  %5d,  %5d,   %5d" % (EL,Element_dic[EL][0],\
                                                          Element_dic[EL][1],Element_dic[EL][2],Element_dic[EL][3])
#写入原单元集合
COINP_SET='*Elset, elset=CO_SET, generate'
print>>outfile,COINP_SET
print>>outfile, "%d, %d, %d" % (CO_ELSET[0],CO_ELSET[1],CO_ELSET[2])
#写入cohesive单元集合
COINP_SET='*Elset, elset=CO_SET_cohesive, generate'
print>>outfile,COINP_SET
print>>outfile, "%d, %d, %d" % (min(CO_SET_cohesive),max(CO_SET_cohesive),1)
#写入尾部

print>>outfile,'*End Part'
end=['**','** ASSEMBLY','**','*Assembly, name=Assembly','**','*Instance, name=PART-1-1, part=PART-1',\
     '*End Instance','**','*End Assembly']
for i in end:
    print>>outfile,i

outfile.close()