class File_comparison:
    def __init__(self,file1,file2):
        self.file1=file1
        self.file2=file2
    def initiate_comparison(self):
        import filecmp
        if filecmp.cmp(self.file1,self.file2, shallow=False) ==True:
            compare=False
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
        print(difference)
        difference2 = '\n'.join(difference)
        print(difference2)
        return file1_lines, file2_lines, difference
    #Formatting
    def editing_a_line(self,changes,change,nextLine,previousLine,nextNextLine,previousPreviousLine):
        if change[0]=="+" and "?" in nextLine:
                for y in range(0,len(change)):
                    if nextLine[y]=="+" or nextLine[y]=="^":
                        if change[y]==" ":
                            changes.write(f"<mark style='background-color: green;display: inline-block;'>&#160</mark>")
                        else:
                            changes.write(f"<div style='background-color: green; color: black;display: inline-block;'>{change[y]}</div>")
                    else:
                        if change[y]==" ":
                            changes.write(f"<mark style='background-color: #ddffdd;display: inline-block;'>&#160</mark>")
                        else:
                            changes.write(f"<div style='background-color: #ddffdd; color: black;display: inline-block; '>{change[y]}</div>")
                changes.write("<br>")
                return "editted"
        elif change[0]=="-" and "?" in nextLine:
                for y in range(0,len(change)):
                    if nextLine[y]=="-" or nextLine[y]=="^":
                        if change[y]==" ":
                            changes.write(f"<mark style='background-color: red; height: 20;'>&#160</mark>")
                        else:
                            changes.write(f"<div style='background-color: red; color: black;display: inline-block; '>{change[y]}</div>")
                    else:
                        if change[y]==" ":
                            changes.write(f"<mark style='background-color: rgba(255, 0, 0, 0.5); display: inline-block;'>&#160</mark>")
                        else:
                            changes.write(f"<div style='background-color: rgba(255, 0, 0, 0.5); color: black;display: inline-block; '>{change[y]}</div>")
                changes.write("<br>")
                print("editted")
                return "editted"
    def adding_a_line(self,changes,change,file1_lines,file2_lines):
        if change[2: ] in file2_lines and change[2: ] not in file1_lines:
            changes.write(f"<div style='background-color: green; color: black;display: inline-block; '>{change}</div><br>")
            return "added"               
    def deleting_a_line(self,changes,change,file1_lines,file2_lines):
        if change[2: ] in file1_lines and change[2: ] not in file2_lines:
                print("no")
                changes.write(f"<div style='background-color: red; color: black;display: inline-block; '>{change}</div><br>")
                return "deleted"
    def no_change(self,changes,change,file1_lines,file2_lines):
        if change[2: ] in file1_lines and change[2: ] in file2_lines:
            changes.write(f"<div style='color: black;display: inline-block; '>{change}</div><br>")
    def main(self):
        changes=open(r"C:\Users\sanpo\OneDrive\Desktop\changes.html","w")
        compare=self.initiate_comparison()
        print(compare)
        if compare:
            file1_lines,file2_lines,difference=self.raw_comparison()
            print(file1_lines)
            print(file2_lines)
            print(difference)
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
comparison=File_comparison(r"C:\Users\sanpo\OneDrive\Desktop\original.txt",r"C:\Users\sanpo\OneDrive\Desktop\changed.txt")
comparison.main()