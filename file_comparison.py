class File_comparison:
    def __init__(self,file1,file2,outputFile):
        self.file1=file1
        self.file2=file2
        self.outputFile=outputFile
    def initiate_comparison(self):
        from bs4 import BeautifulSoup
        import filecmp
        with open (self.file1) as f:
            file1_lines = f.readlines()
        with open (self.file2) as f:
            file2_lines = f.readlines()
        file1_lines='\n'.join(file1_lines)
        file2_lines="\n".join(file2_lines)
        if filecmp.cmp(self.file1,self.file2, shallow=False) ==True:
            compare=False
            print("The files are the same")
        elif bool(BeautifulSoup(file1_lines, "html.parser").find())==True or bool(BeautifulSoup(file2_lines, "html.parser").find())==True:
            compare=False
            print("Error: HTML cannot be present in the files")
        else:
            compare=True
        return compare
    def raw_comparison(self):
        from difflib import Differ
        
        with open (self.file1) as f:
            file1_lines = f.readlines()
        with open (self.file2) as f:
            file2_lines = f.readlines()
        d = Differ()
        difference = list(d.compare(file1_lines, file2_lines))
        difference2 = '\n'.join(difference)
        print(difference2)
        return file1_lines, file2_lines, difference
    
    #Formatting
    def editing_a_line(self,changes,change,nextLine,previousLine,nextNextLine,previousPreviousLine):
        if change[0]=="+" and "?" in nextLine:
                for y in range(0,len(change)):
                    if nextLine[y]=="+" or nextLine[y]=="^":
                        if change[y]==" ":
                            changes.write("<mark style='background-color: green;display: inline-block;'>&#160</mark>")
                        else:
                            changes.write(f"<div style='background-color: green; color: black;display: inline-block;'>{change[y]}</div>")
                    else:
                        if change[y]==" ":
                            changes.write("<mark style='background-color: #ddffdd;display: inline-block;'>&#160</mark>")
                        else:
                            changes.write(f"<div style='background-color: #ddffdd; color: black;display: inline-block; '>{change[y]}</div>")
                changes.write("<br>")
                return "editted"
        elif change[0]=="-" and "?" in nextLine:
                for y in range(0,len(change)):
                    if nextLine[y]=="-" or nextLine[y]=="^":
                        if change[y]==" ":
                            changes.write("<mark style='background-color: red;display: inline-block;'>&#160</mark>")
                        else:
                            changes.write(f"<div style='background-color: red; color: black;display: inline-block; '>{change[y]}</div>")
                    else:
                        if change[y]==" ":
                            changes.write("<mark style='background-color: rgba(255, 0, 0, 0.5); display: inline-block;'>&#160</mark>")
                        else:
                            changes.write(f"<div style='background-color: rgba(255, 0, 0, 0.5); color: black;display: inline-block; '>{change[y]}</div>")
                changes.write("<br>")
                return "editted"
    def adding_a_line(self,changes,change,file1_lines,file2_lines):
        if change[2: ] in file2_lines and change[2: ] not in file1_lines:
            changes.write(f"<div style='background-color: green; color: black;display: inline-block; '>{change}</div><br>")
            return "added"               
    def deleting_a_line(self,changes,change,file1_lines,file2_lines):
        if change[2: ] in file1_lines and change[2: ] not in file2_lines:
                changes.write(f"<div style='background-color: red; color: black;display: inline-block; '>{change}</div><br>")
                return "deleted"
    def no_change(self,changes,change,file1_lines,file2_lines):
        if change[2: ] in file1_lines and change[2: ] in file2_lines:
            changes.write(f"<div style='color: black;display: inline-block; '>{change}</div><br>")
            
    def main(self):
        changes=open(self.outputFile,"w")
        compare=self.initiate_comparison()
        if compare:
            file1_lines,file2_lines,difference=self.raw_comparison()
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
                    oneIndexBelow=difference[x-1]
                except IndexError:
                    oneIndexAbove=" "
                    oneIndexBelow=" "
                if len(difference[x])>len(oneIndexAbove) and oneIndexAbove[0]=="?":
                    oneIndexAbove=oneIndexAbove+(" "*(len(difference[x])-len(difference[x+1])))
                elif len(difference[x])<len(oneIndexAbove) and oneIndexAbove[0]=="?":
                    difference[x]=difference[x]+(" "*(len(oneIndexAbove)-len(difference[x])))
                if difference[x][0]=="?":
                    pass
                added=""
                deleted=""
                editted=""
                editted=self.editing_a_line(changes,difference[x],oneIndexAbove,oneIndexBelow,twoIndexAbove,twoIndexBelow)
                if editted!="editted":
                    added=self.adding_a_line(changes,difference[x],file1_lines,file2_lines)
                if added!="added" and editted!="editted":
                    deleted=self.deleting_a_line(changes,difference[x],file1_lines,file2_lines)
                if deleted!="deleted" and added!="added" and editted!="editted":
                    self.no_change(changes,difference[x],file1_lines,file2_lines)
                x=x+1
        changes.close()
import sys
if len(sys.argv)!=4:
    print("Usage: <file1> <file2> <outputFile>")
file1=sys.argv[1]
file2=sys.argv[2]
outputFile=sys.argv[3]

comparison=File_comparison(r""+(file1),r""+(file2),r""+outputFile)
comparison.main()

#Unable to test command line compatibility on my system