from pandas import DataFrame
class compare_directories:
    def __init__ (self,directory1,directory2,sender_email,receiver_email):
        self.directory1=directory1
        self.directory2=directory2
        self.sender_email=sender_email
        self.receiver_email=receiver_email
    def comparison(self):
        import os
        from difflib import Differ
        path = self.directory1
        file1_names=[]
        file2_names=[]
        comparisons=[]
        for dirpath, dirs,f_names in os.walk(path):
            files=f_names
        for x in range(0,len(files)):
            with open (self.directory1+"\\"+files[x]) as f:
                file1_lines = f.readlines()
            with open (self.directory2+"\\"+files[x]) as f:
                file2_lines = f.readlines()
            d = Differ()
            difference = list(d.compare(file1_lines, file2_lines))
            difference2 = '\n'.join(difference)
            if "+" not in difference2 and "-" not in difference2:
                file1_names.append(files[x])
                file2_names.append(files[x])
                comparisons.append("same")
            else:
                file1_names.append(files[x])
                file2_names.append(files[x])
                comparisons.append("different")
        return file1_names,file2_names,comparisons
    def create_table(self):
        file1_names,file2_names,comparisons=self.comparison()
        raw_comparisons={}
        raw_comparisons["File 1"]=file1_names
        raw_comparisons["File 2"]=file2_names
        raw_comparisons["Result"]=comparisons
        table=DataFrame(raw_comparisons)
        return table
    def export_table_to_email(self):
        
        import smtplib, ssl
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        
        port = 587
        smtp_server = "smtp-mail.outlook.com"
        sender_email = self.sender_email  # Enter your address
        receiver_email = self.receiver_email  # Enter receiver address
        password = input("Type your password and press enter: ")
        table=self.create_table()
        html=table.to_html(classes='table',index=False)
        
        
        
        email_message = MIMEMultipart()
        
        part1 = MIMEText(html, 'html')
        
        email_message.attach(part1)
        email_string = email_message.as_string()
        
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email,""+ email_string)
        print("Email successfully sent")
    def main(self):
       self.create_table()
       self.export_table_to_email()
       

import sys
if len(sys.argv)!=5:
    print("Usage: <Directory1> <Directory2> <sender_email> <receiver_email>")
directory1=sys.argv[1]
directory2=sys.argv[2]
sender_email=sys.argv[3]
receiver_email=sys.argv[4]
comparison=compare_directories(r""+directory1,r""+directory2,sender_email,receiver_email)
comparison.main()

#Unable to test command line compatibility on my system