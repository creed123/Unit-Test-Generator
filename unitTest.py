def findAutowired(fileName):
	file = open(fileName,"r")
	Autowired = []
	i= file.readlines()
	for j in range(0,len(i)):
		if("@Autowired" in i[j]):
			x =i[j+1].split(" ")
			x= x[len(x)-1]
			y=x.split(";")
			Autowired.append(y[0])
	return Autowired

def listAutowiredFieldsInMethods(methodName,fileName):
	file = open(fileName,"r")
	Autowired=findAutowired(fileName)
	lines=[]
	file.seek(0)
	i = file.readlines()
	count = 0
	inMethod = False
	for j in range(0,len(i)):
		if(inMethod==True):
			for num in range(0,len(Autowired)):
				if(Autowired[num] in i[j]):
					lines.append(i[j])
					break
			if("{" in i[j]):
				count = count +1
			if("}" in i[j]):
				count = count -1
				if(count ==0):
					inMethod = False
					break
		if(methodName in i[j]):
			inMethod = True
			if("{" in i[j]):
				count=count +1
	return lines

def listDummyDataInMethod(methodName,fileName):
	lines=listAutowiredFieldsInMethods(methodName,fileName)
	dummyDataObjects=[]
	for i in range(0,len(lines)):
		line=lines[i]
		line = line.split(" ")
		j=0
		while(line[j]==''):
			j=j+1
			continue
		x=line[j]
		if j!=len(line)-1:
			x=x+" "+line[j+1]
		x = x.split(";")
		dummyDataObjects.append(x[0])
	return dummyDataObjects


def listInternalObjects(methodName,fileName):
	dummyDataObjects=listDummyDataInMethod(methodName,fileName)
	file = open(fileName,"r")
	file.seek(0)
	objectRel={}
	i = file.readlines()
	for j in range(0,len(i)):
		if("=" in i[j]):
			for k in range(0,len(dummyDataObjects)):
				if(dummyDataObjects[k].split(" ")[1] in i[k]):
					objectRel[i[j].split("=")[0]]=dummyDataObjects[k].split(" ")[1]
					break
	return objectRel


def parseIfElseConditions(methodName,fileName):
	file = open(fileName,"r")
	file.seek(0)
	i = file.readlines() 
	conditions=[]
	length = getMethodLength(i,methodName)
	inMethod=False
	for j in range(0,len(i)):
		if(inMethod==True):
			if("if" in i[j] or "else" in i[j]):
				print j
				lineNumber=findBlockLastLine(i,j)
				conditions=conditions+parseBlock(i,j,lineNumber)
				j=lineNumber
				print(j)
				if(j>length):
					break
		if(methodName in i[j]):
			inMethod=True
	return conditions


def parseBlock(i,j,lineNumber):
	conditions=[]
	for k in range(j,lineNumber):
		if(k>=lineNumber):
			break
		if("if" in i[k]):
			temp=[]
			temp.append(i[k])
			lineNum=findBlockLastLine(i,k)
			temp.append(parseBlock(i,k+1,lineNum))
			conditions.append(temp)
			k=lineNum
		if("else" in i[k]):
			temp=[]
			temp.append(i[k])
			lineNum=findBlockLastLine(i,k)
			temp.append(parseBlock(i,k+1,lineNum))
			conditions.append(temp)
			k=lineNum
	return conditions

def findBlockLastLine(i,j):
	count =0
	while(True):
		if("}" in i[j]):
			count =count- findCount("}",i[j])
		if("{" in i[j]):
			count =count +findCount("{",i[j])
		j=j+1
		if (count<=0):
			break
	return j	

def findCount(brace,line):
	count=0
	for i in range(0,len(line)):
		if(line[i] == brace):
			count =count +1
	return count

def getMethodLength(i,methodName):
	count =0
	for j in range(0,len(i)):
		if(methodName in i[j]):
			if("{" in i[j]):
				count =count +1
			if("}" in i[j]):
				count =count -1
	return count


		

