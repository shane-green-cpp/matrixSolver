# Importing NumPy Library
from numpy import array, zeros, fabs
import sys

fileName = sys.argv[len(sys.argv) - 1]
sysEqnFile = open(fileName, "r")

contents = sysEqnFile.read()
sysEqnFile.close()
n = int(contents[0])
if sys.argv[1] == "--spp":
    spp = True
else:
    spp = False
a = zeros((n,n), float)
b = zeros(n, float)
x = zeros(n, float)
ind = zeros(n, int)
for num in range(n):
    ind[num] = num

def stringFormater(contents):
    lines = contents.split('\n')
    bnums = lines[len(lines) - 2].split(' ')
    print(bnums)
    for i in range(n):
        nums = lines[i+1].split(' ')
        print(nums)
        for j in range(n):
            a[i][j] = float(nums[j])
    for k in range(n):
        b[k] = float(bnums[k])

stringFormater(contents)

eqnSolFile = fileName[0:len(fileName) - 3] + "sol"
print(eqnSolFile)

def writeSolution(x):
    if spp:
        type = " SPP "
    else:
        type = " NGE "
    f = open(eqnSolFile, "w")
    f.write("solution to the system")
    f.write(type)
    f.write(str(x))
    f.close()

#spp forward elim algo function
def sppForwardElimination(a, b, ind, n):
    scaling = zeros(n, float)
    #this sets scaling equal to the largest num in each of the rows
    for i in range(n):
        smax = 0 #scale max
        for j in range(n):
            smax = max(smax, fabs(a[i][j]))
        scaling[i] = smax
    
    for k in range(n-1):
        rmax = 0 #row max
        maxInd = k
        for i in range(k,n):
            r = fabs(a[ind[i]][k] / scaling[ind[i]])
            if r > rmax:
                rmax = r
                maxInd = i
        #the swap
        temp = ind[maxInd]
        ind[maxInd] = ind[k]
        ind[k] = temp

        for i in range(k+1,n):
            if a[i,k] == 0:continue
            mult = a[ind[i],k]/a[ind[k],k]
            for j in range(k,n):
                a[ind[i],j] = a[ind[i],j] - (mult * a[ind[k],j])
            b[ind[i]] = b[ind[i]] - (mult * b[ind[k]])

#spp back sub
def sppBackSub(a, b, x, ind, n):
    x[n-1] = b[ind[n-1]] / a[ind[n-1], n-1]
    for i in range(n-1, -1, -1):
        sum = b[ind[i]]
        for j in range(i+1, n):
            sum = sum - (a[ind[i],j] * x[j])
        x[i] = sum / a[ind[i]][i]
        

#forward elim algo function
def forwardElimination(a, b, n):
    for k in range(n-1):
        for i in range(k+1,n):
            if a[i,k] == 0:continue
            mult = a[i,k]/a[k,k]
            for j in range(k,n):
                a[i,j] = a[i,j] - (mult * a[k,j])
            b[i] = b[i] - (mult * b[k])

#back sub algo function  
def backSub(a, b, x, n):
    x[n-1] = b[n-1] / a[n-1, n-1]
    for i in range(n-1, -1, -1):
        sum = b[i]
        for j in range(i+1, n):
            sum = sum - (a[i,j] * x[j])
        x[i] = sum / a[i][i]
if spp:
    sppForwardElimination(a,b,ind,n)
    sppBackSub(a,b,x,ind,n)
    print("spp")
else:
    forwardElimination(a, b, n)
    backSub(a, b, x, n)
    print("naive")

print("solution to the system")
print(x)
writeSolution(x)