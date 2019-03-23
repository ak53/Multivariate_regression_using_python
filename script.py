import csv
import numpy as np
from itertools import combinations
from numpy.linalg import inv as inv
from operator import itemgetter

result=[['Combo','Absolute error','Mean squared error']]

csv.register_dialect('myDialect',delimiter = ',',quoting=csv.QUOTE_NONE,skipinitialspace=True)


##### --- READING FILES AND EXTRACTING DATA ---#####
abs_error=[]
ms_error=[]
name="scimagojr 2017  Subject Area - Computer Science.txt"
file=open(name,'rt')
data=file.read()
file.close()
lines=data.split('\n')[1:]
ifile=open('found.txt','rt')                
idata=ifile.read()
ifile.close()
ilines=idata.split("\n")
lol=[]
imf=[]

for i in range(len(lines)-1):             # last line is empty
	if (lines[i].split(";"))[2][1:-2] in idata:
		lst=[]
		lst.append((lines[i].split(";"))[2][1:-1])                                                      #0=title
		if (lines[i].split(";"))[5]=="":
			lst.append(1.0)
		else:
			lst.append(float((lines[i].split(";"))[5].replace(",","")))                   #1=sjr
		lst.append(float((lines[i].split(";"))[7]))                                                  #2=h index
		lst.append(float((lines[i].split(";"))[8]))                                                #3=total docs(2017)
		lst.append(float((lines[i].split(";"))[9]))                                               #4=total docs(3yrs)
		lst.append(float((lines[i].split(";"))[10]))                                              #5=total refs
		lst.append(float((lines[i].split(";"))[11]))                                               #6=total cites(3yrs)
		lst.append(float((lines[i].split(";"))[12]))                                              #7=citable docs(3yrs)
		lst.append(float((lines[i].split(";"))[13].replace(",",".")))                    #8=cites/docs(2yrs)
		lst.append(float((lines[i].split(";"))[14].replace(",",".")  ))                  #9=ref/docs
		                                                                                                      
		t=[]
		index=idata.find((lines[i].split(";"))[2][1:-2])
		length=len(idata[idata.find((lines[i].split(";"))[2][1:-2]):idata.find(";",idata.find((lines[i].split(";"))[2][1:-2]))])
		req=index+length+1
		imf.append(float(idata[idata.find(";",req)+1:idata.find("\n",idata.find(";",req)+1)]))
		lol.append(lst)


##### --- DIVIDING DATA FOR TRAINING AND TESTING ---#####
train_x=lol[:493]
train_y=imf[:493]
test_x=lol[493:]
test_y=imf[493:]


def love(combo,t):                         #CREATES MATRICES
	if t==1:
		s=train_x
	elif t==2:
		s=test_x
	A=[]
	for i in range(len(s)):
		temp=[]
		for j in combo:
			temp.append(s[i][j])
		A.append(temp)
	A=np.array(A)
	return(A)


def error(combo,lst):                          #CALCULATES ERROR AND BEST COMBINATIONS
	n=len(lst)
	abs_e=0
	se=0
	for i in lst:
		abs_e+=abs(i)
		se+=(i)**2
	ans=[]
	abs_e=abs_e/n
	ms_e=se/n
	dic1={1:'SJR',2:'h-index',3:'total docs(2017)',4:'total docs(3yrs)',5:'total refs',6:'total cites(3yrs)',7:'citable docs(3yrs)',8:'cites/docs(2yrs)',9:'refs/docs'}

	combi=""
	for i in combo:
		combi+=(dic1[i]+"; ")

	ans.append(combi[:-2])
	ans.append(abs_e)
	temp1=[]
	temp2=[]
	temp1.append(combi[:-2])
	temp2.append(combi[:-2])

	temp1.append(abs_e)
	abs_error.append(temp1)
	ans.append(ms_e)
	temp2.append(ms_e)
	ms_error.append(temp2)
	result.append(ans)


def mar(combo):                 #CALCULATES (y-Ax) AND USES FUNC ERROR TO APPEND TO RESULT
	err=[]
	A=love(combo,1)
	x=np.matmul(np.matmul(inv(np.matmul(np.transpose(A),A)),np.transpose(A)),train_y)
	a=love(combo,2)
	err.append(test_y-np.matmul(a,x))
	error(combo,err[0])
	return x


##### --- PRINTS RESULT TO CSV FILE --- #####

lst=[1,2,3,4,5,6,7,8,9]
for i in range(9):
	combos=list(combinations(lst,i+1))
	for j in combos:
		mar(j)
with open ('output.csv','w') as out:
	writer=csv.writer(out,dialect='myDialect')
	writer.writerows(result)
out.close()


##### ---PART 2 ---#####

abs_error.sort(key=itemgetter(1))
ms_error.sort(key=itemgetter(1))
p=0
for i in range(len(abs_error)):
	for j in range(i):
		if abs_error[i][0]==ms_error[j][0] and p==0:
			best=abs_error[i][0]
			best_abs_error=abs_error[i][1]
			best_ms_error=ms_error[j][1]
			p+=1

ans=[]
ans.append(best)
ans.append(best_abs_error)
ans.append(best_ms_error)
print("Best combination: "+str(ans)[1:-2])