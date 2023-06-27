#Initiate comparison?
import filecmp
if filecmp.cmp(r"C:\Users\sanpo\OneDrive\Desktop\original.txt",r"C:\Users\sanpo\OneDrive\Desktop\changed.txt", shallow=False) ==True:
    quit()

#comparison
from difflib import Differ

with open (r"C:\Users\sanpo\OneDrive\Desktop\original.txt") as f:
    file1_lines = f.readlines()
with open (r"C:\Users\sanpo\OneDrive\Desktop\changed.txt") as f:
    file2_lines = f.readlines()
d = Differ()
difference = list(d.compare(file1_lines, file2_lines))
difference2 = '\n'.join(difference)
print(difference2)
#Formatting
size=20
changes=open(r"C:\Users\sanpo\OneDrive\Desktop\changes.html","w")
x=0
while len(difference)-x>=1:
    try:
        twoIndexAbove=difference[x+2]
        twoIndexBelow=difference[x-2]
    except IndexError:
        twoIndexAbove=" "
        twoIndexBelow=" "
    try:
        oneIndexAbove=difference[x+1]
    except IndexError:
        oneIndexAbove=" "
    if len(difference[x])>len(oneIndexAbove) and oneIndexAbove[0]=="?":
        oneIndexAbove=oneIndexAbove+(" "*(len(difference[x])-len(difference[x+1])))
    elif len(difference[x])<len(oneIndexAbove) and oneIndexAbove[0]=="?":
        difference[x]=difference[x]+(" "*(len(oneIndexAbove)-len(difference[x])))
    if difference[x][0]=="?":
        pass
    #Adding and deleting in a line
    elif (oneIndexAbove[0]=="+" and twoIndexAbove[0]=="?") or (twoIndexBelow[0]=="-" and difference[x-1][0]=="?" and oneIndexAbove[0]!="?"):
            pass
    elif difference[x][0]=="+" and "?" in oneIndexAbove:
            for y in range(0,len(difference[x])):
                if oneIndexAbove[y]=="+" or oneIndexAbove[y]=="^":
                    if difference[x][y]==" ":
                        changes.write(f"<mark style='background-color: green; font-size: {size};display: inline-block;'>&#160</mark>")
                    else:
                        changes.write(f"<div style='background-color: green; color: black;display: inline-block; font-size: {size};'>{difference[x][y]}</div>")
                else:
                    if difference[x][y]==" ":
                        changes.write(f"<mark style='background-color: #ddffdd; font-size: {size};display: inline-block;'>&#160</mark>")
                    else:
                        changes.write(f"<div style='background-color: #ddffdd; color: black;display: inline-block; font-size: {size};'>{difference[x][y]}</div>")
            changes.write("<br>")
    elif difference[x][0]=="-" and "?" in oneIndexAbove:
            for y in range(0,len(difference[x])):
                if oneIndexAbove[y]=="-" or oneIndexAbove[y]=="^":
                    if difference[x][y]==" ":
                        changes.write(f"<mark style='background-color: red; font-size: {size};height: 20;'>&#160</mark>")
                    else:
                        changes.write(f"<div style='background-color: red; color: black;display: inline-block; font-size: {size};'>{difference[x][y]}</div>")
                else:
                    if difference[x][y]==" ":
                        changes.write(f"<mark style='background-color: rgba(255, 0, 0, 0.5); font-size: {size};display: inline-block;'>&#160</mark>")
                    else:
                        changes.write(f"<div style='background-color: rgba(255, 0, 0, 0.5); color: black;display: inline-block; font-size: {size};'>{difference[x][y]}</div>")
            changes.write("<br>")
    
    #Adding entire line
    elif difference[x][2: ] in file2_lines and difference[x][2: ] not in file1_lines:
        changes.write(f"<div style='background-color: green; color: black;display: inline-block; font-size: {size};'>{difference[x]}</div><br>")
        
    #Deleting entire line
    elif difference[x][2: ] in file1_lines and difference[x][2: ] not in file2_lines:
            changes.write(f"<div style='background-color: red; color: black;display: inline-block; font-size: {size};'>{difference[x]}</div><br>")
   
    #No change
    elif difference[x][2: ] in file1_lines and difference[x][2: ] in file2_lines:
        changes.write(f"<div style='color: black;display: inline-block; font-size: {size};'>{difference[x]}</div><br>")
    x=x+1
changes.close()
    