from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import date
from typing import Any
from db import connect_database

# Module-level references for static analysis and runtime safety
employee_treeview: Any = None
back_image: Any = None

def create_database_table():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute("create table if not exists Employee_Data (empid INT PRIMARY KEY, name VARCHAR(75), farmrole VARCHAR(100), gender VARCHAR(15), dob VARCHAR(10), contact varchar(20), employement_type VARCHAR(50), education varchar (40), work_shift VARCHAR(50), address VARCHAR(100), doj VARCHAR(30), salary NUMERIC(10,2), usertype VARCHAR(30), maincrop VARCHAR(100))")
    connection.commit()
    cursor.close()
    connection.close()

#showing all the database value on screen record
def treeview_data():
        cursor,connection=connect_database()
        if not cursor or not connection:
            return  
        cursor.execute("use inventory")
        try:  
            cursor.execute("select * from Employee_Data")
            employee_records=cursor.fetchall()
            if employee_treeview is not None:
                employee_treeview.delete(*employee_treeview.get_children())
                for record in employee_records:
                    employee_treeview.insert('',END,values=record)
        except Exception as e:
            messagebox.showerror("Error",f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()


#Selecting all the datavalue
def select_data(event,empid_entry, name_entry, farm_role_entry, dob_date_entry, gender_combobox, contact_entry, employement_combobox, education_combobox, workshift_combobox, address_text, doj_date_entry, Salary_entry, usertype_combobox, main_crop_entry):
    if employee_treeview is None:
        return
    index=employee_treeview.selection()
    content=employee_treeview.item(index)
    row=content['values']
    clear_fields(empid_entry, name_entry, farm_role_entry, dob_date_entry, gender_combobox, contact_entry, employement_combobox, education_combobox, workshift_combobox, address_text, doj_date_entry, Salary_entry, usertype_combobox, main_crop_entry,False)
    empid_entry.insert(0, row[0])
    name_entry.insert(0, row[1])
    farm_role_entry.insert(0, row[2])
    gender_combobox.set(row[3])
    dob_date_entry.set_date(row[4])
    contact_entry.insert(0, row[5])
    employement_combobox.set(row[6])
    education_combobox.set(row[7])
    workshift_combobox.set(row[8])
    address_text.insert(1.0, row[9])
    doj_date_entry.set_date(row[10])
    Salary_entry.insert(0,row[11])
    usertype_combobox.set(row[12])
    main_crop_entry.insert(0,row[13])


#Adding emplyee
def add_employee(empid,name,farmrole,gender,dob,contact,employement_type,education,work_shift,address,doj,salary,usertype,maincrop):
    if (empid=='' or name=='' or farmrole=='' or gender=="Select Gender" or contact=='' or employement_type=="select type" or education=="select type" or work_shift=="select type" or address=="/n" or
        salary==''or usertype=='' or maincrop==""):
        messagebox.showerror("Error","ALL these field are required")
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute("use inventory")
        try:
            cursor.execute("select empid from Employee_Data where empid=%s",(empid))
            if cursor.fetchone():
                messagebox.showerror("Error","Id Already Exists")
                return
            address=address.strip()
            cursor.execute(""" INSERT INTO Employee_Data (empid, name, farmrole, contact, gender, dob, employement_type, education, work_shift, address, doj, salary, usertype, maincrop) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """, (int(empid), name, farmrole, contact, gender, dob, employement_type, education, work_shift, address, doj, salary, usertype, maincrop))
            connection.commit()
            treeview_data()
            messagebox.showinfo("success","Data is inserted successfully")
        except Exception as e:
            messagebox.showerror("Error",f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()



#Clearing all the input values on the employee page

def clear_fields(empid_entry, name_entry, farm_role_entry, dob_date_entry, gender_combobox, contact_entry, employement_combobox, education_combobox, workshift_combobox, address_text, doj_date_entry, Salary_entry, usertype_combobox, main_crop_entry,check):
    empid_entry.delete(0,END)
    name_entry.delete(0,END)
    farm_role_entry.delete(0,END)
    dob_date_entry.set_date(date.today())
    gender_combobox.set('Select Gender')
    contact_entry.delete(0,END)
    employement_combobox.set('Select Type')
    education_combobox.set('Select Education')
    workshift_combobox.set('Select Shift')
    address_text.delete(1.0,END)
    doj_date_entry.set_date(date.today())
    Salary_entry.delete(0,END)
    usertype_combobox.set('Select User Type')
    main_crop_entry.delete(0,END)
    if check and employee_treeview is not None:
        employee_treeview.selection_remove(employee_treeview.selection())


#Updating employee information

def update_employee(empid,name,farmrole,gender,dob,contact,employement_type,education,work_shift,address,doj,salary,usertype,maincrop):
    if employee_treeview is None:
        return
    selected=employee_treeview.selection()
    if not selected:
        messagebox.showerror("Error","No row was selected")
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return  
        try:
            cursor.execute("use inventory")
            cursor.execute('select * from Employee_Data where empid=%s',(empid,))
            current_data=cursor.fetchone()
            current_data=current_data[1:]
            address=address.strip()
            new_data=(name,farmrole,gender,dob,contact,employement_type,education,work_shift,address,doj,salary,usertype,maincrop)
            if current_data==new_data:
                messagebox.showinfo("Information","No changes dectected")
                return

            cursor.execute('update Employee_Data set name=%s, farmrole=%s, gender=%s, dob=%s, contact=%s, employement_type=%s, education=%s, work_shift=%s, address=%s, doj=%s, salary=%s, usertype=%s, maincrop=%s where empid=%s',(name,farmrole,gender,dob,contact,employement_type,education,work_shift,address,doj,salary,usertype,maincrop,empid))
            connection.commit()
            treeview_data()
            messagebox.showinfo("Success","Data is updated successfully")

        except Exception as e:
            messagebox.showerror("Error",f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

#Deleting employee information
def delete_employee(empid):
    if employee_treeview is None:
        return
    selected=employee_treeview.selection()
    if not selected:
        messagebox.showerror("Error","No row was selected")
    else:
        result=messagebox.askyesno('Confirm',"Do you really wanna delete the record?")
        if result:
            cursor,connection=connect_database()
            if not cursor or not connection:
                return  
            try:
                cursor.execute("use inventory")
                cursor.execute('Delete from Employee_Data where empid=%s',(empid,))
                connection.commit()
                treeview_data()
                messagebox.showinfo("Success","Record was deleted")
            except Exception as e:
                messagebox.showerror("Error",f'Error due to {e}')
            finally:
                cursor.close()
                connection.close()           


#searching employee
def search_employee(search_option,value):
    if search_option=='Search By':
        messagebox.showerror("Error","No option is selected")
    elif value=="":
        messagebox.showerror("Error","No value is selected")
    else:
            cursor,connection=connect_database()
            if not cursor or not connection:
                return  
            try:
                cursor.execute("use inventory")
                cursor.execute(f'select * from Employee_Data where {search_option} LIKE %s',(f'%{value}%',))
                records=cursor.fetchall()
                if employee_treeview is not None:
                    employee_treeview.delete(*employee_treeview.get_children())
                    for record in records:
                        employee_treeview.insert('',END,values=record)
            except Exception as e:
                messagebox.showerror("Error",f'Error due to {e}')
            finally:
                cursor.close()
                connection.close() 

#showing all button functionality

def show_all(search_entry,search_combobox):
    treeview_data()
    search_entry.delete(0,END)
    search_combobox.set('Search By')



#Employee details
def employee_form(window):
    global back_image,employee_treeview
    employee_frame=Frame(window,width=1070,height=567,bg="white")
    employee_frame.place(x=250,y=98,relwidth=1, width=-250, relheight=0.85) #if problem we can change x=20,y=100
    heading_lable=Label(employee_frame,text="Manage Employee Details",font=("times new roman", 16,"bold"),bg="#594236",fg="white")
    heading_lable.place(x=0,y=0,relwidth=1)

    back_image=PhotoImage(file="images/back.png")


    top_frame=Frame(employee_frame,bg="white")
    top_frame.place(x=0,y=40,relwidth=1,height=235)

    back_button=Button(top_frame,image=back_image,bd=0,cursor="hand2",bg="white",command=lambda:employee_frame.place_forget())
    back_button.place(x=10,y=0 )
    search_frame=Frame(top_frame,bg="white")
    search_frame.pack()
    search_combobox=ttk.Combobox(search_frame,values=("Empid",'Name','Farmrole',"Gender",'Dob','Contact','Employement_type',
                                                     'Education','Work_shift','Address','DOJ','Salary','Usertype',"Maincrop"),font=("new times roman",12),state="readonly")
    search_combobox.set("Search By")
    search_combobox.grid(row=0,column=0,padx=20)

    search_entry=Entry(search_frame,font=("new times roman",12),bg="lightyellow")
    search_entry.grid(row=0,column=1)

    search_button=Button(search_frame,text="Search",font=("new times roman",12),width=10,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:search_employee(search_combobox.get(),search_entry.get()))
    search_button.grid(row=0,column=2,padx=20)

    show_button=Button(search_frame,text="Show all",font=("new times roman",12),width=10,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:show_all(search_entry,search_combobox))
    show_button.grid(row=0,column=3)


    horizontal_scrollbar=Scrollbar(top_frame,orient=HORIZONTAL)
    vertical_scrollbar=Scrollbar(top_frame,orient=VERTICAL)

    employee_treeview=ttk.Treeview(top_frame,columns=("empid",'name','farmrole',"gender",'dob','contact',
                                                      'employement_type','education','work_shift','address',
                                                      'doj','salary','usertype',"maincrop"),
                                                      show="headings",
                                                      yscrollcommand=vertical_scrollbar.set,xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM,fill=X)
    vertical_scrollbar.pack(side=RIGHT,fill=Y,pady=(10,0))

    horizontal_scrollbar.config(command=employee_treeview.xview)
    vertical_scrollbar.config(command=employee_treeview.yview)
    employee_treeview.pack(pady=(10,0))

    
    employee_treeview.heading("empid",text="EMPID")
    employee_treeview.heading("name",text="NAME")
    employee_treeview.heading("farmrole",text="FARMROLE")
    employee_treeview.heading("contact",text="CONTACT")
    employee_treeview.heading("gender",text="GENDER")
    employee_treeview.heading("dob",text="DOB")
    employee_treeview.heading("employement_type",text="EMPLOYMENT TYPE")
    employee_treeview.heading("education",text="EDUCATION")
    employee_treeview.heading("work_shift",text="WORK SHIFT")
    employee_treeview.heading("address",text="ADDRESS")
    employee_treeview.heading("doj",text="JOINING DATE")
    employee_treeview.heading("salary",text="SALARY")
    employee_treeview.heading("usertype",text="USER TYPE")
    employee_treeview.heading("maincrop",text="MAINCROP")
    
    employee_treeview.column('empid',width=60)
    employee_treeview.column('name', width=140)
    employee_treeview.column('farmrole', width=180)
    employee_treeview.column('gender', width=80)
    employee_treeview.column('contact', width=100)
    employee_treeview.column('dob', width=100)
    employee_treeview.column('employement_type', width=120)
    employee_treeview.column('education', width=120)
    employee_treeview.column('work_shift', width=100)
    employee_treeview.column('address', width=200)
    employee_treeview.column('doj', width=100)
    employee_treeview.column('salary', width=140)
    employee_treeview.column('usertype', width=120)
    employee_treeview.column("maincrop",width=120)

    treeview_data()

    #detail frame section

    detail_frame=Frame(employee_frame,bg="white")
    detail_frame.place(x=0,y=280)

    #empid
    empid_lable=Label(detail_frame,text="EmpId",font=("new times roman",12),bg="white")
    empid_lable.grid(row=0,column=0,pady=10,padx=20,sticky="w")
    empid_entry=Entry(detail_frame,font=("new times roman",12),bg="lightyellow")
    empid_entry.grid(row=0,column=1,pady=10,padx=20)

    # name
    name_lable=Label(detail_frame,text="Name",font=("new times roman",12),bg="white")
    name_lable.grid(row=0,column=2,pady=10,padx=20,sticky="w")
    name_entry=Entry(detail_frame,font=("new times roman",12),bg="lightyellow")
    name_entry.grid(row=0,column=3,pady=10,padx=20)

    # farmrole
    farm_role_lable=Label(detail_frame,text="FarmRole",font=("new times roman",12),bg="white")
    farm_role_lable.grid(row=0,column=4,pady=10,padx=20,sticky="w")
    farm_role_entry=Entry(detail_frame,font=("new times roman",12),bg="lightyellow")
    farm_role_entry.grid(row=0,column=5,pady=10,padx=20)

    # gender
    gender_lable=Label(detail_frame,text="Gender",font=("new times roman",12),bg="white")
    gender_lable.grid(row=1,column=0,pady=10,padx=20,sticky="w")
    gender_combobox=ttk.Combobox(detail_frame,values=("Male","Female"),font=("new times roman",12),width=18,state="readonly")
    gender_combobox.set("select Gender")
    gender_combobox.grid(row=1,column=1)

    # dob (Date of Birth)
    dob_lable=Label(detail_frame,text="DOB",font=("new times roman",12),bg="white")
    dob_lable.grid(row=1,column=2,pady=10,padx=20,sticky="w")
    dob_date_entry=DateEntry(detail_frame, width=18,font=("new times roman",12),state="readonly",date_pattern="dd/mm/yyyy")
    dob_date_entry.grid(row=1,column=3)

    # # contact (Phone Number)
    contact_lable=Label(detail_frame,text="Contact",font=("new times roman",12),bg="white")
    contact_lable.grid(row=1,column=4,pady=10,padx=20,sticky="w")
    contact_entry=Entry(detail_frame,font=("new times roman",12),bg="lightyellow")
    contact_entry.grid(row=1,column=5,pady=10,padx=20)

    # # employement_type
    employement_lable=Label(detail_frame,text="Employment",font=("new times roman",12),bg="white")
    employement_lable.grid(row=2,column=0,pady=10,padx=20,sticky="w")
    employement_combobox=ttk.Combobox(detail_frame,values=("Fulltime","Parttime","Contract","Seasonal","Internship"),font=("new times roman",12),width=18,state="readonly")
    employement_combobox.set("select type")
    employement_combobox.grid(row=2,column=1)  

    #education
    education_lable=Label(detail_frame,text="Education",font=("new times roman",12),bg="white")
    education_lable.grid(row=2,column=2,pady=10,padx=20,sticky="w")
    education_option=["BTECH","BCOM","DIPLOMA","ITI","Class 10","Class 12"]
    education_combobox=ttk.Combobox(detail_frame,values=education_option,font=("new times roman",12),width=18,state="readonly")
    education_combobox.set("select type")
    education_combobox.grid(row=2,column=3)  

    #Workshift
    workshift_lable=Label(detail_frame,text="WorkShift",font=("new times roman",12),bg="white")
    workshift_lable.grid(row=2,column=4,pady=10,padx=20,sticky="w")
    workshift_option=["MORNING","AFTERNOON","EVENING","NIGHT"]
    workshift_combobox=ttk.Combobox(detail_frame,values=workshift_option,font=("new times roman",12),width=18,state="readonly")
    workshift_combobox.set("select type")
    workshift_combobox.grid(row=2,column=5)  

    # # address
    address_lable=Label(detail_frame,text="Address",font=("new times roman",12),bg="white")
    address_lable.grid(row=3,column=0,pady=10,padx=20,sticky="w")
    address_text=Text(detail_frame,width=20,height=3,font=("new times roman",12),bg="lightyellow")
    address_text.grid(row=3,column=1,rowspan=2)

    # # doj (Date of Joining)
    doj_lable=Label(detail_frame,text="DOJ",font=("new times roman",12),bg="white")
    doj_lable.grid(row=3,column=2,padx=20,pady=10,sticky="w")
    doj_date_entry=DateEntry(detail_frame, width=18,font=("new times roman",12),state="readonly",date_pattern="dd/mm/yyyy")
    doj_date_entry.grid(row=3,column=3)



    #start with user type
    usertype_lable=Label(detail_frame,text="UserType",font=("new times roman",12),bg="white")
    usertype_lable.grid(row=4,column=2,pady=10,padx=20,sticky="w")
    usertype_option=["Admin","Employee"]
    usertype_combobox=ttk.Combobox(detail_frame,values=usertype_option,font=("new times roman",12),width=18,state="readonly")
    usertype_combobox.set("select Type")
    usertype_combobox.grid(row=4,column=3)  


    #Salary
    Salary_lable=Label(detail_frame,text="Salary",font=("new times roman",12),bg="white")
    Salary_lable.grid(row=3,column=4,pady=10,padx=20,sticky="w")
    Salary_entry=Entry(detail_frame,font=("new times roman",12),bg="lightyellow")
    Salary_entry.grid(row=3,column=5,pady=10,padx=20)

    #maincrop
    main_crop_lable=Label(detail_frame,text="MainCrop",font=("new times roman",12),bg="white")
    main_crop_lable.grid(row=4,column=4,pady=10,padx=20,sticky="w")
    main_crop_entry=Entry(detail_frame,font=("new times roman",12),bg="lightyellow")
    main_crop_entry.grid(row=4,column=5,pady=10,padx=20)

    #BUTTONS
    button_frame=Frame(employee_frame,bg="white")
    button_frame.place(x=200,y=520)

    #ADD BUTTON
    add_button=Button(button_frame,text="ADD",font=("new times roman",12),width=10,cursor="hand2",fg="white",bg="#0f4d7d", command=lambda:add_employee(empid_entry.get(),name_entry.get(),farm_role_entry.get(),
                                                                gender_combobox.get(),dob_date_entry.get(),contact_entry.get(),
                                                                employement_combobox.get(),education_combobox.get(),workshift_combobox.get(),
                                                                address_text.get(1.0,END),doj_date_entry.get(),Salary_entry.get(),usertype_combobox.get(),main_crop_entry.get( )))
    add_button.grid(row=0,column=0,padx=20)    


    #UPDATE BUTTON
    Update_button=Button(button_frame,text="UPDATE",font=("new times roman",12),width=10,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:update_employee(empid_entry.get(),name_entry.get(),farm_role_entry.get(),
                                                                gender_combobox.get(),dob_date_entry.get(),contact_entry.get(),
                                                                employement_combobox.get(),education_combobox.get(),workshift_combobox.get(),
                                                                address_text.get(1.0,END),doj_date_entry.get(),Salary_entry.get(),usertype_combobox.get(),main_crop_entry.get( )))
    Update_button.grid(row=0,column=1,padx=20)    

    #DELETE BUTTON
    delete_button=Button(button_frame,text="DELETE",font=("new times roman",12),width=10,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:delete_employee(empid_entry.get(),))
    delete_button.grid(row=0,column=2,padx=20)  


    #CLEAR BUTTON
    clear_button=Button(button_frame,text="CLEAR",font=("new times roman",12),width=10,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda: clear_fields(empid_entry, name_entry, farm_role_entry, dob_date_entry, gender_combobox, contact_entry, employement_combobox, education_combobox, workshift_combobox, address_text, doj_date_entry, Salary_entry, usertype_combobox, main_crop_entry,True))
    clear_button.grid(row=0,column=3,padx=20)


    
    employee_treeview.bind("<ButtonRelease-1>",lambda event:select_data(event,empid_entry, name_entry, farm_role_entry, dob_date_entry, gender_combobox, contact_entry, employement_combobox, education_combobox, workshift_combobox, address_text, doj_date_entry, Salary_entry, usertype_combobox, main_crop_entry))
    create_database_table()
    return employee_frame