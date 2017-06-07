def findAutowired(fileName):#Drawback is doesnt take into account constructor autowiring.
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

def listAutowiredFieldsInMethods(methodName,fileName):#We can list all the autowired fields in the method. 
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

def listDummyDataInMethod(methodName,fileName):#gets the dummy data objects in the method. Looks for autowired objects in the method. 
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


def listInternalObjects(methodName,fileName):#Creates a dictionary of internal objects mapped against the autowired methods calls.
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


def parseIfElseConditions(methodName,fileName):#returns the if-else constructs in a parsable manner in case of nested and multiple statements. 
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


def parseBlock(i,j,lineNumber):#Recursive function to parse an if or else for nested conditions.
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

def findBlockLastLine(i,j):#To find the end line of an if or else block.
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

def findCount(brace,line):#Counts the number of brackets in a line.(Only a particular bracket though)
	count=0
	for i in range(0,len(line)):
		if(line[i] == brace):
			count =count +1
	return count

def getMethodLength(i,methodName):#Gets the length of a method.
	count =0
	for j in range(0,len(i)):
		if(methodName in i[j]):
			if("{" in i[j]):
				count =count +1
			if("}" in i[j]):
				count =count -1
	return count


		

