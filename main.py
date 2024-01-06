import tkinter
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk ,ImageFilter
import os
import mysql.connector
import datetime
import cv2
import csv
import numpy as np
import pandas as pd
import math
import random
import string
import smtplib
import ssl
from PIL import Image, ImageTk 
root =Tk()
root.title("Home Page")
root.geometry("1080x650+100+20")
root.resizable(False, False) 
global root_window
is_admin = False
root_window = root

def draw_admin():
    def draw_edit_employee():
        def search():
            option = dropdown.get()
            search_input = searchInput.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            if search_input == "":  
                mycursor.execute("SELECT * FROM employee_table")
            elif option == "Name":
                mycursor.execute("SELECT * FROM employee_table WHERE name = '" + str(search_input).upper() + "'")
            elif option == "UID":
                mycursor.execute("SELECT * FROM employee_table WHERE id = '" + str(search_input) + "'")
            elif option == "Designation":
                mycursor.execute("SELECT * FROM employee_table WHERE desg = '" + str(search_input) + "'")
            elif option == "Department":
                mycursor.execute("SELECT * FROM employee_table WHERE dept = '" + str(search_input).upper() + "'")
            else:
                return
            rows = mycursor.fetchall()
            data_table.delete(*data_table.get_children())
            if rows == None:
                note_text['text'] = "Data: 0 Rows"
                return 
            note_text['text'] = "Data: "+str(len(rows))+" Rows"
            for row in rows:
                data_table.insert('', END, values=row)
            db.commit()
            db.close()
            # pass


        # IT WILL SHOW VALUE FROM DATABASE
        def show():
            id = IdEntry.get()
            nam = NameEntry.get()
            desig = DesignationEntry.get()
            dept = DepartmentEntry.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            mycursor.execute("select * from employee_table")
            rows = mycursor.fetchall()
            if len(rows) != 0:
                data_table.delete(*data_table.get_children())
            for row in rows:
                data_table.insert('', END, values=row)
            db.commit()
            db.close()

        # IT WILL GET DATA IN LEFTBOX (getdata made events there and fecth value there also)
        def getdata(event):
            currow = data_table.focus()
            contents = data_table.item(currow)
            row = contents['values']
            updatebt.configure(state = "normal")
            deletebt.configure(state = "normal")
            IdEntry.configure(state='normal')
            IdEntry.delete(0, END)
            NameEntry.delete(0, END)
            DesignationEntry.delete(0, END)
            DepartmentEntry.delete(0, END)
            IdEntry.insert(0, row[0])
            IdEntry.configure(state='readonly')
            NameEntry.insert(0, row[1])
            DesignationEntry.insert(0, row[2])
            DepartmentEntry.insert(0, row[3])
            addbt.configure(state = 'disabled')

        # IT WILL ADD DATAS
        def add():
            if IdEntry.get()=="" or NameEntry.get()=="" or DesignationEntry.get()=="" or DepartmentEntry.get()=="":
               messagebox.showerror("Error","All fields are required")
            else:
                iD=IdEntry.get()
                name=NameEntry.get()
                desg=DesignationEntry.get()
                dept=DepartmentEntry.get()
                db=mysql.connector.connect(host="localhost",user="root",password="",database="KBP")
                mycursor=db.cursor()
                try:
                   mycursor.execute("INSERT INTO employee_table (id,name,desg,dept) VALUES ('"+str(iD)+"', '"+str(name).upper()+"', '"+str(desg).upper()+"', '"+str(dept).upper()+"')")
                   db.commit()
                   messagebox.showinfo("information","Record Inserted successfully")
                   search()
                   clear()
                except EXCEPTION as e:
                   print(e)
                   db.rollback()
                   db.close()

        def update():
            iD = IdEntry.get()
            name = NameEntry.get()
            desg = DesignationEntry.get()
            dept = DepartmentEntry.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            mycursor.execute("UPDATE employee_table SET name = '"+str(name).upper()+"', desg = '"+str(desg)+"', dept = '"+str(dept).upper()+"' WHERE id = '"+str(iD)+"'")
            db.commit()
            messagebox.showinfo("information", "Record Updated successfully")
            IdEntry.delete(0, END)
            NameEntry.delete(0, END)
            DesignationEntry.delete(0, END)
            DepartmentEntry.delete(0, END)
            search()
            clear()

        def delete1():
            iD = IdEntry.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            sql = "DELETE FROM employee_table WHERE id='"+str(iD)+"'"
            mycursor.execute(sql)
            db.commit()
            messagebox.showinfo("information", "Record Deleted successfully")
            IdEntry.delete(0, END)
            NameEntry.delete(0, END)
            DesignationEntry.delete(0, END)
            DepartmentEntry.delete(0, END)
            search()
            clear()


        # IT WILL CLEAR DATAS
        def clear():
            updatebt.configure(state = "disabled")
            deletebt.configure(state = "disabled")
            IdEntry.configure(state='normal')
            IdEntry.delete(0, END)
            IdEntry.insert(0,random_string())
            NameEntry.delete(0, END)
            DesignationEntry.delete(0, END)
            DepartmentEntry.delete(0, END)
            NameEntry.focus_set()
            addbt.configure(state='normal')
        def random_string():
            count = 1
            S = 5
            while(count!=0):
                ran = ''.join(random.choices(string.ascii_letters + string.digits, k = S))
                db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
                mycursor = db.cursor()
                mycursor.execute("select count(id) from employee_table where id = '"+str(ran)+"'")
                rows = mycursor.fetchone()
                count = rows[0]
            return ran
        #He
        label=Frame(footer,bd=0,bg="brown")
        label.place(x=0,y=0,width=1080,height=85)
        abcframe=Frame(footer,bd=0,bg="black")
        abcframe.place(x=90,y=15,width=900,height=1)
        ILabel=Label(label,text="Here You Can Edit Or View Employee database",font=("Helvetica",20),fg="#eae2b7",bg="brown")
        ILabel.place(x=250, y =30)
        
        leftbox=Frame(dashboard,bd=0,bg="brown")
        leftbox.place(x=0,y=50,width=600,height=450)
        # INSIDE LEFT BOX
        leftbox_title=Label(leftbox,text="Manage Database",font=("Helvetica",25,"bold"),fg="#eae2b7",bg="brown")
        leftbox_title.place(x=50, y=10)
        IdLabel=Label(leftbox,text="ID",font=("Helvetica",20),fg="#eae2b7",bg="brown")
        IdLabel.place(x=30, y =50)
        IdEntry=Entry(leftbox,font=("Helvetica",20),bd=0)
        IdEntry.insert(0,random_string())
        IdEntry.place(x=200, y =50, width = 120)
        NameLabel=Label(leftbox,text="Name",font=("Helvetica", 20),fg="#eae2b7",bg="brown")
        NameLabel.place(x=30, y=100)
        NameEntry=Entry(leftbox,font=("Helvetica", 20),bd=0)
        NameEntry.place(x=140, y=100, width = 200)
        DesignationLabel=Label(leftbox,text="Designation",font=("Helvetica", 20),fg="#eae2b7",bg="brown")
        DesignationLabel.place(x=30, y=150)
        DesignationEntry=Entry(leftbox,font=("Helvetica", 20),bd=0)
        DesignationEntry.place(x=220, y=150, width = 150)
        DepartmentLabel=Label(leftbox,text="Department",font=("Helvetica", 20),fg="#eae2b7",bg="brown")
        DepartmentLabel.place(x=30, y=200)
        DepartmentEntry=Entry(leftbox,font=("Helvetica", 20),bd=0)
        DepartmentEntry.place(x=220, y=200, width = 150)

        # LEFT BOX BUTTONS
        btnfrm=Frame(leftbox, bd=0, bg="brown")
        btnfrm.place(x=10,y=250,width=350,height=50)

        addbt=Button(btnfrm,text="Add",font=("Helvetica", 15),bg="indianred",fg="white",bd=0,command=add)
        addbt.place(x=50, y=0, width = 100)
        updatebt=Button(btnfrm,text="Edit",font=("Helvetica", 15),bg="indianred",fg="white",bd=0,command=update)
        updatebt.configure(state = "disabled")
        updatebt.place(x=180, y=0, width = 120)

        btnfrm2=Frame(leftbox,relief=RIDGE,bg="brown")
        btnfrm2.place(x=10,y=300,width=350,height=50)

        deletebt=Button(btnfrm2,text="Delete",font=("Helvetica", 15),bg="indianred",fg="white",command=delete1, bd =0)
        deletebt.configure(state = "disabled")
        deletebt.place(x=50, y=0, width = 130)
        clrbt=Button(btnfrm2,text="Clear",font=("Helvetica", 15),bg="indianred",fg="white",command=clear, bd = 0)
        clrbt.place(x=200, y=0, width = 130)






        # RIGHT BOX
        rightbox=Frame(dashboard,bd=0,bg="indianred")
        rightbox.place(x=450,y=50,width=630,height=450)

        # RIGHT BOX HEADING
        searchBy=Label(rightbox,text="Enter Value",font=("Helvetica", 14),bg="indianred",fg="white")
        searchBy.place(x=10, y=10)
        searchInput=Entry(rightbox,font=("Helvetica", 12),bd=0,width=17)
        searchInput.place(x=130, y=10, height = 30)
        dropdown=ttk.Combobox(rightbox,font=("Helvetica",12),state='readonly', width = 12)
        dropdown['values']=("--Search By--", "Name", "UID", "Designation", "Department")
        dropdown.current(0)
        dropdown.place(x=300, y=10, height = 30)
        searchBtn=Button(rightbox,text="Search",command=search,font=("Helvetica", 12),width=10, bd = 0)
        searchBtn.place(x=450, y=10, height = 30)

        # BOX INSIDE RIGHT BOX
        tabfrm=Frame(rightbox,bd=4,relief=RIDGE,bg="lightblue")
        tabfrm.place(x=10,y=50,width=550,height=270)
        scrolly=Scrollbar(tabfrm,orient=VERTICAL)
        data_table=ttk.Treeview(tabfrm,columns=("id","name","Designation","department"),yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=data_table.yview)

        note_text=Label(rightbox,font=("Helvetica", 10),bg="indianred",fg="white")
        note_text.place(x=10, y=325)

        # INSIDE RIGHT BOX
        data_table.heading("id",text="ID")
        data_table.heading("name",text="Name")
        data_table.heading("Designation",text="Designation")
        data_table.heading("department",text="Department")
        data_table['show']="headings"
        data_table.column("id",width = 10)
        data_table.column("name",width=200)
        data_table.column("Designation",width=30)
        data_table.column("department",width=30)
        data_table.pack(fill=BOTH,expand=1)
        data_table.bind("<ButtonRelease-1>",getdata)
        search()
    def draw_change_password():
        
        def change_pwd():
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            mycursor.execute("SELECT y FROM global_values WHERE x = 'admin'")
            rows = mycursor.fetchone()
            if rows == None:
                messagebox.showerror("Failure",  "Oops! Something went wrong")
                return
            server_pwd = rows[0]
            db.commit()
            if CurrentPwd.get() == server_pwd:
                if NewPwd.get() == NewPwd2.get():
                    try:
                        mycursor.execute("UPDATE global_values SET y = '"+str(NewPwd.get())+"' WHERE x = 'admin'")
                        db.commit()
                        messagebox.showinfo("Success",  "Password changed")
                    except EXCEPTION as e:
                        messagebox.showerror("Failure",  e)
                        db.rollback()
                        db.close()
                else:
                    messagebox.showerror("Failure",  "New Passwords didn't match")

            else:
                messagebox.showerror("Failure",  "Oops! Something went wrong")
            CurrentPwd.delete(0, END)
            NewPwd.delete(0, END)
            NewPwd2.delete(0, END)
            root_window.destroy()
            

       

        label=Frame(footer,bd=0,bg="brown")
        label.place(x=0,y=0,width=1080,height=85)
        abcframe=Frame(footer,bd=0,bg="black")
        abcframe.place(x=90,y=15,width=900,height=1)
        ILabel=Label(label,text="Here You Can Change Password",font=("Helvetica",20),fg="#eae2b7",bg="brown")
        ILabel.place(x=350, y =30)
        #panel
        panel=Frame(dashboard, bg="#fff", bd=0)
        panel.place(x=0,y=50,width=1080,height=375)
        #panel_elements
        def on_enter(e):
            CurrentPwd.delete(0,'end')
        def on_leave(e):
            if CurrentPwd.get()=='':
                CurrentPwd.insert(0,'Current Password')

                
        CurrentPwd=Entry(panel,width=30,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        CurrentPwd.place(x=600,y=30)
        CurrentPwd.insert(0,'Current Password')
        CurrentPwd.bind("<FocusIn>",on_enter)
        CurrentPwd.bind("<FocusOut>",on_leave)
        Frame(panel,width=300,height=2,bg='black').place(x=600,y=55)
        def on_enter(e):
            NewPwd.delete(0,'end')
        def on_leave(e):
            if NewPwd.get()=='':
                NewPwd.insert(0,'New Password')

                
        NewPwd=Entry(panel,width=30,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        NewPwd.place(x=600,y=100)
        NewPwd.insert(0,'New Password')
        NewPwd.bind("<FocusIn>",on_enter)
        NewPwd.bind("<FocusOut>",on_leave)
        Frame(panel,width=300,height=2,bg='black').place(x=600,y=125)
        def on_enter(e):
            NewPwd2.delete(0,'end')
        def on_leave(e):
            if NewPwd2.get()=='':
                NewPwd2.insert(0,'Confirm Password')

                
        NewPwd2=Entry(panel,width=30,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        NewPwd2.place(x=600,y=180)
        NewPwd2.insert(0,'Conform Password')
        NewPwd2.bind("<FocusIn>",on_enter)
        NewPwd2.bind("<FocusOut>",on_leave)
        Frame(panel,width=300,height=2,bg='black').place(x=600,y=205)

        searchBtn=Button(panel,width=39,pady=7,text='Change Password',bg='#57a1f8',fg='white',border=0, command = change_pwd, font=("Helvetica",16,"bold"), bd = 0)
        searchBtn.place(x=600, y=260, height = 50, width = 250)

        img=PhotoImage(file='./media/pass.png')
        Label(panel,image=img,border=0,bg='white').place(x=50,y=70)
        print(1)
        dashboard.mainloop()


       

    def draw_edit_student():
        def search():
            option = dropdown.get()
            search_input = searchInput.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            if search_input == "":
                mycursor.execute("SELECT * FROM student_table")
            elif option == "Name":
                mycursor.execute("SELECT * FROM student_table WHERE name = '" + str(search_input).upper() + "'")
            elif option == "UID":
                mycursor.execute("SELECT * FROM student_table WHERE id = '" + str(search_input) + "'")
            elif option == "Semester":
                mycursor.execute("SELECT * FROM student_table WHERE sem = " + str(search_input))
            elif option == "Department":
                mycursor.execute("SELECT * FROM student_table WHERE stream = '" + str(search_input).upper() + "'")
            else:
                return
            rows = mycursor.fetchall()
            data_table.delete(*data_table.get_children())
            if rows == None:
                note_text['text'] = "Data: 0 Rows"
                return 
            note_text['text'] = "Data: "+str(len(rows))+" Rows"
            for row in rows:
                data_table.insert('', END, values=row)
            db.commit()
            db.close()
            # pass


        # IT WILL SHOW VALUE FROM DATABASE
        def show():
            id = IdEntry.get()
            nam = NameEntry.get()
            desig = SemesterEntry.get()
            dept = DepartmentEntry.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            mycursor.execute("select * from student_table")
            rows = mycursor.fetchall()
            if len(rows) != 0:
                data_table.delete(*data_table.get_children())
            for row in rows:
                data_table.insert('', END, values=row)
            db.commit()
            db.close()

        # IT WILL GET DATA IN LEFTBOX (getdata made events there and fecth value there also)
        def getdata(event):
            currow = data_table.focus()
            contents = data_table.item(currow)
            row = contents['values']
            updatebt.configure(state = "normal")
            deletebt.configure(state = "normal")
            IdEntry.configure(state='normal')
            IdEntry.delete(0, END)
            NameEntry.delete(0, END)
            SemesterEntry.delete(0, END)
            DepartmentEntry.delete(0, END)
            IdEntry.insert(0, row[0])
            IdEntry.configure(state='readonly')
            NameEntry.insert(0, row[1])
            SemesterEntry.insert(0, row[2])
            DepartmentEntry.insert(0, row[3])
            addbt.configure(state = 'disabled')

        # IT WILL ADD DATAS
        def add():
            if IdEntry.get()=="" or NameEntry.get()=="" or SemesterEntry.get()=="" or DepartmentEntry.get()=="":
               messagebox.showerror("Error","All fields are required")
            else:
                iD=IdEntry.get()
                name=NameEntry.get()
                sem=SemesterEntry.get()
                dept=DepartmentEntry.get()
                db=mysql.connector.connect(host="localhost",user="root",password="",database="KBP")
                mycursor=db.cursor()
                try:
                   sql="insert into student_details_table(id,name,profession,department)values(%s,%s,%s,%s)"
                   val=(id,name,sem,dept)
                   # mycursor.execute(sql,val)
                   mycursor.execute("INSERT INTO student_table (id,name,sem,stream) VALUES ('"+str(iD)+"', '"+str(name).upper()+"', "+str(sem)+", '"+str(dept).upper()+"')")
                   db.commit()
                   messagebox.showinfo("information","Record Inserted successfully")
                   show()
                   clear()
                except EXCEPTION as e:
                   print(e)
                   db.rollback()
                   db.close()

        def update():
            iD = IdEntry.get()
            name = NameEntry.get()
            sem = SemesterEntry.get()
            dept = DepartmentEntry.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            mycursor.execute("UPDATE student_table SET name = '"+str(name).upper()+"', sem = "+str(sem)+", stream = '"+str(dept).upper()+"' WHERE id = '"+str(iD)+"'")
            db.commit()
            messagebox.showinfo("information", "Record Updated successfully")
            IdEntry.delete(0, END)
            NameEntry.delete(0, END)
            SemesterEntry.delete(0, END)
            DepartmentEntry.delete(0, END)
            show()
            clear()

        def delete1():
            iD = IdEntry.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            sql = "DELETE FROM student_table WHERE id='"+str(iD)+"'"
            mycursor.execute(sql)
            db.commit()
            messagebox.showinfo("information", "Record Deleted successfully")
            IdEntry.delete(0, END)
            NameEntry.delete(0, END)
            SemesterEntry.delete(0, END)
            DepartmentEntry.delete(0, END)
            show()
            clear()

        # IT WILL CLEAR DATAS
        def clear():
            updatebt.configure(state = "disabled")
            deletebt.configure(state = "disabled")
            IdEntry.configure(state='normal')
            IdEntry.delete(0, END)
            IdEntry.insert(0,random_string())
            NameEntry.delete(0, END)
            SemesterEntry.delete(0, END)
            DepartmentEntry.delete(0, END)
            NameEntry.focus_set()
            addbt.configure(state='normal')
        def random_string():
            count = 1
            S = 5
            while(count!=0):
                ran = ''.join(random.choices(string.ascii_letters + string.digits, k = S))
                db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
                mycursor = db.cursor()
                mycursor.execute("select count(id) from student_table where id = '"+str(ran)+"'")
                rows = mycursor.fetchone()
                count = rows[0]
            return ran
        label=Frame(footer,bd=0,bg="brown")
        label.place(x=0,y=0,width=1080,height=85)
        abcframe=Frame(footer,bd=0,bg="black")
        abcframe.place(x=90,y=15,width=900,height=1)
        ILabel=Label(label,text="Here You Can Edit Or View Student database",font=("Helvetica",20),fg="#eae2b7",bg="brown")
        ILabel.place(x=260, y =30)
        # LEFT BOX
        leftbox=Frame(dashboard,bd=0,bg="brown")
        leftbox.place(x=0,y=50,width=600,height=450)
        # INSIDE LEFT BOX
        leftbox_title=Label(leftbox,text="Manage Database",font=("Helvetica",20,"bold"),fg="#eae2b7",bg="brown")
        leftbox_title.place(x=100, y=10)
        IdLable=Label(leftbox,text="ID",font=("Helvetica",15),fg="#eae2b7",bg="brown")
        IdLable.place(x=70, y =60)
        IdEntry=Entry(leftbox,font=("Helvetica",15),bd=0)
        IdEntry.insert(0,random_string())
        IdEntry.place(x=260, y =70, width = 80)
        NameLable=Label(leftbox,text="Name",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
        NameLable.place(x=60, y=110)
        NameEntry=Entry(leftbox,font=("Helvetica", 15),bd=0)
        NameEntry.place(x=140, y=110, width = 200)
        SemesterLable=Label(leftbox,text="Semester",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
        SemesterLable.place(x=60, y=160)
        SemesterEntry=Entry(leftbox,font=("Helvetica", 15),bd=0)
        SemesterEntry.place(x=160, y=160, width = 180)
        DepartmentLable=Label(leftbox,text="Department",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
        DepartmentLable.place(x=60, y=210)
        DepartmentEntry=Entry(leftbox,font=("Helvetica", 15),bd=0)
        DepartmentEntry.place(x=190, y=210, width = 150)

        # LEFT BOX BUTTONS
        btnfrm=Frame(leftbox, bd=0, bg="brown")
        btnfrm.place(x=10,y=250,width=350,height=50)

        addbt=Button(btnfrm,text="Add",font=("Helvetica", 15),bg="indianred",fg="white",bd=0,command=add)
        addbt.place(x=50, y=0, width = 130)
        updatebt=Button(btnfrm,text="Edit",font=("Helvetica", 15),bg="indianred",fg="white",bd=0,command=update)
        updatebt.configure(state = "disabled")
        updatebt.place(x=200, y=0, width = 130)

        btnfrm2=Frame(leftbox,relief=RIDGE,bg="brown")
        btnfrm2.place(x=10,y=300,width=350,height=50)

        deletebt=Button(btnfrm2,text="Delete",font=("Helvetica", 15),bg="indianred",fg="white",command=delete1, bd =0)
        deletebt.configure(state = "disabled")
        deletebt.place(x=50, y=0, width = 130)
        clrbt=Button(btnfrm2,text="Clear",font=("Helvetica", 15),bg="indianred",fg="white",command=clear, bd = 0)
        clrbt.place(x=200, y=0, width = 130)






        # RIGHT BOX
        rightbox=Frame(dashboard,bd=0,bg="indianred")
        rightbox.place(x=450,y=50,width=630,height=450)

        # RIGHT BOX HEADING
        searchBy=Label(rightbox,text="Enter Value",font=("Helvetica", 14),bg="indianred",fg="white")
        searchBy.place(x=10, y=10)
        searchInput=Entry(rightbox,font=("Helvetica", 12),bd=0,width=17)
        searchInput.place(x=130, y=10, height = 30)
        dropdown=ttk.Combobox(rightbox,font=("Helvetica",12),state='readonly', width = 12)
        dropdown['values']=("--Search By--", "Name", "UID", "Designation", "Department")
        dropdown.current(0)
        dropdown.place(x=300, y=10, height = 30)
        searchBtn=Button(rightbox,text="Search",command=search,font=("Helvetica", 12),width=10, bd = 0)
        searchBtn.place(x=450, y=10, height = 30)

        # BOX INSIDE RIGHT BOX
        tabfrm=Frame(rightbox,bd=4,relief=RIDGE,bg="lightblue")
        tabfrm.place(x=10,y=50,width=550,height=270)
        scrolly=Scrollbar(tabfrm,orient=VERTICAL)
        data_table=ttk.Treeview(tabfrm,columns=("id","name","semester","department"),yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=data_table.yview)

        note_text=Label(rightbox,font=("Helvetica", 10),bg="indianred",fg="white")
        note_text.place(x=10, y=325)

       
        # INSIDE RIGHT BOX
        data_table.heading("id",text="ID")
        data_table.heading("name",text="Name")
        data_table.heading("semester",text="Semester")
        data_table.heading("department",text="Department")
        data_table['show']="headings"
        data_table.column("id",width = 10)
        data_table.column("name",width=200)
        data_table.column("semester",width=30)
        data_table.column("department",width=30)
        data_table.pack(fill=BOTH,expand=1)
        data_table.bind("<ButtonRelease-1>",getdata)
        # show()
        search()
    def draw_edit_notice_board():
        def search():
            option = dropdown.get()
            search_input = searchInput.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            if search_input == "":
                mycursor.execute("SELECT * FROM notice_board")
            elif option == "UID":
                mycursor.execute("SELECT * FROM notice_board WHERE id = '" + str(search_input) + "'")
            elif option == "Topic":
                mycursor.execute("SELECT * FROM notice_board WHERE topic = '" + str(search_input).upper() + "'")
            else:
                return
            rows = mycursor.fetchall()
            data_table.delete(*data_table.get_children())
            if rows == None:
                note_text['text'] = "Data: 0 Rows"
                return 
            note_text['text'] = "Data: "+str(len(rows))+" Rows"
            for row in rows:
                data_table.insert('', END, values=row)
            db.commit()
            db.close()
            # pass


        # IT WILL SHOW VALUE FROM DATABASE
        def show():
            id = IdEntry.get()
            nam = TopicEntry.get()
            desig = DescriptionEntry.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            mycursor.execute("select * from notice_board")
            rows = mycursor.fetchall()
            if len(rows) != 0:
                data_table.delete(*data_table.get_children())
            for row in rows:
                data_table.insert('', END, values=row)
            db.commit()
            db.close()

        # IT WILL GET DATA IN LEFTBOX (getdata made events there and fecth value there also)
        def getdata(event):
            currow = data_table.focus()
            contents = data_table.item(currow)
            row = contents['values']
            updatebt.configure(state = "normal")
            deletebt.configure(state = "normal")
            IdEntry.configure(state='normal')
            IdEntry.delete(0, END)
            TopicEntry.delete(0, END)
            DescriptionEntry.delete("1.0", "end")
            IdEntry.insert(0, row[0])
            IdEntry.configure(state='readonly')
            TopicEntry.insert(0, row[1])
            DescriptionEntry.insert(END, row[2])
            addbt.configure(state = 'disabled')

        # IT WILL ADD DATAS
        def add():
            if IdEntry.get()=="" or TopicEntry.get()=="" or DescriptionEntry.get(1.0, "end-1c")=="":
               messagebox.showerror("Error","All fields are required")
            else:
                iD=IdEntry.get()
                name=TopicEntry.get()
                desg=DescriptionEntry.get(1.0, "end-1c")
                db=mysql.connector.connect(host="localhost",user="root",password="",database="KBP")
                mycursor=db.cursor()
                print(desg)
                #desg = db.converter.escape(desg)
                try:
                   mycursor.execute("INSERT INTO notice_board (id, topic, description) VALUES ('"+str(iD)+"', '"+str(name).upper()+"', '"+str(desg)+"')")
                   db.commit()
                   messagebox.showinfo("information","Record Inserted successfully")
                   search()
                   clear()
                except EXCEPTION as e:
                   print(e)
                   db.rollback()
                   db.close()

        def update():
            iD = IdEntry.get()
            name = TopicEntry.get()
            desg = DescriptionEntry.get(1.0, "end-1c")
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            desg = db.converter.escape(desg)
            mycursor.execute("UPDATE notice_board SET topic = '"+str(name).upper()+"', description = '"+str(desg)+"' WHERE id = '"+str(iD)+"'")
            db.commit()
            messagebox.showinfo("information", "Record Updated successfully")
            IdEntry.delete(0, END)
            TopicEntry.delete(0, END)
            DescriptionEntry.delete("1.0", "end")
            search()
            clear()

        def delete1():
            iD = IdEntry.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            sql = "DELETE FROM notice_board WHERE id='"+str(iD)+"'"
            mycursor.execute(sql)
            db.commit()
            messagebox.showinfo("information", "Record Deleted successfully")
            IdEntry.delete(0, END)
            TopicEntry.delete(0, END)
            DescriptionEntry.delete("1.0", "end")
            search()
            clear()


        # IT WILL CLEAR DATAS
        def clear():
            updatebt.configure(state = "disabled")
            deletebt.configure(state = "disabled")
            IdEntry.configure(state='normal')
            IdEntry.delete(0, END)
            IdEntry.insert(0,random_string())
            TopicEntry.delete(0, END)
            DescriptionEntry.delete("1.0", "end")
            TopicEntry.focus_set()
            addbt.configure(state='normal')
        def random_string():
            count = 1
            S = 5
            while(count!=0):
                ran = ''.join(random.choices(string.ascii_letters + string.digits, k = S))
                db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
                mycursor = db.cursor()
                mycursor.execute("select count(id) from notice_board where id = '"+str(ran)+"'")
                rows = mycursor.fetchone()
                count = rows[0]
            return ran
        label=Frame(footer,bd=0,bg="brown")
        label.place(x=0,y=0,width=1080,height=85)
        abcframe=Frame(footer,bd=0,bg="black")
        abcframe.place(x=90,y=15,width=900,height=1)
        ILabel=Label(label,text="Here You Can Edit Or View Notice Board database",font=("Helvetica",20),fg="#eae2b7",bg="brown")
        ILabel.place(x=250, y=30)
        leftbox=Frame(dashboard,bd=0,bg="brown")
        leftbox.place(x=0,y=50,width=550,height=350)

        # INSIDE LEFT BOX
        leftbox_title=Label(leftbox,text="Manage Database",font=("Helvetica",20,"bold"),fg="#eae2b7",bg="brown")
        leftbox_title.place(x=50, y=10, width=  500)
        IdLabel=Label(leftbox,text="ID",font=("Helvetica",15),fg="#eae2b7",bg="brown")
        IdLabel.place(x=50, y =50)
        IdEntry=Entry(leftbox,font=("Helvetica",15),bd=0)
        IdEntry.insert(0,random_string())
        IdEntry.place(x=100, y =50, width = 80)
        TopicLabel=Label(leftbox,text="Topic",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
        TopicLabel.place(x=250, y=50)
        TopicEntry=Entry(leftbox,font=("Helvetica", 15),bd=0)
        TopicEntry.place(x=320, y=50, width = 200)
        DescriptionLabel=Label(leftbox,text="Description",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
        DescriptionLabel.place(x=50, y=80)
        scrolly=Scrollbar(leftbox,orient=VERTICAL)
        DescriptionEntry=Text(leftbox, font=("Helvetica", 15),bd=0, yscrollcommand=scrolly.set)
        scrolly.config(command=DescriptionEntry.yview)
        DescriptionEntry.place(x=50, y=110, width = 450, height = 170)
        scrolly.place(x=510, y=110, height = 170)


        # LEFT BOX BUTTONS
        btnfrm=Frame(leftbox, bd=0, bg="brown")
        btnfrm.place(x=0,y=300,width=500,height=50)

        addbt=Button(btnfrm,text="Add",font=("Helvetica", 12),bg="indianred",fg="white",bd=0,command=add)
        addbt.place(x=50, y=0, width = 70)
        updatebt=Button(btnfrm,text="Edit",font=("Helvetica", 12),bg="indianred",fg="white",bd=0,command=update)
        updatebt.configure(state = "disabled")
        updatebt.place(x=150, y=0, width = 70)
        deletebt=Button(btnfrm,text="Delete",font=("Helvetica", 12),bg="indianred",fg="white",command=delete1, bd =0)
        deletebt.configure(state = "disabled")
        deletebt.place(x=250, y=0, width = 70)
        clrbt=Button(btnfrm,text="Clear",font=("Helvetica", 12),bg="indianred",fg="white",command=clear, bd = 0)
        clrbt.place(x=350, y=0, width = 70)






        # RIGHT BOX
        rightbox=Frame(dashboard,bd=0,bg="indianred")
        rightbox.place(x=550,y=50,width=600,height=350)

        # RIGHT BOX HEADING
        searchInput=Entry(rightbox,font=("Helvetica", 12),bd=0,width=17)
        searchInput.place(x=10, y=10, height = 30)
        dropdown=ttk.Combobox(rightbox,font=("Helvetica",10),state='readonly', width = 10)
        dropdown['values']=("--Search By--", "UID", "Topic")
        dropdown.current(0)
        dropdown.place(x=180, y=10, height = 30)
        searchBtn=Button(rightbox,text="Search",command=search,font=("Helvetica", 12),width=10, bd = 0)
        searchBtn.place(x=280, y=10, height = 30)

        # BOX INSIDE RIGHT BOX
        tabfrm=Frame(rightbox,bd=4,relief=RIDGE,bg="lightblue")
        tabfrm.place(x=10,y=50,width=510,height=270)
        scrolly=Scrollbar(tabfrm,orient=VERTICAL)
        data_table=ttk.Treeview(tabfrm,columns=("id","name","description"),yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=data_table.yview)

        note_text=Label(rightbox,font=("Helvetica", 10),bg="indianred",fg="white")
        note_text.place(x=10, y=325)

        # INSIDE RIGHT BOX
        data_table.heading("id",text="ID")
        data_table.heading("name",text="Topic")
        data_table.heading("description",text="Description")
        data_table['show']="headings"
        data_table.column("id",width = 10)
        data_table.column("name",width=50)
        data_table.column("description",width=30)
        data_table.pack(fill=BOTH,expand=1)
        data_table.bind("<ButtonRelease-1>",getdata)
        search()
    
    def draw_execute_dbms():
        def execute_query():
            query_input = queryInput.get(1.0, "end-1c")
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor(buffered = True)
            try:
                mycursor.execute(query_input)
                db.commit()
            except:
                messagebox.showerror("Alert", "An error occured, check your query")
                db.rollback()
                db.close()
                return
            rows = mycursor.fetchall()
            for widget in bottom_panel.winfo_children():
                widget.destroy()
            label1 = Label(bottom_panel, text =">>> "+ str(mycursor.rowcount)+" Rows Affected / Selected", bg = "#333", fg = "#00FF00", font = ("Lucida Console", 12))
            label1.place(x=10, y=0, height = 40, width = 300)
            if rows == None:
                return
            for widget in top_panel.winfo_children():
                widget.destroy()
            num_fields = len(mycursor.description)
            field_names = [i[0] for i in mycursor.description]
            a = list(field_names)
            scrollx=Scrollbar(top_panel,orient=HORIZONTAL)
            data_table=ttk.Treeview(top_panel, columns=a, show="headings", xscrollcommand=scrollx.set)
            scrollx.place(x=10, y=180, width = 880)
            scrollx.config(command=data_table.xview)
            data_table.place(x=10, y=0, width = 880, height = 180)
            for i in a:
                data_table.heading(column = i, text = i.upper())
                data_table.column(column = i, width = 200)
            for row in rows:
                data_table.insert('', END, values=row)
        label=Frame(footer,bd=0,bg="brown")
        label.place(x=0,y=0,width=1080,height=85)
        abcframe=Frame(footer,bd=0,bg="black")
        abcframe.place(x=90,y=15,width=900,height=1)
        ILabel=Label(label,text="Here You Can Execute Database Query's",font=("Helvetica",20),fg="#eae2b7",bg="brown")
        ILabel.place(x=300, y =30)

        #Header
        #panel
        panel=Frame(dashboard, bg="brown", bd=0)
        panel.place(x=0,y=50,width=1080,height=375)
        #panel_elements
        searchBy=Label(panel,text="Enter Query",font=("Helvetica",15, "bold"),bg="brown",fg="#222")
        searchBy.place(x=10, y=5)
        scrollx=Scrollbar(panel,orient=HORIZONTAL)
        queryInput=Text(panel, wrap=NONE, font=("Lucida Console", 15),bd=0, xscrollcommand=scrollx.set)
        scrollx.config(command=queryInput.xview)
        scrollx.place(x=15, y=70, width = 1050, height = 12)
        queryInput.place(x=15, y=40, height = 30, width = 1050)
        queryBtn=Button(panel,text="Execute", command = execute_query, font=("Helvetica",18,"bold"), bd = 0)
        queryBtn.place(x=960, y=5, height = 30)

        top_panel=Frame(panel, bg="indianred", bd=0)
        top_panel.place(x=0,y=85,width=1080,height=300)
        

          
    def draw_edit_company_list():
        def search():
            option = dropdown.get()
            search_input = searchInput.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            if search_input == "":
                mycursor.execute("SELECT * FROM company_list")
            elif option == "Name":
                mycursor.execute("SELECT * FROM company_list WHERE name = '" + str(search_input).upper() + "'")
            elif option == "Year":
                mycursor.execute("SELECT * FROM company_list WHERE year LIKE '%" + str(search_input).upper() + "%'")
            elif option == "Department":
                mycursor.execute("SELECT * FROM company_list WHERE dept lIKE '%" + str(search_input).upper() + "%'")
            else:
                return
            rows = mycursor.fetchall()
            data_table.delete(*data_table.get_children())
            if rows == None:
                note_text['text'] = "Data: 0 Rows"
                return 
            note_text['text'] = "Data: "+str(len(rows))+" Rows"
            for row in rows:
                data_table.insert('', END, values=row)
            db.commit()
            db.close()
            # pass


        # IT WILL GET DATA IN LEFTBOX (getdata made events there and fecth value there also)
        def getdata(event):
            currow = data_table.focus()
            contents = data_table.item(currow)
            row = contents['values']
            updatebt.configure(state = "normal")
            deletebt.configure(state = "normal")
            NameEntry.configure(state='normal')
            NameEntry.delete(0, END)
            YearEntry.delete("1.0", "end")
            DepartmentEntry.delete("1.0", "end")
            NameEntry.insert(0, row[0])
            NameEntry.configure(state='readonly')
            YearEntry.insert(END, row[2])
            DepartmentEntry.insert(END, row[1])
            addbt.configure(state = 'disabled')

        # IT WILL ADD DATAS
        def add():
            if NameEntry.get()=="" or YearEntry.get(1.0, "end-1c")=="" or DepartmentEntry.get(1.0, "end-1c")=="":
               messagebox.showerror("Error","All fields are required")
            else:
                name=NameEntry.get()
                year=YearEntry.get(1.0, "end-1c")
                dept=DepartmentEntry.get(1.0, "end-1c")
                db=mysql.connector.connect(host="localhost",user="root",password="",database="KBP")
                mycursor=db.cursor()
                try:
                   mycursor.execute("INSERT INTO company_list (name, year, dept) VALUES ('"+str(name).upper()+"', '"+str(year).upper()+"', '"+str(dept).upper()+"')")
                   db.commit()
                   messagebox.showinfo("Information","Record Inserted successfully")
                   search()
                   clear()
                except EXCEPTION as e:
                   print(e)
                   db.rollback()
                   db.close()

        def update():
            name = NameEntry.get()
            year = YearEntry.get(1.0, "end-1c")
            dept = DepartmentEntry.get(1.0, "end-1c")
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            # dept = db.converter.escape(dept)
            mycursor.execute("UPDATE company_list SET year = '"+str(year).upper()+"', dept = '"+str(dept).upper()+"' WHERE name = '"+str(name).upper()+"'")
            db.commit()
            messagebox.showinfo("information", "Record Updated successfully")
            NameEntry.delete(0, END)
            YearEntry.delete("1.0", "end")
            DepartmentEntry.delete("1.0", "end")
            search()
            clear()

        def delete1():
            name = NameEntry.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            sql = "DELETE FROM company_list WHERE name='"+str(name).upper()+"'"
            mycursor.execute(sql)
            db.commit()
            messagebox.showinfo("information", "Record Deleted successfully")
            NameEntry.delete(0, END)
            YearEntry.delete("1.0", "end")
            DepartmentEntry.delete("1.0", "end")
            search()
            clear()


        # IT WILL CLEAR DATAS
        def clear():
            updatebt.configure(state = "disabled")
            deletebt.configure(state = "disabled")
            NameEntry.configure(state='normal')
            NameEntry.delete(0, END)
            YearEntry.delete("1.0", "end")
            DepartmentEntry.delete("1.0", "end")
            addbt.configure(state='normal')
            
        label=Frame(footer,bd=0,bg="brown")
        label.place(x=0,y=0,width=1080,height=85)
        abcframe=Frame(footer,bd=0,bg="black")
        abcframe.place(x=90,y=15,width=900,height=1)
        ILabel=Label(label,text="Here You Can Edit Or View Company database",font=("Helvetica",20),fg="#eae2b7",bg="brown")
        ILabel.place(x=250, y =30)
       
        # LEFT BOX
        leftbox=Frame(dashboard,bd=0,bg="brown")
        leftbox.place(x=0,y=50,width=600,height=350)

        # INSIDE LEFT BOX
        leftbox_title=Label(leftbox,text="Manage Database",font=("Helvetica",20,"bold"),fg="#eae2b7",bg="brown")
        leftbox_title.place(x=10, y=30, width=  500)
        NameLabel=Label(leftbox,text="Company Name",font=("Helvetica",15),fg="#eae2b7",bg="brown")
        NameLabel.place(x=10, y =90)
        NameEntry=Entry(leftbox,font=("Helvetica",15),bd=0)
        NameEntry.place(x=160, y =90, width = 317)
        YearLabel=Label(leftbox,text="Year",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
        YearLabel.place(x=10, y=120)
        scrolly=Scrollbar(leftbox,orient=VERTICAL)
        YearEntry=Text(leftbox, font=("Helvetica", 15),bd=0, yscrollcommand=scrolly.set)
        scrolly.config(command=YearEntry.yview)
        YearEntry.place(x=160, y=120, width = 300, height = 70)
        scrolly.place(x=460, y=120, height = 70)
        DepartmentLabel=Label(leftbox,text="Department",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
        DepartmentLabel.place(x=10, y=190)
        scrolly=Scrollbar(leftbox,orient=VERTICAL)
        DepartmentEntry=Text(leftbox, font=("Helvetica", 15),bd=0, yscrollcommand=scrolly.set)
        # DescriptionEntry['text'] = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
        scrolly.config(command=DepartmentEntry.yview)
        DepartmentEntry.place(x=160, y=195, width = 300, height = 70)
        scrolly.place(x=460, y=195, height = 70)


        # LEFT BOX BUTTONS
        btnfrm=Frame(leftbox, bd=0, bg="brown")
        btnfrm.place(x=0,y=300,width=500,height=50)

        addbt=Button(btnfrm,text="Add",font=("Helvetica", 12),bg="indianred",fg="white",bd=0,command=add)
        addbt.place(x=50, y=0, width = 70)
        updatebt=Button(btnfrm,text="Edit",font=("Helvetica", 12),bg="indianred",fg="white",bd=0,command=update)
        updatebt.configure(state = "disabled")
        updatebt.place(x=150, y=0, width = 70)
        deletebt=Button(btnfrm,text="Delete",font=("Helvetica", 12),bg="indianred",fg="white",command=delete1, bd =0)
        deletebt.configure(state = "disabled")
        deletebt.place(x=250, y=0, width = 70)
        clrbt=Button(btnfrm,text="Clear",font=("Helvetica", 12),bg="indianred",fg="white",command=clear, bd = 0)
        clrbt.place(x=350, y=0, width = 70)






        # RIGHT BOX
        rightbox=Frame(dashboard,bd=0,bg="indianred")
        rightbox.place(x=500,y=50,width=600,height=350)

        # RIGHT BOX HEADING
        searchInput=Entry(rightbox,font=("Helvetica", 12),bd=0,width=17)
        searchInput.place(x=10, y=10, height = 30)
        dropdown=ttk.Combobox(rightbox,font=("Helvetica",10),state='readonly', width = 10)
        dropdown['values']=("--Search By--", "Name", "Year", "Department")
        dropdown.current(0)
        dropdown.place(x=180, y=10, height = 30)
        searchBtn=Button(rightbox,text="Search",command=search,font=("Helvetica", 12),width=10, bd = 0)
        searchBtn.place(x=280, y=10, height = 30)

        # BOX INSIDE RIGHT BOX
        tabfrm=Frame(rightbox,bd=4,relief=RIDGE,bg="lightblue")
        tabfrm.place(x=10,y=50,width=550,height=270)
        scrolly=Scrollbar(tabfrm,orient=VERTICAL)
        data_table=ttk.Treeview(tabfrm,columns=("name","department", "year"),yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=data_table.yview)

        note_text=Label(rightbox,font=("Helvetica", 10),bg="indianred",fg="white")
        note_text.place(x=10, y=325)

        # INSIDE RIGHT BOX
        data_table.heading("name",text="Name")
        data_table.heading("year",text="Year")
        data_table.heading("department",text="Department")
        data_table['show']="headings"
        data_table.column("name",width = 10)
        data_table.column("year",width=50)
        data_table.column("department",width=30)
        data_table.pack(fill=BOTH,expand=1)
        data_table.bind("<ButtonRelease-1>",getdata)
        search()
        

        
    for widget in footer.winfo_children():
        widget.destroy()
    for widget in dashboard.winfo_children():
        widget.destroy()
    footer1=Frame(footer, bg="brown", bd=0)
    footer1.place(x=0,y=565,width=1080,height=85)
    welcome_text["text"] = "Welcome, Admin"
    image1 = Image.open("media/kbp.jpg")
    im1 = image1.filter(ImageFilter.BLUR)
    test = ImageTk.PhotoImage(im1)
    label1 = Label(dashboard,image=test)
    label1.photo = test
    label1.place(x=0, y=0, height = 400, width = 1080)
    option= Button(dashboard, text ="View/Edit Employee", command=draw_edit_employee, bd =0, font=("Helvetica",11),fg='#0097e8',activeforeground='#0097e8')
    option.place(x=0, y=0, width = 200, height = 50)
    
    option= Button(dashboard, text ="View/Edit Student", command=draw_edit_student, bd =0, font=("Helvetica",11),fg='#0097e8',activeforeground='#0097e8')
    option.place(x=166, y=0, width = 200, height = 50)
   
    option= Button(dashboard, text ="Change Password", command=draw_change_password, bd =0, font=("Helvetica",11),fg='#0097e8',activeforeground='#0097e8')
    option.place(x=332, y=0, width = 200, height = 50)
 
    option= Button(dashboard, text ="View/Edit Notice Board", command=draw_edit_notice_board, bd =0, font=("Helvetica",11),fg='#0097e8',activeforeground='#0097e8')
    option.place(x=510, y=0, width = 200, height = 50)
   
    option= Button(dashboard, text ="Execute DBMS Query", command=draw_execute_dbms, bd =0, font=("Helvetica",11),fg='#0097e8',activeforeground='#0097e8')
    option.place(x=690, y=0, width = 200, height = 50)
    
    option= Button(dashboard, text ="View/Edit Company List", command=draw_edit_company_list,bd =0, font=("Helvetica",11),fg='#0097e8',activeforeground='#0097e8')
    option.place(x=880, y=0, width = 200, height = 50)
   



    
def on_closing():
    global is_on
    if is_admin:
        on_.config(image=off)
        is_on = False
    else:
        on_.config(image=on)
        is_on = True
    window.destroy()

def admin():
    
    for widget in dashboard.winfo_children():
        widget.destroy()
    for widget in footer.winfo_children():
        widget.destroy()
    

    def DetectFace():
        df = pd.read_csv('admin Profile.csv')
        df.sort_values('Ids', inplace = True)
        df.drop_duplicates(subset = 'Ids', keep = 'first', inplace = True)
        df.to_csv('admin Profile.csv', index = False)
        Name=user.get() 
        ID_Number= code.get()
        #print(OTP1)
        name , Id = '',''
        dic = {
            'Name' : Name,
            'Ids' : ID_Number
        }
        def store_data():
            global name,Id,dic
            name = Name
                   
            Id  = ID_Number
                   
            dic = {
                'Ids' : ID_Number,
                'Name': Name
            }
            c = dic
            return  c
        reader = csv.DictReader(open('admin Profile.csv'))
        print('Detecting Login Face')
        for rows in reader:
            result = dict(rows)
            a=int(result['Ids'])
            if a <100:
                name1 = result['Name']
                

            
        
        recognizer = cv2.face.LBPHFaceRecognizer_create()  #cv2.createLBPHFaceRecognizer()
        recognizer.read("TrainData\Trainner.yml")
        harcascadePath = 'C:\\Users\\vaibh\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml '
        faceCascade = cv2.CascadeClassifier(harcascadePath);
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        Face_Id = ''
        name2 = ''

        # Camera ON Everytime
        while True:
            ret, frame = cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.3, 5)
            Face_Id = 'Not detected'

            # Drawing a rectagle around the face 
            for (x, y, w, h) in faces:
                Face_Id = 'Not detected'
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
                if (confidence < 90):
                    if (Id <100):
                        name = name1
                    Predicted_name = str(name)
                    Face_Id = Predicted_name
                    print(name)
                    
                else:
                    Predicted_name = 'Unknown'
                    Face_Id = Predicted_name
                    # Here unknown faces detected will be stored
                    noOfFile = len(os.listdir("UnknownFaces")) + 1
                    if int(noOfFile) < 100:
                        cv2.imwrite("UnknownFaces\Image" + str(noOfFile) + ".jpg", frame[y:y + h, x:x + w])
                    
                    else:
                        pass


                cv2.putText(frame, str(Predicted_name), (x, y + h), font, 1, (255, 255, 255), 2)
                
            cv2.imshow('Picture', frame)
            #print(Face_Id)
            cv2.waitKey(1)

            # Checking if the face matches for Login
            if Face_Id == name1 or name2 and Face_Id != 'Unknown' :
                mydate = datetime.datetime.now()
                
                date = datetime.datetime.strftime(mydate, '%d, %m, %Y')
                time = datetime.datetime.strftime(mydate, '%H, %M, %S')
                d={'Name':Face_Id,'Ids':Id,'Date':date,'Time':time}
                with open('admin attendance.csv','a+') as f:
                    fields = ['Name','Ids','Date','Time']   
                    writer=csv.DictWriter(f,fieldnames=fields)

                    writer.writerow(d)
                messagebox.showinfo("LOGIN","login succesfull!!" )
                cv2.destroyAllWindows()
                draw_admin()
                
                
                break
                
            elif Face_Id == 'Not detected':
                print("-----Face Not Detected, Try again------")
                pass
            else:
                print('-----------Login failed please try agian-------')
            
            
            if (cv2.waitKey(1) == ord('q')):
               break
            
            
        def DetectFace():
            root.destroy()
       


    def signin():
        Name=user.get()
        ID_Number=code.get()
        name , Id = '',''
        dic = {
            'Name' : Name,
            'Ids' : ID_Number
        }
        def store_data(signin):
            global name,Id,dic
            name = Name
           
            Id  = ID_Number
           
            dic = {
                'Ids' : ID_Number,
                'Name': Name
            }
            c = dic
            return  c
        db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
        mycursor=db.cursor()
        command="select *from register where Name=%s and ID_Number=%s"
        if Name == "" and ID_Number == "":
            print(1)
            messagebox.showinfo("Invalid","Both The Fields Are Empty!!" )
        elif Name == "" or ID_Number == " ":
               messagebox.showinfo("Invalid","Any Field Is Empty Please Filed It!!" )
        else:
            print(ID_Number)
            query = "SELECT * FROM register WHERE Name = %(name)s AND ID_Number = %(id_number)s"
            params = {'name': Name, 'id_number': ID_Number}
            mycursor.execute(query, params)
 
        print(params)    
        result=mycursor.fetchall()
        print(result)
        
        if result=="":
            print(3)
            messagebox.showinfo("Invalid","Invalid username or password!!" )
        else :
            if result:
    
                for row in result:
                     name, id_number, other_column1, other_column2 = row
                     print(f"Name: {name}, ID_Number: {id_number}, Other_Column1: {other_column1}, Other_Column2: {other_column2}")
                print(4)
                mydate = datetime.datetime.now()  
                date = datetime.datetime.strftime(mydate, '%d, %m, %Y')
                time = datetime.datetime.strftime(mydate, '%H, %M, %S')
                d={'Name':Name,'Ids':ID_Number,'Date':date,'Time':time}
                with open('admin attendance.csv','a+') as f:
                    fields = ['Name','Ids','Date','Time']
                    writer=csv.DictWriter(f,fieldnames=fields)
                    writer.writerow(d)
                messagebox.showinfo("LOGIN","login succesfull!!" )
                draw_admin()
                print(5) 
            else:
                 messagebox.showinfo("Invalid","No matching records found.")
        def signin():
            root.destroy()
       

            
    ###########________________________________________sign up code
    def signup_command():
       # window = Toplevel()
       # window.title("SignUp")
       # window.geometry('925x600+300+200')
       # window.config(bg='#fff')
      #  window.resizable(False,False)
    
        for widget in dashboard.winfo_children():
            widget.destroy()
        def signup():
            Name=user.get() 
            Mobile_Number=code.get()
            Emailid=conform_code.get()
            ID_Number=email.get()
            #print(OTP1)
            name , Id = '',''
            dic = {
                'Name' : Name,
                'Ids' : ID_Number
            }
            def store_data():
                global name,Id,dic
                name = Name
                   
                Id  = ID_Number
                   
                dic = {
                    'Ids' : ID_Number,
                    'Name': Name
                }
                c = dic
                return  c
            x=len(Mobile_Number)
            if Name=="" or Mobile_Number=="" or Emailid=="" or ID_Number=="":
                messagebox.showinfo("Insert Status","All Fileds are required")
                
            elif (x!=10):
                Label(frame,width=39,pady=7,text='*Invalid Number',bg='white',fg='Red',border=0).place(x=130,y=250)
            else:
                db=mysql.connector.connect(host="localhost",user="root",password="",database="KBP")
                mycursor=db.cursor()
                mycursor.execute("INSERT INTO register (Name,ID_Number,Mobile_Number,Emailid) VALUES ('"+str(Name)+"', '"+str(ID_Number).upper()+"', '"+str(Mobile_Number).upper()+"', '"+str(Emailid).upper()+"')")
                db.commit()
                
                db.close();
                def getImagesAndLabels(path):
                    # Get the path of all the files in the folder
                    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

                    # Create empth face list
                    faces = []
                    # Create empty ID list
                    Ids = []
                    # Looping through all the image paths and loading the Ids and the images
                    for imagePath in imagePaths:
                        # Loading the image and converting it to gray scale
                        pilImage = Image.open(imagePath).convert('L')
                        # Now we are converting the PIL image into numpy array
                        imageNp = np.array(pilImage, 'uint8')
                        # getting the Id from the image
                        Id = int(os.path.split(imagePath)[-1].split(".")[1])
                        # extract the face from the training image sample
                        faces.append(imageNp)
                        
                        Ids.append(Id)
                    return faces, Ids

                # Train image using LBPHFFace recognizer 
                recognizer = cv2.face.LBPHFaceRecognizer_create()  # recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
                harcascadePath = 'C:\\Users\\vaibh\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml '
                detector = cv2.CascadeClassifier(harcascadePath)
                faces , Id= getImagesAndLabels("C:\\Users\\vaibh\\Desktop\\College-Management-System-using-Python-and-Tkinter-main\\College-Management-System-using-Python-and-Tkinter-main\\TrainingImage")
                recognizer.train(faces, np.array(Id))
                #store data in file 
                recognizer.save("TrainData\Trainner.yml")
                res = "Image Trained and data stored in TrainData\Trainner.yml "

                print(res)
                messagebox.showinfo("Registration","Registered Successfully")

           
        def TakeImages():
            Name=user.get() 
            ID_Number=email.get()
            Mobile_Number=code.get()
            Emailid=conform_code.get()
            
            #print(OTP1)
            name , Id,mobileno,emailid = '','','',''
            dic = {
                'Name' : Name,
                'Ids' : ID_Number,
                'Mobile Number':Mobile_Number,
                'Email-Id':Emailid
            }
            def store_data():
                global name,Id,dic
                name = Name
                mobileno = Mobile_Number
                emailid = Emailid
                Id  = ID_Number
                   
                dic = {
                    'Ids' : ID_Number,
                    'Name': Name,
                    'Mobile Number':Mobile_Number,
                    'Email-Id':Emailid
                }
                c = dic
                return  c
            dict1 = store_data()
            print(dict1)        
            if (Name.isalpha()):
                if Id == '1':
                    fieldnames = ['Name','Ids','Mobile Number','Email-Id']
                    with open('admin Profile.csv','w') as f:
                        writer = csv.DictWriter(f, fieldnames =fieldnames)
                        writer.writerow(dict1)
                else:
                    fieldnames = ['Name','Ids','Mobile Number','Email-Id']
                    with open('admin Profile.csv','a') as f:
                        writer = csv.DictWriter(f, fieldnames =fieldnames)
                        writer.writerow(dict1)
                cam = cv2.VideoCapture(0)

                #Haarcascade file for detctionof face
                harcascadePath = 'C:\\Users\\vaibh\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml '
                detector = cv2.CascadeClassifier(harcascadePath)
                sampleNum = 0
                while (True):
                    ret, img = cam.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = detector.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                        # Incrementing sample number
                        sampleNum = sampleNum + 1
                        # Saving the captured face in the dataset folder TrainingImage
                        cv2.imwrite("TrainingImage\ " + Name + "." + ID_Number + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                        # display the frame
                    cv2.imshow('Cpaturing Face for Login ', img)
                
                    # wait for 100 miliseconds
                    if cv2.waitKey(100) & 0xFF == ord('q'):
                        break
                    # break if the sample number is morethan 60
                    elif sampleNum > 1:
                        break
                    
                
                cam.release()
                cv2.destroyAllWindows()
                res = "Images Saved for Name : " + name + " with ID  " + Id
                print(res)
                print(' Images save location is TrainingImage\ ')
              
                
            else:
                if(name.isalpha()):
                    print('Enter Proper Id')
                else:
                    print('Enter Proper Id and Name')

        img=PhotoImage(file='E:\\Project\\sign.png')
        Label(dashboard,image=img,border=0,bg='white').place(x=125,y=90)
        
        frame=Frame(dashboard,width=350,height=500,bg='#fff')
        frame.place(x=600,y=0)

        heading=Label(frame,text='Sign Up',fg="#57a1f8",bg='white',font=('Microsoft Yahei UI Light',23,'bold'))
        heading.place(x=100,y=5)
        #username Column______________________________________________________________
        def on_enter(e):
            user.delete(0,'end')
        def on_leave(e):
            if user.get()=='':
                user.insert(0,'Name')

                    
        user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        user.place(x=30,y=80)
        user.insert(0,'Name')
        user.bind("<FocusIn>",on_enter)
        user.bind("<FocusOut>",on_leave)

        Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)
            #Id Number______________________________________________________________
        def otp():
            def verify():
                print(OTP1)
                
                b=otp1.get()
                print(b)
                if(OTP1==b):
                    Label(frame,text='Email verified',fg="red",bg='white',font=('Microsoft Yahei UI Light',7,'bold')).place(x=250,y=380)
                 
                else:
                  
                    heading=Label(frame,text='Invalid OTP',fg="red",bg='white',font=('Microsoft Yahei UI Light',7,'bold')).place(x=250,y=380)
                    
                 
            OTP1=str(random.randint(1000,9999))
            print(OTP1)
            s=smtplib.SMTP_SSL("smtp.gmail.com",465)
            s.login('vaibhavvpatill@gmail.com',"gnssmfzqnbdssmzq")
            send_to=conform_code.get()
            print(send_to)
            s.sendmail('vaibhavvpatill@gmail.com',send_to,OTP1)
            def on_enter(e):
                otp1.delete(0,'end')
            def on_leave(e):
                if otp1.get()=='':
                    otp1.insert(0,'Enter OTP')
                     
            otp1=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
            otp1.place(x=30,y=340)
            otp1.insert(0,'Enter OTP')
            otp1.bind("<FocusIn>",on_enter)
            otp1.bind("<FocusOut>",on_leave)
            Frame(frame,width=295,height=2,bg='black').place(x=25,y=370)
          
            Button(frame,width=9,pady=5,text='Submit',bg='#57a1f8',fg='white',border=0,command=verify).place(x=250,y=335)
            
            
         
        def on_enter(e):
            conform_code.delete(0,'end')
        def on_leave(e):
            if conform_code.get()=='':
                conform_code.insert(0,'Email-ID')

                    
        conform_code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        conform_code.place(x=30,y=290)
        conform_code.insert(0,'Email-ID')
        conform_code.bind("<FocusIn>",on_enter)
        conform_code.bind("<FocusOut>",on_leave)

        Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)
        Button(frame,width=9,pady=5,text='Send Otp',bg='#57a1f8',fg='white',border=0,command=otp).place(x=250,y=285)

            #Mobile No.______________________________________________________________
        def on_enter(e):
            code.delete(0,'end')
        def on_leave(e):
            if code.get()=='':
                code.insert(0,'Mobile Number')

                    
        code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        code.place(x=30,y=220)
        code.insert(0,'Mobile Number')
        code.bind("<FocusIn>",on_enter)
        code.bind("<FocusOut>",on_leave)
       

        Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

        #Email iD______________________________________________________________

        def on_enter(e):
            email.delete(0,'end')
        def on_leave(e):
            if email.get()=='':
                email.insert(0,'ID Number')

                    
        email=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        email.place(x=30,y=150)
        email.insert(0,'ID Number')
        email.bind("<FocusIn>",on_enter)
        email.bind("<FocusOut>",on_leave)

        Frame(frame,width=295,height=2,bg='black').place(x=25,y=317)

            #signup button___________________________________
        for widget in footer.winfo_children():
            widget.destroy()
        a1frame=Frame(footer,bg='white')
        a1frame.place(x=0,y=0,width=1080,height=85)
        Button(a1frame,width=39,pady=5,text='Take Face ID',bg='#57a1f8',fg='white',border=0,command=TakeImages).place(x=635,y=0)
        Button(a1frame,width=125,pady=7,text='Sign up',bg='#57a1f8',fg='white',border=0,command=signup).place(x=100,y=35)
        Label(frame,width=39,pady=7,text='*Please Insert A Integer',bg='white',fg='Red',border=0).place(x=120,y=180)

        dashboard.mainloop()
        

    ##############__________________________________


    img=PhotoImage(file='E:\\Project\\login.png')
    Label(dashboard,image=img,bg='white').place(x=125,y=50)
        
    
    frame=Frame(dashboard,width=350,height=350,bg='white')
    frame.place(x=600,y=70)

    heading=Label(frame,text='Sign in',fg='#57a1f8',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
    heading.place(x=100,y=5)

    #username_____________________________
    def on_enter(e):
        user.delete(0,'end')

    def on_leave(e):
        name=user.get()
        if name=='':
            user.insert(0,'Username')

            
    user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
    user.place(x=30,y=80)
    user.insert(0,'Username')
    user.bind('<FocusIn>',on_enter)
    user.bind('<FocusOut>',on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)
    #password_____________________________
    def on_enter(e):
        code.delete(0,'end')

    def on_leave(e):
        name=code.get()
        if name=='':
            code.insert(0,'ID_Number')
    code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
    code.place(x=30,y=150)
    code.insert(0,'ID_Number')
    code.bind('<FocusIn>',on_enter)
    code.bind('<FocusOut>',on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)
    for widget in footer.winfo_children():
        widget.destroy()
    a1frame=Frame(footer,bg='white')
    a1frame.place(x=0,y=0,width=1080,height=85)
    #button___________________________________
    Button(frame,width=39,pady=7,text='Sign in',bg='#57a1f8',fg='white',border=0,command=signin).place(x=35,y=204)
    label=Label(frame,text="Don't have an account ?",fg='black',bg='white',font=('Microsoft Yahei UI Light',9))
    label.place(x=75,y=300)
    Button(frame,width=39,pady=7,text='Login with Face ID',bg='#57a1f8',fg='white',border=0,command=DetectFace).place(x=35,y=250)
    sign_up=Button(frame,width=6,text='Sign up',border=0,bg='white',cursor='hand2',fg='#57a1f8',command=signup_command)
    sign_up.place(x=215,y=300)


    root.mainloop()

def draw_staff():
    def draw_change_password():
        def change_pwd():
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            mycursor.execute("SELECT y FROM global_values WHERE x = 'admin'")
            rows = mycursor.fetchone()
            if rows == None:
                messagebox.showerror("Failure",  "Oops! Something went wrong")
                return
            server_pwd = rows[0]
            db.commit()
            if CurrentPwd.get() == server_pwd:
                if NewPwd.get() == NewPwd2.get():
                    try:
                        mycursor.execute("UPDATE global_values SET y = '"+str(NewPwd.get())+"' WHERE x = 'admin'")
                        db.commit()
                        messagebox.showinfo("Success",  "Password changed")
                    except EXCEPTION as e:
                        messagebox.showerror("Failure",  e)
                        db.rollback()
                        db.close()
                else:
                    messagebox.showerror("Failure",  "New Passwords didn't match")

            else:
                messagebox.showerror("Failure",  "Oops! Something went wrong")
            CurrentPwd.delete(0, END)
            NewPwd.delete(0, END)
            NewPwd2.delete(0, END)
            root_window.destroy()
            

       

        label=Frame(footer,bd=0,bg="brown")
        label.place(x=0,y=0,width=1080,height=85)
        abcframe=Frame(footer,bd=0,bg="black")
        abcframe.place(x=90,y=15,width=900,height=1)
        ILabel=Label(label,text="Here You Can Change Password",font=("Helvetica",20),fg="#eae2b7",bg="brown")
        ILabel.place(x=350, y =30)
        #panel
        panel=Frame(dashboard, bg="#fff", bd=0)
        panel.place(x=0,y=50,width=1080,height=375)
        #panel_elements
        def on_enter(e):
            CurrentPwd.delete(0,'end')
        def on_leave(e):
            if CurrentPwd.get()=='':
                CurrentPwd.insert(0,'Current Password')

                
        CurrentPwd=Entry(panel,width=30,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        CurrentPwd.place(x=600,y=30)
        CurrentPwd.insert(0,'Current Password')
        CurrentPwd.bind("<FocusIn>",on_enter)
        CurrentPwd.bind("<FocusOut>",on_leave)
        Frame(panel,width=300,height=2,bg='black').place(x=600,y=55)
        def on_enter(e):
            NewPwd.delete(0,'end')
        def on_leave(e):
            if NewPwd.get()=='':
                NewPwd.insert(0,'New Password')

                
        NewPwd=Entry(panel,width=30,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        NewPwd.place(x=600,y=100)
        NewPwd.insert(0,'New Password')
        NewPwd.bind("<FocusIn>",on_enter)
        NewPwd.bind("<FocusOut>",on_leave)
        Frame(panel,width=300,height=2,bg='black').place(x=600,y=125)
        def on_enter(e):
            NewPwd2.delete(0,'end')
        def on_leave(e):
            if NewPwd2.get()=='':
                NewPwd2.insert(0,'Confirm Password')

                
        NewPwd2=Entry(panel,width=30,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        NewPwd2.place(x=600,y=180)
        NewPwd2.insert(0,'Conform Password')
        NewPwd2.bind("<FocusIn>",on_enter)
        NewPwd2.bind("<FocusOut>",on_leave)
        Frame(panel,width=300,height=2,bg='black').place(x=600,y=205)

        searchBtn=Button(panel,width=39,pady=7,text='Change Password',bg='#57a1f8',fg='white',border=0, command = change_pwd, font=("Helvetica",16,"bold"), bd = 0)
        searchBtn.place(x=600, y=260, height = 50, width = 250)

        img=PhotoImage(file='./media/pass.png')
        Label(panel,image=img,border=0,bg='white').place(x=50,y=70)
        print(1)

    def draw_edit_student():
        def search():
            option = dropdown.get()
            search_input = searchInput.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            if search_input == "":
                mycursor.execute("SELECT * FROM student_table")
            elif option == "Name":
                mycursor.execute("SELECT * FROM student_table WHERE name = '" + str(search_input).upper() + "'")
            elif option == "UID":
                mycursor.execute("SELECT * FROM student_table WHERE id = '" + str(search_input) + "'")
            elif option == "Semester":
                mycursor.execute("SELECT * FROM student_table WHERE sem = " + str(search_input))
            elif option == "Department":
                mycursor.execute("SELECT * FROM student_table WHERE stream = '" + str(search_input).upper() + "'")
            else:
                return
            rows = mycursor.fetchall()
            data_table.delete(*data_table.get_children())
            if rows == None:
                note_text['text'] = "Data: 0 Rows"
                return 
            note_text['text'] = "Data: "+str(len(rows))+" Rows"
            for row in rows:
                data_table.insert('', END, values=row)
            db.commit()
            db.close()
            # pass


        # IT WILL SHOW VALUE FROM DATABASE
        def show():
            id = IdEntry.get()
            nam = NameEntry.get()
            desig = SemesterEntry.get()
            dept = DepartmentEntry.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            mycursor.execute("select * from student_table")
            rows = mycursor.fetchall()
            if len(rows) != 0:
                data_table.delete(*data_table.get_children())
            for row in rows:
                data_table.insert('', END, values=row)
            db.commit()
            db.close()

        # IT WILL GET DATA IN LEFTBOX (getdata made events there and fecth value there also)
        def getdata(event):
            currow = data_table.focus()
            contents = data_table.item(currow)
            row = contents['values']
            updatebt.configure(state = "normal")
            deletebt.configure(state = "normal")
            IdEntry.configure(state='normal')
            IdEntry.delete(0, END)
            NameEntry.delete(0, END)
            SemesterEntry.delete(0, END)
            DepartmentEntry.delete(0, END)
            IdEntry.insert(0, row[0])
            IdEntry.configure(state='readonly')
            NameEntry.insert(0, row[1])
            SemesterEntry.insert(0, row[2])
            DepartmentEntry.insert(0, row[3])
            addbt.configure(state = 'disabled')

        # IT WILL ADD DATAS
        def add():
            if IdEntry.get()=="" or NameEntry.get()=="" or SemesterEntry.get()=="" or DepartmentEntry.get()=="":
               messagebox.showerror("Error","All fields are required")
            else:
                iD=IdEntry.get()
                name=NameEntry.get()
                sem=SemesterEntry.get()
                dept=DepartmentEntry.get()
                db=mysql.connector.connect(host="localhost",user="root",password="",database="KBP")
                mycursor=db.cursor()
                try:
                   sql="insert into student_details_table(id,name,profession,department)values(%s,%s,%s,%s)"
                   val=(id,name,sem,dept)
                   # mycursor.execute(sql,val)
                   mycursor.execute("INSERT INTO student_table (id,name,sem,stream) VALUES ('"+str(iD)+"', '"+str(name).upper()+"', "+str(sem)+", '"+str(dept).upper()+"')")
                   db.commit()
                   messagebox.showinfo("information","Record Inserted successfully")
                   show()
                   clear()
                except EXCEPTION as e:
                   print(e)
                   db.rollback()
                   db.close()

        def update():
            iD = IdEntry.get()
            name = NameEntry.get()
            sem = SemesterEntry.get()
            dept = DepartmentEntry.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            mycursor.execute("UPDATE student_table SET name = '"+str(name).upper()+"', sem = "+str(sem)+", stream = '"+str(dept).upper()+"' WHERE id = '"+str(iD)+"'")
            db.commit()
            messagebox.showinfo("information", "Record Updated successfully")
            IdEntry.delete(0, END)
            NameEntry.delete(0, END)
            SemesterEntry.delete(0, END)
            DepartmentEntry.delete(0, END)
            show()
            clear()

        def delete1():
            iD = IdEntry.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            sql = "DELETE FROM student_table WHERE id='"+str(iD)+"'"
            mycursor.execute(sql)
            db.commit()
            messagebox.showinfo("information", "Record Deleted successfully")
            IdEntry.delete(0, END)
            NameEntry.delete(0, END)
            SemesterEntry.delete(0, END)
            DepartmentEntry.delete(0, END)
            show()
            clear()

        # IT WILL CLEAR DATAS
        def clear():
            updatebt.configure(state = "disabled")
            deletebt.configure(state = "disabled")
            IdEntry.configure(state='normal')
            IdEntry.delete(0, END)
            IdEntry.insert(0,random_string())
            NameEntry.delete(0, END)
            SemesterEntry.delete(0, END)
            DepartmentEntry.delete(0, END)
            NameEntry.focus_set()
            addbt.configure(state='normal')
        def random_string():
            count = 1
            S = 5
            while(count!=0):
                ran = ''.join(random.choices(string.ascii_letters + string.digits, k = S))
                db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
                mycursor = db.cursor()
                mycursor.execute("select count(id) from student_table where id = '"+str(ran)+"'")
                rows = mycursor.fetchone()
                count = rows[0]
            return ran
        label=Frame(footer,bd=0,bg="brown")
        label.place(x=0,y=0,width=1080,height=85)
        abcframe=Frame(footer,bd=0,bg="black")
        abcframe.place(x=90,y=15,width=900,height=1)
        ILabel=Label(label,text="Here You Can Edit Or View Student database",font=("Helvetica",20),fg="#eae2b7",bg="brown")
        ILabel.place(x=260, y =30)
        # LEFT BOX
        leftbox=Frame(dashboard,bd=0,bg="brown")
        leftbox.place(x=0,y=50,width=600,height=450)
        # INSIDE LEFT BOX
        leftbox_title=Label(leftbox,text="Manage Database",font=("Helvetica",20,"bold"),fg="#eae2b7",bg="brown")
        leftbox_title.place(x=100, y=10)
        IdLable=Label(leftbox,text="ID",font=("Helvetica",15),fg="#eae2b7",bg="brown")
        IdLable.place(x=70, y =60)
        IdEntry=Entry(leftbox,font=("Helvetica",15),bd=0)
        IdEntry.insert(0,random_string())
        IdEntry.place(x=260, y =70, width = 80)
        NameLable=Label(leftbox,text="Name",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
        NameLable.place(x=60, y=110)
        NameEntry=Entry(leftbox,font=("Helvetica", 15),bd=0)
        NameEntry.place(x=140, y=110, width = 200)
        SemesterLable=Label(leftbox,text="Semester",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
        SemesterLable.place(x=60, y=160)
        SemesterEntry=Entry(leftbox,font=("Helvetica", 15),bd=0)
        SemesterEntry.place(x=160, y=160, width = 180)
        DepartmentLable=Label(leftbox,text="Department",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
        DepartmentLable.place(x=60, y=210)
        DepartmentEntry=Entry(leftbox,font=("Helvetica", 15),bd=0)
        DepartmentEntry.place(x=190, y=210, width = 150)

        # LEFT BOX BUTTONS
        btnfrm=Frame(leftbox, bd=0, bg="brown")
        btnfrm.place(x=10,y=250,width=350,height=50)

        addbt=Button(btnfrm,text="Add",font=("Helvetica", 15),bg="indianred",fg="white",bd=0,command=add)
        addbt.place(x=50, y=0, width = 130)
        updatebt=Button(btnfrm,text="Edit",font=("Helvetica", 15),bg="indianred",fg="white",bd=0,command=update)
        updatebt.configure(state = "disabled")
        updatebt.place(x=200, y=0, width = 130)

        btnfrm2=Frame(leftbox,relief=RIDGE,bg="brown")
        btnfrm2.place(x=10,y=300,width=350,height=50)

        deletebt=Button(btnfrm2,text="Delete",font=("Helvetica", 15),bg="indianred",fg="white",command=delete1, bd =0)
        deletebt.configure(state = "disabled")
        deletebt.place(x=50, y=0, width = 130)
        clrbt=Button(btnfrm2,text="Clear",font=("Helvetica", 15),bg="indianred",fg="white",command=clear, bd = 0)
        clrbt.place(x=200, y=0, width = 130)






        # RIGHT BOX
        rightbox=Frame(dashboard,bd=0,bg="indianred")
        rightbox.place(x=450,y=50,width=630,height=450)

        # RIGHT BOX HEADING
        searchBy=Label(rightbox,text="Enter Value",font=("Helvetica", 14),bg="indianred",fg="white")
        searchBy.place(x=10, y=10)
        searchInput=Entry(rightbox,font=("Helvetica", 12),bd=0,width=17)
        searchInput.place(x=130, y=10, height = 30)
        dropdown=ttk.Combobox(rightbox,font=("Helvetica",12),state='readonly', width = 12)
        dropdown['values']=("--Search By--", "Name", "UID", "Designation", "Department")
        dropdown.current(0)
        dropdown.place(x=300, y=10, height = 30)
        searchBtn=Button(rightbox,text="Search",command=search,font=("Helvetica", 12),width=10, bd = 0)
        searchBtn.place(x=450, y=10, height = 30)

        # BOX INSIDE RIGHT BOX
        tabfrm=Frame(rightbox,bd=4,relief=RIDGE,bg="lightblue")
        tabfrm.place(x=10,y=50,width=550,height=270)
        scrolly=Scrollbar(tabfrm,orient=VERTICAL)
        data_table=ttk.Treeview(tabfrm,columns=("id","name","semester","department"),yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=data_table.yview)

        note_text=Label(rightbox,font=("Helvetica", 10),bg="indianred",fg="white")
        note_text.place(x=10, y=325)

       
        # INSIDE RIGHT BOX
        data_table.heading("id",text="ID")
        data_table.heading("name",text="Name")
        data_table.heading("semester",text="Semester")
        data_table.heading("department",text="Department")
        data_table['show']="headings"
        data_table.column("id",width = 10)
        data_table.column("name",width=200)
        data_table.column("semester",width=30)
        data_table.column("department",width=30)
        data_table.pack(fill=BOTH,expand=1)
        data_table.bind("<ButtonRelease-1>",getdata)
        # show()
        search()
    def draw_edit_notice_board():
        def search():
            option = dropdown.get()
            search_input = searchInput.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            if search_input == "":
                mycursor.execute("SELECT * FROM notice_board")
            elif option == "UID":
                mycursor.execute("SELECT * FROM notice_board WHERE id = '" + str(search_input) + "'")
            elif option == "Topic":
                mycursor.execute("SELECT * FROM notice_board WHERE topic = '" + str(search_input).upper() + "'")
            else:
                return
            rows = mycursor.fetchall()
            data_table.delete(*data_table.get_children())
            if rows == None:
                note_text['text'] = "Data: 0 Rows"
                return 
            note_text['text'] = "Data: "+str(len(rows))+" Rows"
            for row in rows:
                data_table.insert('', END, values=row)
            db.commit()
            db.close()
            # pass


        # IT WILL SHOW VALUE FROM DATABASE
        def show():
            id = IdEntry.get()
            nam = TopicEntry.get()
            desig = DescriptionEntry.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            mycursor.execute("select * from notice_board")
            rows = mycursor.fetchall()
            if len(rows) != 0:
                data_table.delete(*data_table.get_children())
            for row in rows:
                data_table.insert('', END, values=row)
            db.commit()
            db.close()

        # IT WILL GET DATA IN LEFTBOX (getdata made events there and fecth value there also)
        def getdata(event):
            currow = data_table.focus()
            contents = data_table.item(currow)
            row = contents['values']
            updatebt.configure(state = "normal")
            deletebt.configure(state = "normal")
            IdEntry.configure(state='normal')
            IdEntry.delete(0, END)
            TopicEntry.delete(0, END)
            DescriptionEntry.delete("1.0", "end")
            IdEntry.insert(0, row[0])
            IdEntry.configure(state='readonly')
            TopicEntry.insert(0, row[1])
            DescriptionEntry.insert(END, row[2])
            addbt.configure(state = 'disabled')

        # IT WILL ADD DATAS
        def add():
            if IdEntry.get()=="" or TopicEntry.get()=="" or DescriptionEntry.get(1.0, "end-1c")=="":
               messagebox.showerror("Error","All fields are required")
            else:
                iD=IdEntry.get()
                name=TopicEntry.get()
                desg=DescriptionEntry.get(1.0, "end-1c")
                db=mysql.connector.connect(host="localhost",user="root",password="",database="KBP")
                mycursor=db.cursor()
                desg = db.converter.escape(desg)
                try:
                   mycursor.execute("INSERT INTO notice_board (id, topic, description) VALUES ('"+str(iD)+"', '"+str(name).upper()+"', '"+str(desg)+"')")
                   db.commit()
                   messagebox.showinfo("information","Record Inserted successfully")
                   search()
                   clear()
                except EXCEPTION as e:
                   print(e)
                   db.rollback()
                   db.close()

        def update():
            iD = IdEntry.get()
            name = TopicEntry.get()
            desg = DescriptionEntry.get(1.0, "end-1c")
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            desg = db.converter.escape(desg)
            mycursor.execute("UPDATE notice_board SET topic = '"+str(name).upper()+"', description = '"+str(desg)+"' WHERE id = '"+str(iD)+"'")
            db.commit()
            messagebox.showinfo("information", "Record Updated successfully")
            IdEntry.delete(0, END)
            TopicEntry.delete(0, END)
            DescriptionEntry.delete("1.0", "end")
            search()
            clear()

        def delete1():
            iD = IdEntry.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            sql = "DELETE FROM notice_board WHERE id='"+str(iD)+"'"
            mycursor.execute(sql)
            db.commit()
            messagebox.showinfo("information", "Record Deleted successfully")
            IdEntry.delete(0, END)
            TopicEntry.delete(0, END)
            DescriptionEntry.delete("1.0", "end")
            search()
            clear()


        # IT WILL CLEAR DATAS
        def clear():
            updatebt.configure(state = "disabled")
            deletebt.configure(state = "disabled")
            IdEntry.configure(state='normal')
            IdEntry.delete(0, END)
            IdEntry.insert(0,random_string())
            TopicEntry.delete(0, END)
            DescriptionEntry.delete("1.0", "end")
            TopicEntry.focus_set()
            addbt.configure(state='normal')
        def random_string():
            count = 1
            S = 5
            while(count!=0):
                ran = ''.join(random.choices(string.ascii_letters + string.digits, k = S))
                db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
                mycursor = db.cursor()
                mycursor.execute("select count(id) from notice_board where id = '"+str(ran)+"'")
                rows = mycursor.fetchone()
                count = rows[0]
            return ran
        label=Frame(footer,bd=0,bg="brown")
        label.place(x=0,y=0,width=1080,height=85)
        abcframe=Frame(footer,bd=0,bg="black")
        abcframe.place(x=90,y=15,width=900,height=1)
        ILabel=Label(label,text="Here You Can Edit Or View Notice Board database",font=("Helvetica",20),fg="#eae2b7",bg="brown")
        ILabel.place(x=250, y=30)
        leftbox=Frame(dashboard,bd=0,bg="brown")
        leftbox.place(x=0,y=50,width=550,height=350)

        # INSIDE LEFT BOX
        leftbox_title=Label(leftbox,text="Manage Database",font=("Helvetica",20,"bold"),fg="#eae2b7",bg="brown")
        leftbox_title.place(x=50, y=10, width=  500)
        IdLabel=Label(leftbox,text="ID",font=("Helvetica",15),fg="#eae2b7",bg="brown")
        IdLabel.place(x=50, y =50)
        IdEntry=Entry(leftbox,font=("Helvetica",15),bd=0)
        IdEntry.insert(0,random_string())
        IdEntry.place(x=100, y =50, width = 80)
        TopicLabel=Label(leftbox,text="Topic",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
        TopicLabel.place(x=250, y=50)
        TopicEntry=Entry(leftbox,font=("Helvetica", 15),bd=0)
        TopicEntry.place(x=320, y=50, width = 200)
        DescriptionLabel=Label(leftbox,text="Description",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
        DescriptionLabel.place(x=50, y=80)
        scrolly=Scrollbar(leftbox,orient=VERTICAL)
        DescriptionEntry=Text(leftbox, font=("Helvetica", 15),bd=0, yscrollcommand=scrolly.set)
        scrolly.config(command=DescriptionEntry.yview)
        DescriptionEntry.place(x=50, y=110, width = 450, height = 170)
        scrolly.place(x=510, y=110, height = 170)


        # LEFT BOX BUTTONS
        btnfrm=Frame(leftbox, bd=0, bg="brown")
        btnfrm.place(x=0,y=300,width=500,height=50)

        addbt=Button(btnfrm,text="Add",font=("Helvetica", 12),bg="indianred",fg="white",bd=0,command=add)
        addbt.place(x=50, y=0, width = 70)
        updatebt=Button(btnfrm,text="Edit",font=("Helvetica", 12),bg="indianred",fg="white",bd=0,command=update)
        updatebt.configure(state = "disabled")
        updatebt.place(x=150, y=0, width = 70)
        deletebt=Button(btnfrm,text="Delete",font=("Helvetica", 12),bg="indianred",fg="white",command=delete1, bd =0)
        deletebt.configure(state = "disabled")
        deletebt.place(x=250, y=0, width = 70)
        clrbt=Button(btnfrm,text="Clear",font=("Helvetica", 12),bg="indianred",fg="white",command=clear, bd = 0)
        clrbt.place(x=350, y=0, width = 70)






        # RIGHT BOX
        rightbox=Frame(dashboard,bd=0,bg="indianred")
        rightbox.place(x=550,y=50,width=600,height=350)

        # RIGHT BOX HEADING
        searchInput=Entry(rightbox,font=("Helvetica", 12),bd=0,width=17)
        searchInput.place(x=10, y=10, height = 30)
        dropdown=ttk.Combobox(rightbox,font=("Helvetica",10),state='readonly', width = 10)
        dropdown['values']=("--Search By--", "UID", "Topic")
        dropdown.current(0)
        dropdown.place(x=180, y=10, height = 30)
        searchBtn=Button(rightbox,text="Search",command=search,font=("Helvetica", 12),width=10, bd = 0)
        searchBtn.place(x=280, y=10, height = 30)

        # BOX INSIDE RIGHT BOX
        tabfrm=Frame(rightbox,bd=4,relief=RIDGE,bg="lightblue")
        tabfrm.place(x=10,y=50,width=510,height=270)
        scrolly=Scrollbar(tabfrm,orient=VERTICAL)
        data_table=ttk.Treeview(tabfrm,columns=("id","name","description"),yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=data_table.yview)

        note_text=Label(rightbox,font=("Helvetica", 10),bg="indianred",fg="white")
        note_text.place(x=10, y=325)

        # INSIDE RIGHT BOX
        data_table.heading("id",text="ID")
        data_table.heading("name",text="Topic")
        data_table.heading("description",text="Description")
        data_table['show']="headings"
        data_table.column("id",width = 10)
        data_table.column("name",width=50)
        data_table.column("description",width=30)
        data_table.pack(fill=BOTH,expand=1)
        data_table.bind("<ButtonRelease-1>",getdata)
        search()
    def draw_edit_company_list():
        def search():
            option = dropdown.get()
            search_input = searchInput.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            if search_input == "":
                mycursor.execute("SELECT * FROM company_list")
            elif option == "Name":
                mycursor.execute("SELECT * FROM company_list WHERE name = '" + str(search_input).upper() + "'")
            elif option == "Year":
                mycursor.execute("SELECT * FROM company_list WHERE year LIKE '%" + str(search_input).upper() + "%'")
            elif option == "Department":
                mycursor.execute("SELECT * FROM company_list WHERE dept lIKE '%" + str(search_input).upper() + "%'")
            else:
                return
            rows = mycursor.fetchall()
            data_table.delete(*data_table.get_children())
            if rows == None:
                note_text['text'] = "Data: 0 Rows"
                return 
            note_text['text'] = "Data: "+str(len(rows))+" Rows"
            for row in rows:
                data_table.insert('', END, values=row)
            db.commit()
            db.close()
            # pass


        # IT WILL GET DATA IN LEFTBOX (getdata made events there and fecth value there also)
        def getdata(event):
            currow = data_table.focus()
            contents = data_table.item(currow)
            row = contents['values']
            updatebt.configure(state = "normal")
            deletebt.configure(state = "normal")
            NameEntry.configure(state='normal')
            NameEntry.delete(0, END)
            YearEntry.delete("1.0", "end")
            DepartmentEntry.delete("1.0", "end")
            NameEntry.insert(0, row[0])
            NameEntry.configure(state='readonly')
            YearEntry.insert(END, row[2])
            DepartmentEntry.insert(END, row[1])
            addbt.configure(state = 'disabled')

        # IT WILL ADD DATAS
        def add():
            if NameEntry.get()=="" or YearEntry.get(1.0, "end-1c")=="" or DepartmentEntry.get(1.0, "end-1c")=="":
               messagebox.showerror("Error","All fields are required")
            else:
                name=NameEntry.get()
                year=YearEntry.get(1.0, "end-1c")
                dept=DepartmentEntry.get(1.0, "end-1c")
                db=mysql.connector.connect(host="localhost",user="root",password="",database="KBP")
                mycursor=db.cursor()
                try:
                   mycursor.execute("INSERT INTO company_list (name, year, dept) VALUES ('"+str(name).upper()+"', '"+str(year).upper()+"', '"+str(dept).upper()+"')")
                   db.commit()
                   messagebox.showinfo("Information","Record Inserted successfully")
                   search()
                   clear()
                except EXCEPTION as e:
                   print(e)
                   db.rollback()
                   db.close()

        def update():
            name = NameEntry.get()
            year = YearEntry.get(1.0, "end-1c")
            dept = DepartmentEntry.get(1.0, "end-1c")
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            # dept = db.converter.escape(dept)
            mycursor.execute("UPDATE company_list SET year = '"+str(year).upper()+"', dept = '"+str(dept).upper()+"' WHERE name = '"+str(name).upper()+"'")
            db.commit()
            messagebox.showinfo("information", "Record Updated successfully")
            NameEntry.delete(0, END)
            YearEntry.delete("1.0", "end")
            DepartmentEntry.delete("1.0", "end")
            search()
            clear()

        def delete1():
            name = NameEntry.get()
            db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
            mycursor = db.cursor()
            sql = "DELETE FROM company_list WHERE name='"+str(name).upper()+"'"
            mycursor.execute(sql)
            db.commit()
            messagebox.showinfo("information", "Record Deleted successfully")
            NameEntry.delete(0, END)
            YearEntry.delete("1.0", "end")
            DepartmentEntry.delete("1.0", "end")
            search()
            clear()


        # IT WILL CLEAR DATAS
        def clear():
            updatebt.configure(state = "disabled")
            deletebt.configure(state = "disabled")
            NameEntry.configure(state='normal')
            NameEntry.delete(0, END)
            YearEntry.delete("1.0", "end")
            DepartmentEntry.delete("1.0", "end")
            addbt.configure(state='normal')
            
        label=Frame(footer,bd=0,bg="brown")
        label.place(x=0,y=0,width=1080,height=85)
        abcframe=Frame(footer,bd=0,bg="black")
        abcframe.place(x=90,y=15,width=900,height=1)
        ILabel=Label(label,text="Here You Can Edit Or View Company database",font=("Helvetica",20),fg="#eae2b7",bg="brown")
        ILabel.place(x=250, y =30)
       
        # LEFT BOX
        leftbox=Frame(dashboard,bd=0,bg="brown")
        leftbox.place(x=0,y=50,width=600,height=350)

        # INSIDE LEFT BOX
        leftbox_title=Label(leftbox,text="Manage Database",font=("Helvetica",20,"bold"),fg="#eae2b7",bg="brown")
        leftbox_title.place(x=10, y=30, width=  500)
        NameLabel=Label(leftbox,text="Company Name",font=("Helvetica",15),fg="#eae2b7",bg="brown")
        NameLabel.place(x=10, y =90)
        NameEntry=Entry(leftbox,font=("Helvetica",15),bd=0)
        NameEntry.place(x=160, y =90, width = 317)
        YearLabel=Label(leftbox,text="Year",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
        YearLabel.place(x=10, y=120)
        scrolly=Scrollbar(leftbox,orient=VERTICAL)
        YearEntry=Text(leftbox, font=("Helvetica", 15),bd=0, yscrollcommand=scrolly.set)
        scrolly.config(command=YearEntry.yview)
        YearEntry.place(x=160, y=120, width = 300, height = 70)
        scrolly.place(x=460, y=120, height = 70)
        DepartmentLabel=Label(leftbox,text="Department",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
        DepartmentLabel.place(x=10, y=190)
        scrolly=Scrollbar(leftbox,orient=VERTICAL)
        DepartmentEntry=Text(leftbox, font=("Helvetica", 15),bd=0, yscrollcommand=scrolly.set)
        # DescriptionEntry['text'] = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
        scrolly.config(command=DepartmentEntry.yview)
        DepartmentEntry.place(x=160, y=195, width = 300, height = 70)
        scrolly.place(x=460, y=195, height = 70)


        # LEFT BOX BUTTONS
        btnfrm=Frame(leftbox, bd=0, bg="brown")
        btnfrm.place(x=0,y=300,width=500,height=50)

        addbt=Button(btnfrm,text="Add",font=("Helvetica", 12),bg="indianred",fg="white",bd=0,command=add)
        addbt.place(x=50, y=0, width = 70)
        updatebt=Button(btnfrm,text="Edit",font=("Helvetica", 12),bg="indianred",fg="white",bd=0,command=update)
        updatebt.configure(state = "disabled")
        updatebt.place(x=150, y=0, width = 70)
        deletebt=Button(btnfrm,text="Delete",font=("Helvetica", 12),bg="indianred",fg="white",command=delete1, bd =0)
        deletebt.configure(state = "disabled")
        deletebt.place(x=250, y=0, width = 70)
        clrbt=Button(btnfrm,text="Clear",font=("Helvetica", 12),bg="indianred",fg="white",command=clear, bd = 0)
        clrbt.place(x=350, y=0, width = 70)






        # RIGHT BOX
        rightbox=Frame(dashboard,bd=0,bg="indianred")
        rightbox.place(x=500,y=50,width=600,height=350)

        # RIGHT BOX HEADING
        searchInput=Entry(rightbox,font=("Helvetica", 12),bd=0,width=17)
        searchInput.place(x=10, y=10, height = 30)
        dropdown=ttk.Combobox(rightbox,font=("Helvetica",10),state='readonly', width = 10)
        dropdown['values']=("--Search By--", "Name", "Year", "Department")
        dropdown.current(0)
        dropdown.place(x=180, y=10, height = 30)
        searchBtn=Button(rightbox,text="Search",command=search,font=("Helvetica", 12),width=10, bd = 0)
        searchBtn.place(x=280, y=10, height = 30)

        # BOX INSIDE RIGHT BOX
        tabfrm=Frame(rightbox,bd=4,relief=RIDGE,bg="lightblue")
        tabfrm.place(x=10,y=50,width=550,height=270)
        scrolly=Scrollbar(tabfrm,orient=VERTICAL)
        data_table=ttk.Treeview(tabfrm,columns=("name","department", "year"),yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=data_table.yview)

        note_text=Label(rightbox,font=("Helvetica", 10),bg="indianred",fg="white")
        note_text.place(x=10, y=325)

        # INSIDE RIGHT BOX
        data_table.heading("name",text="Name")
        data_table.heading("year",text="Year")
        data_table.heading("department",text="Department")
        data_table['show']="headings"
        data_table.column("name",width = 10)
        data_table.column("year",width=50)
        data_table.column("department",width=30)
        data_table.pack(fill=BOTH,expand=1)
        data_table.bind("<ButtonRelease-1>",getdata)
        search()
    
    for widget in dashboard.winfo_children():
        widget.destroy()
    
   
    
    footer=Frame(root, bg="brown", bd=0)
    footer.place(x=0,y=565,width=1080,height=85)
    welcome_text["text"] = "Welcome To The College Page"
    welcome_text.place(x=400)
    image1 = Image.open("media/kbp.jpg")
    im1 = image1.filter(ImageFilter.BLUR)
    test = ImageTk.PhotoImage(im1)
    label1 = Label(dashboard,image=test)
    label1.photo = test
    label1.place(x=0, y=0, height = 400, width = 1080)
    option= Button(dashboard, text ="View/Edit Student", command=draw_edit_student, bd =0, font=("Helvetica",11),fg='#0097e8',activeforeground='#0097e8')
    option.place(x=0, y=0, width = 300, height = 50)
    
   
    option= Button(dashboard, text ="Change Password", command=draw_change_password, bd =0, font=("Helvetica",11),fg='#0097e8',activeforeground='#0097e8')
    option.place(x=280, y=0, width = 300, height = 50)
 
    option= Button(dashboard, text ="View/Edit Notice Board", command=draw_edit_notice_board, bd =0, font=("Helvetica",11),fg='#0097e8',activeforeground='#0097e8')
    option.place(x=530, y=0, width = 300, height = 50)
   
    
    option= Button(dashboard, text ="View/Edit Company List", command=draw_edit_company_list,bd =0, font=("Helvetica",11),fg='#0097e8',activeforeground='#0097e8')
    option.place(x=780, y=0, width = 300, height = 50)
   
    
def staff():
    for widget in dashboard.winfo_children():
        widget.destroy()
    
 
    
    footer=Frame(root, bg="white", bd=0)
    footer.place(x=0,y=565,width=1080,height=85)

    def DetectFace():
        df = pd.read_csv('staff Profile.csv')
        df.sort_values('Ids', inplace = True)
        df.drop_duplicates(subset = 'Ids', keep = 'first', inplace = True)
        df.to_csv('staff Profile.csv', index = False)
        Name=user.get() 
        ID_Number= code.get()
        #print(OTP1)
        name , Id = '',''
        dic = {
            'Name' : Name,
            'Ids' : ID_Number
        }
        def store_data():
            global name,Id,dic
            name = Name
                   
            Id  = ID_Number
                   
            dic = {
                'Ids' : ID_Number,
                'Name': Name
            }
            c = dic
            return  c
        reader = csv.DictReader(open('staff Profile.csv'))
        print('Detecting Login Face')
        for rows in reader:
            result = dict(rows)
            a=int(result['Ids'])
            if a <100:
                name1 = result['Name']
            
        recognizer = cv2.face.LBPHFaceRecognizer_create()  #cv2.createLBPHFaceRecognizer()
        recognizer.read("TrainData\Trainner.yml")
        harcascadePath = 'C:\\Users\\vaibh\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml '
        faceCascade = cv2.CascadeClassifier(harcascadePath);
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        Face_Id = ''
        name2 = ''

        # Camera ON Everytime
        while True:
            ret, frame = cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.3, 5)
            Face_Id = 'Not detected'

            # Drawing a rectagle around the face 
            for (x, y, w, h) in faces:
                Face_Id = 'Not detected'
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
                if (confidence < 90):
                    if (Id <100):
                        name = name1
                    Predicted_name = str(name)
                    Face_Id = Predicted_name
                    print(name)
                    
                else:
                    Predicted_name = 'Unknown'
                    Face_Id = Predicted_name
                    # Here unknown faces detected will be stored
                    noOfFile = len(os.listdir("UnknownFaces")) + 1
                    if int(noOfFile) < 100:
                        cv2.imwrite("UnknownFaces\Image" + str(noOfFile) + ".jpg", frame[y:y + h, x:x + w])
                    
                    else:
                        pass


                cv2.putText(frame, str(Predicted_name), (x, y + h), font, 1, (255, 255, 255), 2)
                
            cv2.imshow('Picture', frame)
            #print(Face_Id)
            cv2.waitKey(1)

            # Checking if the face matches for Login
            if Face_Id == name1 or name2 and Face_Id != 'Unknown' :
                mydate = datetime.datetime.now()
                
                date = datetime.datetime.strftime(mydate, '%d, %m, %Y')
                time = datetime.datetime.strftime(mydate, '%H, %M, %S')
                d={'Name':Face_Id,'Ids':Id,'Date':date,'Time':time}
                with open('staff attendance.csv','a+') as f:
                    fields = ['Name','Ids','Date','Time']   
                    writer=csv.DictWriter(f,fieldnames=fields)
                    

                    writer.writerow(d)
                messagebox.showinfo("LOGIN","login succesfull!!" )
                cv2.destroyAllWindows()
                draw_staff()
                
                
                break
                
            elif Face_Id == 'Not detected':
                print("-----Face Not Detected, Try again------")
                pass
            else:
                print('-----------Login failed please try agian-------')
            
            
            if (cv2.waitKey(1) == ord('q')):
               break
            
            
        def DetectFace():
            root.destroy()
       


    def signin():
        Name=user.get()
        ID_Number=code.get()
        name , Id = '',''
        dic = {
            'Name' : Name,
            'Ids' : ID_Number
        }
        def store_data(signin):
            global name,Id,dic
            name = Name
           
            Id  = ID_Number
           
            dic = {
                'Ids' : ID_Number,
                'Name': Name
            }
            c = dic
            return  c
        db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
        mycursor=db.cursor()
        if Name == "" and ID_Number == "":
            print(1)
            messagebox.showinfo("Invalid","Both The Fields Are Empty!!" )
        elif Name == "" or ID_Number == " ":
               messagebox.showinfo("Invalid","Any Field Is Empty Please Filed It!!" )
        else:
            print(ID_Number)
            query = "SELECT * FROM staff WHERE Name = %(name)s AND ID_Number = %(id_number)s"
            params = {'name': Name, 'id_number': ID_Number}
            mycursor.execute(query, params)
 
        print(params)    
        result=mycursor.fetchall()
        print(result)
        
        if result=="":
            print(3)
            messagebox.showinfo("Invalid","Invalid username or password!!" )
        else :
            if result:
    
                for row in result:
                     name, id_number, other_column1, other_column2 = row
                     print(f"Name: {name}, ID_Number: {id_number}, Other_Column1: {other_column1}, Other_Column2: {other_column2}")
                print(4)
                mydate = datetime.datetime.now()  
                date = datetime.datetime.strftime(mydate, '%d, %m, %Y')
                time = datetime.datetime.strftime(mydate, '%H, %M, %S')
                d={'Name':Name,'Ids':ID_Number,'Date':date,'Time':time}
                with open('staff attendance.csv','a+') as f:
                    print(date)
                    fields = ['Name','Ids','Date','Time']
                    writer=csv.DictWriter(f,fieldnames=fields)
                    writer.writerow(d)
                messagebox.showinfo("LOGIN","login succesfull!!" )
                draw_admin()
            
        def signin():
            root.destroy()
       

            
    ###########________________________________________sign up code
    def signup_command():
        for widget in dashboard.winfo_children():
            widget.destroy()
        def signup():
            Name=user.get() 
            Mobile_Number=code.get()
            Emailid=conform_code.get()
            ID_Number=email.get()
            #print(OTP1)
            name , Id = '',''
            dic = {
                'Name' : Name,
                'Ids' : ID_Number
            }
            def store_data():
                global name,Id,dic
                name = Name
                   
                Id  = ID_Number
                   
                dic = {
                    'Ids' : ID_Number,
                    'Name': Name
                }
                c = dic
                return  c
            x=len(Mobile_Number)
            if Name=="" or Mobile_Number=="" or Emailid=="" or ID_Number=="":
                messagebox.showinfo("Insert Status","All Fileds are required")
                
            elif (x!=10):
                Label(frame,width=39,pady=7,text='*Invalid Number',bg='white',fg='Red',border=0).place(x=130,y=250)
            else:
                db=mysql.connector.connect(host="localhost",user="root",password="",database="KBP")
                mycursor=db.cursor()
                mycursor.execute("INSERT INTO staff (Name,ID_Number,Mobile_Number,Emailid) VALUES ('"+str(Name)+"', '"+str(ID_Number).upper()+"', '"+str(Mobile_Number).upper()+"', '"+str(Emailid).upper()+"')")
                db.commit()
                
                db.close();
                def getImagesAndLabels(path):
                    # Get the path of all the files in the folder
                    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]  
                    # Create empth face list
                    faces = []
                    # Create empty ID list
                    Ids = []
                    # Looping through all the image paths and loading the Ids and the images
                    for imagePath in imagePaths:
                        # Loading the image and converting it to gray scale
                        pilImage = Image.open(imagePath).convert('L')
                        # Now we are converting the PIL image into numpy array
                        imageNp = np.array(pilImage, 'uint8')
                        # getting the Id from the image
                        Id = int(os.path.split(imagePath)[-1].split(".")[1])
                        # extract the face from the training image sample
                        faces.append(imageNp)
                        
                        Ids.append(Id)
                    return faces, Ids

                # Train image using LBPHFFace recognizer 
                recognizer = cv2.face.LBPHFaceRecognizer_create()  # recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
                harcascadePath = 'C:\\Users\\vaibh\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml '
                detector = cv2.CascadeClassifier(harcascadePath)
                faces , Id= getImagesAndLabels("C:\\Users\\vaibh\\Desktop\\College-Management-System-using-Python-and-Tkinter-main\\College-Management-System-using-Python-and-Tkinter-main\\TrainingImage")
                recognizer.train(faces, np.array(Id))
                #store data in file 
                recognizer.save("TrainData\Trainner.yml")
                res = "Image Trained and data stored in TrainData\Trainner.yml "

                print(res)
                messagebox.showinfo("Registration","Registered Successfully")
                staff()

           
        def TakeImages():
            Name=user.get() 
            ID_Number=email.get()
            Mobile_Number=code.get()
            Emailid=conform_code.get()
            
            #print(OTP1)
            name , Id,mobileno,emailid = '','','',''
            dic = {
                'Name' : Name,
                'Ids' : ID_Number,
                'Mobile Number':Mobile_Number,
                'Email-Id':Emailid
            }
            def store_data():
                global name,Id,dic
                name = Name
                mobileno = Mobile_Number
                emailid = Emailid
                Id  = ID_Number
                   
                dic = {
                    'Ids' : ID_Number,
                    'Name': Name,
                    'Mobile Number':Mobile_Number,
                    'Email-Id':Emailid
                }
                c = dic
                return  c
            dict1 = store_data()
            print(dict1)        
            if (Name.isalpha()):
                if Id == '1':
                    fieldnames = ['Name','Ids','Mobile Number','Email-Id']
                    with open('staff Profile.csv','w') as f:
                        writer = csv.DictWriter(f, fieldnames =fieldnames)
                        writer.writerow(dict1)
                else:
                    fieldnames = ['Name','Ids','Mobile Number','Email-Id']
                    with open('staff Profile.csv','a') as f:
                        writer = csv.DictWriter(f, fieldnames =fieldnames)
                        writer.writerow(dict1)
                cam = cv2.VideoCapture(0)

                #Haarcascade file for detctionof face
                harcascadePath = 'C:\\Users\\vaibh\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml '
                detector = cv2.CascadeClassifier(harcascadePath)
                sampleNum = 0
                while (True):
                    ret, img = cam.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = detector.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                        # Incrementing sample number
                        sampleNum = sampleNum + 1
                        # Saving the captured face in the dataset folder TrainingImage
                        cv2.imwrite("TrainingImage\ " + Name + "." + ID_Number + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                        # display the frame
                    cv2.imshow('Cpaturing Face for Login ', img)
                
                    # wait for 100 miliseconds
                    if cv2.waitKey(100) & 0xFF == ord('q'):
                        break
                    # break if the sample number is morethan 60
                    elif sampleNum > 1:
                        break
                    
                
                cam.release()
                cv2.destroyAllWindows()
                res = "Images Saved for Name : " + name + " with ID  " + Id
                print(res)
                print(' Images save location is TrainingImage\ ')
              
                
            else:
                if(name.isalpha()):
                    print('Enter Proper Id')
                else:
                    print('Enter Proper Id and Name')

        img=PhotoImage(file='E:\\Project\\sign.png')
        Label(dashboard,image=img,border=0,bg='white').place(x=125,y=90)
        
        frame=Frame(dashboard,width=350,height=500,bg='#fff')
        frame.place(x=600,y=0)

        heading=Label(frame,text='Sign Up',fg="#57a1f8",bg='white',font=('Microsoft Yahei UI Light',23,'bold'))
        heading.place(x=100,y=5)
        #username Column______________________________________________________________
        def on_enter(e):
            user.delete(0,'end')
        def on_leave(e):
            if user.get()=='':
                user.insert(0,'Name')

                    
        user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        user.place(x=30,y=80)
        user.insert(0,'Name')
        user.bind("<FocusIn>",on_enter)
        user.bind("<FocusOut>",on_leave)

        Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)
            #Id Number______________________________________________________________
        def otp():
            def verify():
                print(OTP1)
                
                b=otp1.get()
                print(b)
                if(OTP1==b):
                    Label(frame,text='Email verified',fg="red",bg='white',font=('Microsoft Yahei UI Light',7,'bold')).place(x=250,y=380)
                 
                else:
                  
                    heading=Label(frame,text='Invalid OTP',fg="red",bg='white',font=('Microsoft Yahei UI Light',7,'bold')).place(x=250,y=380)
                    
                 
            OTP1=str(random.randint(1000,9999))
            s=smtplib.SMTP_SSL("smtp.gmail.com",465)
            s.login('vaibhavvpatill@gmail.com',"gnssmfzqnbdssmzq")
            send_to=conform_code.get()
            s.sendmail('vaibhavvpatill@gmail.com',send_to,OTP1)
            def on_enter(e):
                otp1.delete(0,'end')
            def on_leave(e):
                if otp1.get()=='':
                    otp1.insert(0,'Enter OTP')
                     
            otp1=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
            otp1.place(x=30,y=340)
            otp1.insert(0,'Enter OTP')
            otp1.bind("<FocusIn>",on_enter)
            otp1.bind("<FocusOut>",on_leave)
            Frame(frame,width=295,height=2,bg='black').place(x=25,y=370)
          
            Button(frame,width=9,pady=5,text='Submit',bg='#57a1f8',fg='white',border=0,command=verify).place(x=250,y=335)
            
            
         
        def on_enter(e):
            conform_code.delete(0,'end')
        def on_leave(e):
            if conform_code.get()=='':
                conform_code.insert(0,'Email-ID')

                    
        conform_code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        conform_code.place(x=30,y=290)
        conform_code.insert(0,'Email-ID')
        conform_code.bind("<FocusIn>",on_enter)
        conform_code.bind("<FocusOut>",on_leave)

        Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)
        Button(frame,width=9,pady=5,text='Send Otp',bg='#57a1f8',fg='white',border=0,command=otp).place(x=250,y=285)

            #Mobile No.______________________________________________________________
        def on_enter(e):
            code.delete(0,'end')
        def on_leave(e):
            if code.get()=='':
                code.insert(0,'Mobile Number')

                    
        code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        code.place(x=30,y=220)
        code.insert(0,'Mobile Number')
        code.bind("<FocusIn>",on_enter)
        code.bind("<FocusOut>",on_leave)
       

        Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

        #Email iD______________________________________________________________

        def on_enter(e):
            email.delete(0,'end')
        def on_leave(e):
            if email.get()=='':
                email.insert(0,'ID Number')

                    
        email=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        email.place(x=30,y=150)
        email.insert(0,'ID Number')
        email.bind("<FocusIn>",on_enter)
        email.bind("<FocusOut>",on_leave)

        Frame(frame,width=295,height=2,bg='black').place(x=25,y=317)

            #signup button___________________________________
        for widget in footer.winfo_children():
            widget.destroy()
        a1frame=Frame(footer,bg='white')
        a1frame.place(x=0,y=0,width=1080,height=85)
        Button(a1frame,width=39,pady=5,text='Take Face ID',bg='#57a1f8',fg='white',border=0,command=TakeImages).place(x=635,y=0)
        Button(a1frame,width=125,pady=7,text='Sign up',bg='#57a1f8',fg='white',border=0,command=signup).place(x=100,y=35)
        Label(frame,width=39,pady=7,text='*Please Insert A Integer',bg='white',fg='Red',border=0).place(x=120,y=180)

        dashboard.mainloop()
        

    ##############__________________________________


    img=PhotoImage(file='E:\\Project\\login.png')
    Label(dashboard,image=img,bg='white').place(x=125,y=50)
        
    
    frame=Frame(dashboard,width=350,height=350,bg='white')
    frame.place(x=600,y=70)

    heading=Label(frame,text='Sign in',fg='#57a1f8',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
    heading.place(x=100,y=5)

    #username_____________________________
    def on_enter(e):
        user.delete(0,'end')

    def on_leave(e):
        name=user.get()
        if name=='':
            user.insert(0,'Username')

            
    user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
    user.place(x=30,y=80)
    user.insert(0,'Username')
    user.bind('<FocusIn>',on_enter)
    user.bind('<FocusOut>',on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)
    #password_____________________________
    def on_enter(e):
        code.delete(0,'end')

    def on_leave(e):
        name=code.get()
        if name=='':
            code.insert(0,'ID_Number')
    code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
    code.place(x=30,y=150)
    code.insert(0,'ID_Number')
    code.bind('<FocusIn>',on_enter)
    code.bind('<FocusOut>',on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)
    for widget in footer.winfo_children():
        widget.destroy()
    a1frame=Frame(footer,bg='white')
    a1frame.place(x=0,y=0,width=1080,height=85)
    #button___________________________________
    Button(frame,width=39,pady=7,text='Sign in',bg='#57a1f8',fg='white',border=0,command=signin).place(x=35,y=204)
    label=Label(frame,text="Don't have an account ?",fg='black',bg='white',font=('Microsoft Yahei UI Light',9))
    label.place(x=75,y=300)
    Button(frame,width=39,pady=7,text='Login with Face ID',bg='#57a1f8',fg='white',border=0,command=DetectFace).place(x=35,y=250)
    sign_up=Button(frame,width=6,text='Sign up',border=0,bg='white',cursor='hand2',fg='#57a1f8',command=signup_command)
    sign_up.place(x=215,y=300)


    root.mainloop()

def draw_student():
 
    def draw_company_list():
        def company():
            
            def search():
                option = dropdown.get()
                search_input = searchInput.get()
                db = mysql.connector.connect(host="localhost", user="root", password="", database="kbp")
                mycursor = db.cursor()
                if search_input == "":
                    mycursor.execute("SELECT * FROM company_list")
                elif option == "Name":
                    mycursor.execute("SELECT * FROM company_list WHERE name = '" + str(search_input).upper() + "'")
                elif option == "Year":
                    mycursor.execute("SELECT * FROM company_list WHERE year LIKE '%" + str(search_input).upper() + "%'")
                elif option == "Department":
                    mycursor.execute("SELECT * FROM company_list WHERE dept lIKE '%" + str(search_input).upper() + "%'")
                else:
                    return
                rows = mycursor.fetchall()
                data_table.delete(*data_table.get_children())
                if rows == None:
                    note_text['text'] = "Data: 0 Rows"
                    return 
                note_text['text'] = "Data: "+str(len(rows))+" Rows"
                for row in rows:
                    data_table.insert('', END, values=row)
                db.commit()
                db.close()

            # IT WILL GET DATA IN LEFTBOX (getdata made events there and fecth value there also)
            def getdata(event):
                currow = data_table.focus()
                contents = data_table.item(currow)
                row = contents['values']

                NameEntry.configure(state='normal')
                NameEntry.delete(0, END)
                YearEntry.delete("1.0", "end")
                DepartmentEntry.delete("1.0", "end")
                NameEntry.insert(0, row[0])
                NameEntry.configure(state='readonly')
                YearEntry.insert(END, row[2])
                DepartmentEntry.insert(END, row[1])
              

            #Header
            
            for widget in footer.winfo_children():
                widget.destroy()
            # LEFT BOX
            leftbox=Frame(dashboard,bd=0,bg="brown")
            leftbox.place(x=0,y=50,width=600,height=350)

            # INSIDE LEFT BOX
            leftbox_title=Label(leftbox,text="Company List",font=("Helvetica",20,"bold"),fg="#eae2b7",bg="brown")
            leftbox_title.place(x=10, y=30, width=  500)
            NameLabel=Label(leftbox,text="Company Name",font=("Helvetica",15),fg="#eae2b7",bg="brown")
            NameLabel.place(x=10, y =90)
            NameEntry=Entry(leftbox,font=("Helvetica",15),bd=0)
            NameEntry.place(x=160, y =90, width = 317)
            YearLabel=Label(leftbox,text="Year",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
            YearLabel.place(x=10, y=140)
            scrolly=Scrollbar(leftbox,orient=VERTICAL)
            YearEntry=Text(leftbox, font=("Helvetica", 15),bd=0, yscrollcommand=scrolly.set)
            scrolly.config(command=YearEntry.yview)
            YearEntry.place(x=160, y=140, width = 300, height = 70)
            scrolly.place(x=460, y=140, height = 70)
            DepartmentLabel=Label(leftbox,text="Department",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
            DepartmentLabel.place(x=10, y=230)
            scrolly=Scrollbar(leftbox,orient=VERTICAL)
            DepartmentEntry=Text(leftbox, font=("Helvetica", 15),bd=0, yscrollcommand=scrolly.set)
            scrolly.config(command=DepartmentEntry.yview)
            DepartmentEntry.place(x=160, y=235, width = 300, height = 70)
            scrolly.place(x=460, y=235, height = 70)

            # RIGHT BOX
            rightbox=Frame(dashboard,bd=0,bg="indianred")
            rightbox.place(x=600,y=50,width=500,height=350)

            # RIGHT BOX HEADING
            searchInput=Entry(rightbox,font=("Helvetica", 12),bd=0,width=17)
            searchInput.place(x=10, y=10, height = 30)
            dropdown=ttk.Combobox(rightbox,font=("Helvetica",10),state='readonly', width = 10)
            dropdown['values']=("--Search By--", "Name", "Year", "Department")
            dropdown.current(0)
            dropdown.place(x=180, y=10, height = 30)
            searchBtn=Button(rightbox,text="Search",command=search,font=("Helvetica", 12),width=10, bd = 0)
            searchBtn.place(x=280, y=10, height = 30)

            # BOX INSIDE RIGHT BOX
            tabfrm=Frame(rightbox,bd=4,relief=RIDGE,bg="lightblue")
            tabfrm.place(x=10,y=50,width=370,height=270)
            scrolly=Scrollbar(tabfrm,orient=VERTICAL)
            data_table=ttk.Treeview(tabfrm,columns=("name","department", "year"),yscrollcommand=scrolly.set)
            scrolly.pack(side=RIGHT,fill=Y)
            scrolly.config(command=data_table.yview)

            note_text=Label(rightbox,font=("Helvetica", 10),bg="indianred",fg="white")
            note_text.place(x=10, y=325)

            # INSIDE RIGHT BOX
            data_table.heading("name",text="Name")
            data_table.heading("year",text="Year")
            data_table.heading("department",text="Department")
            data_table['show']="headings"
            data_table.column("name",width = 10)
            data_table.column("year",width=50)
            data_table.column("department",width=30)
            data_table.pack(fill=BOTH,expand=1)
            data_table.bind("<ButtonRelease-1>",getdata)

            search()


        company()

        
    


    
    for widget in dashboard.winfo_children():
        widget.destroy()
    footer=Frame(root, bg="brown", bd=0)
    footer.place(x=0,y=565,width=1080,height=85)
    frame=Frame(dashboard, bg="#fbb1bd")
    frame.place(x=0,y=115,width=1080,height=50)
    image1 = Image.open("media/kbp.jpg")
    im1 = image1.filter(ImageFilter.BLUR)
    test = ImageTk.PhotoImage(im1)
    label1 = Label(dashboard,image=test)
    label1.photo = test
    label1.place(x=0, y=0, height = 400, width = 1080)
    option= Button(dashboard, text ="View Fees", command=draw_visitor_fees, bd =0, font=("Helvetica",11),fg='#0097e8',activeforeground='#0097e8')
    option.place(x=0, y=0, width = 400, height = 50)
    
   
    option= Button(dashboard, text ="Notice Board", command=draw_notice_board, bd =0, font=("Helvetica",11),fg='#0097e8',activeforeground='#0097e8')
    option.place(x=350, y=0, width = 400, height = 50)
 
    option= Button(dashboard, text ="View Companies List", command=draw_company_list, bd =0, font=("Helvetica",11),fg='#0097e8',activeforeground='#0097e8')
    option.place(x=700, y=0, width = 400, height = 50)
   
    
def student():
    for widget in dashboard.winfo_children():
        widget.destroy()

    def DetectFace():
        df = pd.read_csv('student Profile.csv')
        df.sort_values('Ids', inplace = True)
        df.drop_duplicates(subset = 'Ids', keep = 'first', inplace = True)
        df.to_csv('student Profile.csv', index = False)
        Name=user.get() 
        ID_Number= code.get()
        #print(OTP1)
        name , Id = '',''
        dic = {
            'Name' : Name,
            'Ids' : ID_Number
        }
        def store_data():
            global name,Id,dic
            name = Name
                   
            Id  = ID_Number
                   
            dic = {
                'Ids' : ID_Number,
                'Name': Name
            }
            c = dic
            return  c
        reader = csv.DictReader(open('student Profile.csv'))
        print('Detecting Login Face')
        for rows in reader:
            result = dict(rows)
            a=int(result['Ids'])
            if a <10000:
                name1 = result['Name']
                

            
        
        recognizer = cv2.face.LBPHFaceRecognizer_create()  #cv2.createLBPHFaceRecognizer()
        recognizer.read("TrainData\Trainner.yml")
        harcascadePath = 'C:\\Users\\vaibh\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml '
        faceCascade = cv2.CascadeClassifier(harcascadePath);
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        Face_Id = ''
        name2 = ''

        # Camera ON Everytime
        while True:
            ret, frame = cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.3, 5)
            Face_Id = 'Not detected'

            # Drawing a rectagle around the face 
            for (x, y, w, h) in faces:
                Face_Id = 'Not detected'
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
                if (confidence < 90):
                    if (Id <100):
                        name = name1
                    Predicted_name = str(name)
                    Face_Id = Predicted_name
                    print(name)
                    
                else:
                    Predicted_name = 'Unknown'
                    Face_Id = Predicted_name
                    # Here unknown faces detected will be stored
                    noOfFile = len(os.listdir("UnknownFaces")) + 1
                    if int(noOfFile) < 100:
                        cv2.imwrite("UnknownFaces\Image" + str(noOfFile) + ".jpg", frame[y:y + h, x:x + w])
                    
                    else:
                        pass


                cv2.putText(frame, str(Predicted_name), (x, y + h), font, 1, (255, 255, 255), 2)
                
            cv2.imshow('Picture', frame)
            #print(Face_Id)
            cv2.waitKey(1)

            # Checking if the face matches for Login
            if Face_Id == name1 or name2 and Face_Id != 'Unknown' :
                mydate = datetime.datetime.now()
                
                date = datetime.datetime.strftime(mydate, '%d, %m, %Y')
                time = datetime.datetime.strftime(mydate, '%H, %M, %S')
                d={'Name':Face_Id,'Ids':Id,'Date':date,'Time':time}
                with open('student attendance.csv','a+') as f:
                    fields = ['Name','Ids','Date','Time']   
                    writer=csv.DictWriter(f,fieldnames=fields)

                    writer.writerow(d)
                messagebox.showinfo("LOGIN","login succesfull!!" )
                cv2.destroyAllWindows()
                draw_student()
                
                
                break
                
            elif Face_Id == 'Not detected':
                print("-----Face Not Detected, Try again------")
                pass
            else:
                print('-----------Login failed please try agian-------')
            
            
            if (cv2.waitKey(1) == ord('q')):
               break
            
            
        def DetectFace():
            root.destroy()
       


    def signin():
        Name=user.get()
        ID_Number=code.get()
        name , Id = '',''
        dic = {
            'Name' : Name,
            'Ids' : ID_Number
        }
        def store_data(signin):
            global name,Id,dic
            name = Name
           
            Id  = ID_Number
           
            dic = {
                'Ids' : ID_Number,
                'Name': Name
            }
            c = dic
            return  c
        db = mysql.connector.connect(host="localhost", user="root", password="", database="KBP")
        mycursor=db.cursor()
        
        if Name == "" and ID_Number == "":
            print(1)
            messagebox.showinfo("Invalid","Both The Fields Are Empty!!" )
        elif Name == "" or ID_Number == " ":
               messagebox.showinfo("Invalid","Any Field Is Empty Please Filed It!!" )
        else:
            print(ID_Number)
            query = "SELECT * FROM student WHERE Name = %(name)s AND ID_Number = %(id_number)s"
            params = {'name': Name, 'id_number': ID_Number}
            mycursor.execute(query, params)
 
        print(params)    
        result=mycursor.fetchall()
        print(result)
        
        if result=="":
            print(3)
            messagebox.showinfo("Invalid","Invalid username or password!!" )
        else :
            if result:
    
                for row in result:
                     name, id_number, other_column1, other_column2 = row
                     print(f"Name: {name}, ID_Number: {id_number}, Other_Column1: {other_column1}, Other_Column2: {other_column2}")
                print(4)
                mydate = datetime.datetime.now()  
                date = datetime.datetime.strftime(mydate, '%d, %m, %Y')
                time = datetime.datetime.strftime(mydate, '%H, %M, %S')
                d={'Name':Name,'Ids':ID_Number,'Date':date,'Time':time}
                with open('student attendance.csv','a+') as f:
                    fields = ['Name','Ids','Date','Time']
                    writer=csv.DictWriter(f,fieldnames=fields)
                    writer.writerow(d)
                messagebox.showinfo("LOGIN","login succesfull!!" )
                draw_admin()
            
        def signin():
            root.destroy()
       

            
    ###########________________________________________sign up code
    def signup_command():
       # window = Toplevel()
       # window.title("SignUp")
       # window.geometry('925x600+300+200')
       # window.config(bg='#fff')
      #  window.resizable(False,False)
    
        for widget in dashboard.winfo_children():
            widget.destroy()
        def signup():
            Name=user.get() 
            Mobile_Number=code.get()
            Emailid=conform_code.get()
            ID_Number=email.get()
            #print(OTP1)
            name , Id = '',''
            dic = {
                'Name' : Name,
                'Ids' : ID_Number
            }
            def store_data():
                global name,Id,dic
                name = Name
                   
                Id  = ID_Number
                   
                dic = {
                    'Ids' : ID_Number,
                    'Name': Name
                }
                c = dic
                return  c
            x=len(Mobile_Number)
            if Name=="" or Mobile_Number=="" or Emailid=="" or ID_Number=="":
                messagebox.showinfo("Insert Status","All Fileds are required")
                
            elif (x!=10):
                Label(frame,width=39,pady=7,text='*Invalid Number',bg='white',fg='Red',border=0).place(x=130,y=250)
            else:
                db=mysql.connector.connect(host="localhost",user="root",password="",database="KBP")
                mycursor=db.cursor()
                mycursor.execute("INSERT INTO student (Name,ID_Number,Mobile_Number,Emailid) VALUES ('"+str(Name)+"', '"+str(ID_Number).upper()+"', '"+str(Mobile_Number).upper()+"', '"+str(Emailid).upper()+"')")
                db.commit()
                
                db.close();
                def getImagesAndLabels(path):
                    # Get the path of all the files in the folder
                    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

                    # Create empth face list
                    faces = []
                    # Create empty ID list
                    Ids = []
                    # Looping through all the image paths and loading the Ids and the images
                    for imagePath in imagePaths:
                        # Loading the image and converting it to gray scale
                        pilImage = Image.open(imagePath).convert('L')
                        # Now we are converting the PIL image into numpy array
                        imageNp = np.array(pilImage, 'uint8')
                        # getting the Id from the image
                        Id = int(os.path.split(imagePath)[-1].split(".")[1])
                        # extract the face from the training image sample
                        faces.append(imageNp)
                        
                        Ids.append(Id)
                    return faces, Ids

                # Train image using LBPHFFace recognizer 
                recognizer = cv2.face.LBPHFaceRecognizer_create()  # recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
                harcascadePath = 'C:\\Users\\vaibh\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml '
                detector = cv2.CascadeClassifier(harcascadePath)
                faces , Id= getImagesAndLabels("C:\\Users\\vaibh\\Desktop\\College-Management-System-using-Python-and-Tkinter-main\\College-Management-System-using-Python-and-Tkinter-main\\TrainingImage")
                recognizer.train(faces, np.array(Id))
                #store data in file 
                recognizer.save("TrainData\Trainner.yml")
                res = "Image Trained and data stored in TrainData\Trainner.yml "

                print(res)
                messagebox.showinfo("Registration","Registered Successfully")

           
        def TakeImages():
            Name=user.get() 
            ID_Number=email.get()
            Mobile_Number=code.get()
            Emailid=conform_code.get()
            
            #print(OTP1)
            name , Id,mobileno,emailid = '','','',''
            dic = {
                'Name' : Name,
                'Ids' : ID_Number,
                'Mobile Number':Mobile_Number,
                'Email-Id':Emailid
            }
            def store_data():
                global name,Id,dic
                name = Name
                mobileno = Mobile_Number
                emailid = Emailid
                Id  = ID_Number
                   
                dic = {
                    'Ids' : ID_Number,
                    'Name': Name,
                    'Mobile Number':Mobile_Number,
                    'Email-Id':Emailid
                }
                c = dic
                return  c
            dict1 = store_data()
            print(dict1)        
            if (Name.isalpha()):
                if Id == '1':
                    fieldnames = ['Name','Ids','Mobile Number','Email-Id']
                    with open('student Profile.csv','w') as f:
                        writer = csv.DictWriter(f, fieldnames =fieldnames)
                        writer.writerow(dict1)
                else:
                    fieldnames = ['Name','Ids','Mobile Number','Email-Id']
                    with open('student Profile.csv','a') as f:
                        writer = csv.DictWriter(f, fieldnames =fieldnames)
                        writer.writerow(dict1)
                cam = cv2.VideoCapture(0)

                #Haarcascade file for detctionof face
                harcascadePath = 'C:\\Users\\vaibh\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml '
                detector = cv2.CascadeClassifier(harcascadePath)
                sampleNum = 0
                while (True):
                    ret, img = cam.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = detector.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                        # Incrementing sample number
                        sampleNum = sampleNum + 1
                        # Saving the captured face in the dataset folder TrainingImage
                        cv2.imwrite("TrainingImage\ " + Name + "." + ID_Number + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                        # display the frame
                    cv2.imshow('Cpaturing Face for Login ', img)
                
                    # wait for 100 miliseconds
                    if cv2.waitKey(100) & 0xFF == ord('q'):
                        break
                    # break if the sample number is morethan 60
                    elif sampleNum > 1:
                        break
                    
                
                cam.release()
                cv2.destroyAllWindows()
                res = "Images Saved for Name : " + name + " with ID  " + Id
                print(res)
                print(' Images save location is TrainingImage\ ')
              
                
            else:
                if(name.isalpha()):
                    print('Enter Proper Id')
                else:
                    print('Enter Proper Id and Name')
            
        for widget in footer.winfo_children():
            widget.destroy()

        img=PhotoImage(file='E:\\Project\\sign.png')
        Label(dashboard,image=img,border=0,bg='white').place(x=125,y=90)
        
        frame=Frame(dashboard,width=350,height=500,bg='#fff')
        frame.place(x=600,y=0)

        heading=Label(frame,text='Sign Up',fg="#57a1f8",bg='white',font=('Microsoft Yahei UI Light',23,'bold'))
        heading.place(x=100,y=5)
        #username Column______________________________________________________________
        def on_enter(e):
            user.delete(0,'end')
        def on_leave(e):
            if user.get()=='':
                user.insert(0,'Name')

                    
        user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        user.place(x=30,y=80)
        user.insert(0,'Name')
        user.bind("<FocusIn>",on_enter)
        user.bind("<FocusOut>",on_leave)

        Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)
            #Id Number______________________________________________________________
        def otp():
            def verify():
                print(OTP1)
                
                b=otp1.get()
                print(b)
                if(OTP1==b):
                    Label(frame,text='Email verified',fg="red",bg='white',font=('Microsoft Yahei UI Light',7,'bold')).place(x=250,y=380)
                 
                else:
                  
                    heading=Label(frame,text='Invalid OTP',fg="red",bg='white',font=('Microsoft Yahei UI Light',7,'bold')).place(x=250,y=380)
                    
                 
            OTP1=str(random.randint(1000,9999))
            s=smtplib.SMTP_SSL("smtp.gmail.com",465)
            s.login('vaibhavvpatill@gmail.com',"gnssmfzqnbdssmzq")
            send_to=conform_code.get()
            s.sendmail('vaibhavvpatill@gmail.com',send_to,OTP1)
            def on_enter(e):
                otp1.delete(0,'end')
            def on_leave(e):
                if otp1.get()=='':
                    otp1.insert(0,'Enter OTP')
                     
            otp1=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
            otp1.place(x=30,y=340)
            otp1.insert(0,'Enter OTP')
            otp1.bind("<FocusIn>",on_enter)
            otp1.bind("<FocusOut>",on_leave)
            Frame(frame,width=295,height=2,bg='black').place(x=25,y=370)
          
            Button(frame,width=9,pady=5,text='Submit',bg='#57a1f8',fg='white',border=0,command=verify).place(x=250,y=335)
            
            
         
        def on_enter(e):
            conform_code.delete(0,'end')
        def on_leave(e):
            if conform_code.get()=='':
                conform_code.insert(0,'Email-ID')

                    
        conform_code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        conform_code.place(x=30,y=290)
        conform_code.insert(0,'Email-ID')
        conform_code.bind("<FocusIn>",on_enter)
        conform_code.bind("<FocusOut>",on_leave)

        Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)
        Button(frame,width=9,pady=5,text='Send Otp',bg='#57a1f8',fg='white',border=0,command=otp).place(x=250,y=285)

            #Mobile No.______________________________________________________________
        def on_enter(e):
            code.delete(0,'end')
        def on_leave(e):
            if code.get()=='':
                code.insert(0,'Mobile Number')

                    
        code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        code.place(x=30,y=220)
        code.insert(0,'Mobile Number')
        code.bind("<FocusIn>",on_enter)
        code.bind("<FocusOut>",on_leave)
       

        Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

        #Email iD______________________________________________________________

        def on_enter(e):
            email.delete(0,'end')
        def on_leave(e):
            if email.get()=='':
                email.insert(0,'ID Number')

                    
        email=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',12))
        email.place(x=30,y=150)
        email.insert(0,'ID Number')
        email.bind("<FocusIn>",on_enter)
        email.bind("<FocusOut>",on_leave)

        Frame(frame,width=295,height=2,bg='black').place(x=25,y=317)

            #signup button___________________________________
        for widget in footer.winfo_children():
            widget.destroy()
        a1frame=Frame(footer,bg='white')
        a1frame.place(x=0,y=0,width=1080,height=85)
        Button(a1frame,width=39,pady=5,text='Take Face ID',bg='#57a1f8',fg='white',border=0,command=TakeImages).place(x=635,y=0)
        Button(a1frame,width=125,pady=7,text='Sign up',bg='#57a1f8',fg='white',border=0,command=signup).place(x=100,y=35)
        Label(frame,width=39,pady=7,text='*Please Insert A Integer',bg='white',fg='Red',border=0).place(x=120,y=180)

        dashboard.mainloop()
        

    ##############__________________________________


    img=PhotoImage(file='E:\\Project\\login.png')
    Label(dashboard,image=img,bg='white').place(x=125,y=50)
        
    
    frame=Frame(dashboard,width=350,height=350,bg='white')
    frame.place(x=600,y=70)

    heading=Label(frame,text='Sign in',fg='#57a1f8',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
    heading.place(x=100,y=5)

    #username_____________________________
    def on_enter(e):
        user.delete(0,'end')

    def on_leave(e):
        name=user.get()
        if name=='':
            user.insert(0,'Username')

            
    user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
    user.place(x=30,y=80)
    user.insert(0,'Username')
    user.bind('<FocusIn>',on_enter)
    user.bind('<FocusOut>',on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)
    #password_____________________________
    def on_enter(e):
        code.delete(0,'end')

    def on_leave(e):
        name=code.get()
        if name=='':
            code.insert(0,'ID_Number')
    code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
    code.place(x=30,y=150)
    code.insert(0,'ID_Number')
    code.bind('<FocusIn>',on_enter)
    code.bind('<FocusOut>',on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)
    for widget in footer.winfo_children():
        widget.destroy()
    a1frame=Frame(footer,bg='white')
    a1frame.place(x=0,y=0,width=1080,height=85)
    #button___________________________________
    Button(frame,width=39,pady=7,text='Sign in',bg='#57a1f8',fg='white',border=0,command=signin).place(x=35,y=204)
    label=Label(frame,text="Don't have an account ?",fg='black',bg='white',font=('Microsoft Yahei UI Light',9))
    label.place(x=75,y=300)
    Button(frame,width=39,pady=7,text='Login with Face ID',bg='#57a1f8',fg='white',border=0,command=DetectFace).place(x=35,y=250)
    sign_up=Button(frame,width=6,text='Sign up',border=0,bg='white',cursor='hand2',fg='#57a1f8',command=signup_command)
    sign_up.place(x=215,y=300)


    root.mainloop()

def draw_login_page():
    def home():
        
        draw_visitor()

    for widget in dashboard.winfo_children():
        widget.destroy()
    # newWindow.attributes('-alpha',0.9)
    
    header=Frame(dashboard, bg="white", bd=5)
    header.place(x=0,y=0,width=1080,height=400)
        #heading label
   
    img1=PhotoImage(file='C:\\Users\\vaibh\\Desktop\\College-Management-System-using-Python-and-Tkinter-main\\College-Management-System-using-Python-and-Tkinter-main\\media\\admin.png')
    Button(header,image=img1,border=0,bg='white',command=admin).place(x=50,y=70)
    img2=PhotoImage(file='C:\\Users\\vaibh\\Desktop\\College-Management-System-using-Python-and-Tkinter-main\\College-Management-System-using-Python-and-Tkinter-main\\media\\teacher.png')
    Button(header,image=img2,border=0,bg='white',command=staff).place(x=400,y=70)
    img3=PhotoImage(file='C:\\Users\\vaibh\\Desktop\\College-Management-System-using-Python-and-Tkinter-main\\College-Management-System-using-Python-and-Tkinter-main\\media\\student.png')
    Button(header,image=img3,border=0,bg='white',command=student).place(x=740,y=70)
    Label(header,text="Click To Login",border=0,font=("Helvetica",16,"bold"),bg='white',fg="blue").place(x=480,y=310)
    Button(header,text="Go TO Home Page",border=0,font=("Helvetica",16,"bold"),bg='white',fg="blue",command=home).place(x=450,y=345)
    root.mainloop()

def button_mode():
   global is_on
   #Determine it is on or off
   if is_on:
      on_.config(image=off)
      is_on = False
      draw_login_page()
      
   else:
      on_.config(image = on)
      is_on = True
      is_admin = False
      draw_visitor()
      
def draw_notice_board():
    import view_notice_board
def draw_visitor_fees():
    import visitor_fees_structure
def draw_visitor():
    
    
    for widget in dashboard.winfo_children():
        widget.destroy()
    
    footer=Frame(root, bg="brown", bd=0)
    footer.place(x=0,y=565,width=1080,height=85)
    
    welcome_text["text"] = "Welcome, Visitor"
    image1 = Image.open("media/kbp.jpg")
    test = ImageTk.PhotoImage(image1)
    label1 = Label(dashboard,image=test)
    label1.photo = test
    label1.place(x=0, y=0, height = 400, width = 1080)
    option= Button(dashboard, text ="Fee Structure", command = draw_visitor_fees, bd =0, font=("Helvetica",16), bg = "#118ab2",fg="#eae2b7")
    option.place(x=200, y=175, width = 200, height = 50)
    option= Button(dashboard, text ="Notice Board", command = draw_notice_board,bd =0, font=("Helvetica",16), bg = "#118ab2",fg="#eae2b7")
    option.place(x=700, y=175, width = 200, height = 50)
    

    
#Header
header=Frame(root, bg="brown", bd=0)
header.place(x=0,y=0,width=1080,height=115)
#logo
logo1=PhotoImage(file='./media/logo.png')
logo=Label(root,image=logo1, bg="brown")
logo.place(x=-5,y=-10)

KBP=Label(header, text="Karmaveer Bhaurao Patil College , vashi ",font=("Helvetica",36,"bold"), bg = "brown",fg="#eae2b7")
KBP.place(x=120, y=20, width=950)

#Profile frame
frame=Frame(root, bg="#fbb1bd")
frame.place(x=0,y=115,width=1080,height=50)
welcome_text = Label(frame, text = "Welcome to our Page", font=("Minion Pro Regular", 16), bg="#fbb1bd")
welcome_text.place(x=500, y=10)
is_on = True

# Define Our Images
on = PhotoImage(file ="media/on.png")
off = PhotoImage(file ="media/off.png")
# Create A Button
on_= Button(frame, image =on,bd =0, bg = "#fbb1bd", command = button_mode)
on_.place(x=950, y=0, width = 50, height = 50)
#visitor_text

admin_text = Label(frame, text = "Login", font=("Minion Pro Regular", 16), bg="#fbb1bd")
admin_text.place(x=1000, y=10)
#profile picture

dashboard=Frame(root, bg="white", bd=0)
dashboard.place(x=0,y=165,width=1080,height=400)
draw_visitor()
#Footer
footer=Frame(root, bg="brown", bd=0)
footer.place(x=0,y=565,width=1080,height=85)
root.mainloop()
