import csv
def sum_p(D,i,j):
    sums=0
    while i<=j:
        sums=sums+D[i][2]
        i=i+1
    return sums

def sum_delta(D,i,j):
    sums=0
    while i<=j:
        sums=sums+D[i][4]
        i=i+1
    return sums
def func_L(D1,D2,g_table,l,i,j,ii,jj):
    sums=0
    sums=sums+g_table[ii+1][jj+1][l+max(sum_p(D1,i,ii),sum_p(D2,j,jj))]
    h=i
    while h<=ii:
        sums=sums+max(l+sum_p(D1,i,h)-Data1[h][3],0) 
        h=h+1
    h=j
    while h<=jj:
        sums=sums+max(l+sum_p(D2,j,h)-Data2[h][3],0)   
        h=h+1
    return sums

Data=[]
Data1=[]
Data2=[]
v0=70;

inf=float('inf')
with open('DATA.csv', newline='') as csvfile:
  rows = csv.reader(csvfile)
  for row in rows:
    Data.append([int(row[1]),int(row[2]),int(row[3]),int(row[4]),int(row[2])-int(row[1])])
    
for i in range(50):
    Data1.append(Data[2*i])
    Data2.append(Data[2*i+1])
z=sum_p(Data1,0,49)+sum_p(Data2,0,49)
Process=[]
for i in range(51):
    Proce_Block=[]
    for j in range(51):
        Proce_list=[]
        for k in range(z+1):
            Proce_list.append([inf,inf,inf])
        Proce_Block.append(Proce_list)
    Process.append(Proce_Block)

Hsetlist=[]
for i in range(50):
    LISTROW=[]
    for j in range(50):
        Hset=set()
        ii=i
        jj=j
        
        while ii<50 and jj<50 and sum_p(Data1,i,ii)!=sum_p(Data2,j,jj) and v0+sum_delta(Data1,0,ii-1)+sum_delta(Data2,0,jj-1)-Data1[ii][0]-Data2[jj][0]>=0:
            Hset=Hset.union({(i,j,ii,jj)})
            if sum_p(Data1,i,ii)<sum_p(Data2,j,jj):
                ii=ii+1
            else:
                jj=jj+1
        LISTROW.append(Hset)
    Hsetlist.append(LISTROW)


LIST3D=[]
for i in range(51):
    LIST2D=[]
    for j in range(51):
        LIST1D=[]
        for i in range(z+1):
            LIST1D.append(inf)
        LIST2D.append(LIST1D)
    LIST3D.append(LIST2D)

for k in range(z+1):
    LIST3D[50][50][k]=0
    
i=49
while i>=0:
    for k in range(z+1):
        if v0+sum_delta(Data1,0,i-1)+sum_delta(Data2,0,49)-Data1[i][0]>=0 and k+Data1[i][2]<z+1:
            LIST3D[i][50][k]=LIST3D[i+1][50][k+Data1[i][2]]+max(k+Data1[i][2]-Data1[i][3],0)
            Process[i][j][k][0]=i+1
            Process[i][j][k][1]=j
            Process[i][j][k][2]=k+Data1[i][2]
        else:
            LIST3D[i][50][k]=inf
    i=i-1
        

j=49
while j>=0:
    for k in range(z+1):
        if v0+sum_delta(Data2,0,j-1)+sum_delta(Data1,0,49)-Data2[j][0]>=0 and k+Data2[j][2]<z+1:
            LIST3D[50][j][k]=LIST3D[50][j+1][k+Data2[j][2]]+max(k+Data2[j][2]-Data2[j][3],0)
            Process[i][j][k][0]=i
            Process[i][j][k][1]=j+1
            Process[i][j][k][2]=k+Data2[j][2]
        else:
            LIST3D[50][j][k]=inf
    j=j-1
    


for i in range (49, -1, -1):
    for j in range (49, -1, -1):
        for k in range(z,-1,-1):
            min_v=inf
            if len(Hsetlist[i][j])!=0:
                for (i,j,ii,jj) in Hsetlist[i][j]:
                    if k+max(sum_p(Data1,i,ii),sum_p(Data2,j,jj))<z+1 and min_v> func_L(Data1,Data2,LIST3D,k,i,j,ii,jj):
                        min_v=func_L(Data1,Data2,LIST3D,k,i,j,ii,jj) 
                        
                        Process[i][j][k][0]=ii+1
                        Process[i][j][k][1]=jj+1
                        Process[i][j][k][2]=k+max(sum_p(Data1,i,ii),sum_p(Data2,j,jj))
                        
            if v0+sum_delta(Data1,0,i-1)+sum_delta(Data2,0,j-1)-Data1[i][0]>=0 and k+Data1[i][2]<z+1 and min_v>LIST3D[i+1][j][k+Data1[i][2]]+max(k+Data1[i][2]-Data1[i][3],0):
                min_v=LIST3D[i+1][j][k+Data1[i][2]]+max(k+Data1[i][2]-Data1[i][3],0)
                
                Process[i][j][k][0]=i+1
                Process[i][j][k][1]=j
                Process[i][j][k][2]=k+Data1[i][2]
                
            if v0+sum_delta(Data1,0,i-1)+sum_delta(Data2,0,j-1)-Data2[j][0]>=0 and k+Data2[j][2]<z+1 and min_v>LIST3D[i][j+1][k+Data2[j][2]]+max(k+Data2[j][2]-Data2[j][3],0):
                min_v=LIST3D[i][j+1][k+Data2[j][2]]+max(k+Data2[j][2]-Data2[j][3],0)
                
                Process[i][j][k][0]=i
                Process[i][j][k][1]=j+1
                Process[i][j][k][2]=k+Data2[j][2]
                
            LIST3D[i][j][k]=min_v
print(LIST3D[0][0][0])

i=0
j=0
k=0
while i<50 or j<50:
    print(Process[i][j][k][0],Process[i][j][k][1])
    i=Process[i][j][k][0]
    j=Process[i][j][k][1]
    k=Process[i][j][k][2]
    