from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employees import connect_database


def delete_supplier(invoice,treeview):
    index=treeview.selection()
    if not index:
        messagebox.showerror("Error",'No Row Was Selected')
        return
    else:
        result=messagebox.askyesno('Confirm',"Do you really wanna delete the record?")
        if result:
            cursor,connection=connect_database()
            if not cursor or not connection:
                return 
            try:
                cursor.execute("use inventory")
                cursor.execute("delete from supplier_data where invoice=%s",invoice)
                connection.commit()
                treeview_data(treeview)
                messagebox.showinfo("Success","Selected Data Was Deleted")
            except Exception as e:
                messagebox.showerror("Error",f'Error due to {e}')
            finally:
                    cursor.close()
                    connection.close()



def clear(invoice_entry,name_entry,Contact_entry,address_entry,Description_text,treeview):
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    Contact_entry.delete(0,END)
    address_entry.delete(0,END)
    Description_text.delete(1.0,END)
    treeview.selection_remove(treeview.selection())

def search_supplier(search_value,treeview):
    if search_value=='':
        messagebox.showerror("Error","Please Enter The Invoive Number")
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return 
        try:
            cursor.execute("use inventory")
            cursor.execute('select * from supplier_data where invoice=%s',search_value)
            record=cursor.fetchone()
            if not record:
                messagebox.showerror("Error","No Invoice Was Found")
                return
            treeview.delete(*treeview.get_children())
            treeview.insert('',END,values=record)
        except Exception as e:
            messagebox.showerror("Error",f'Error due to {e}')
        finally:
                cursor.close()
                connection.close()


def show_all(treeview,search_entry):
    treeview_data(treeview)
    search_entry.delete(0,END)



def update_supplier(invoice,name,contact,address,description,treeview):
    index=treeview.selection()
    if not index:
        messagebox.showerror("Error",'No Row Was Selected')
        return
    cursor,connection=connect_database()
    if not cursor or not connection:
        return 
    try:
        cursor.execute("use inventory")
        cursor.execute('select * from supplier_data where invoice=%s',invoice)
        current_data=cursor.fetchone()
        current_data=current_data[1:]
        new_data=(name,contact,address,description)
        if current_data==new_data:
            messagebox.showinfo('Information',"No chnages were made")
            return
        cursor.execute('update supplier_data set name=%s, contact=%s, address=%s, description=%s where invoice=%s',(name,contact,address,description,invoice))
        connection.commit()
        messagebox.showinfo("Success","Data Was Updated Successfully")
        treeview_data(treeview)    
    except Exception as e:
        messagebox.showerror("Error",f'Error due to {e}')
    finally:
            cursor.close()
            connection.close()


def select_data(event,invoice_entry,name_entry,Contact_entry,address_entry,Description_text,treeview):
    index=treeview.selection()
    content=treeview.item(index)
    actual_content=content['values']

    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    Contact_entry.delete(0,END)
    address_entry.delete(0,END)
    Description_text.delete(1.0,END)


    invoice_entry.insert(0,actual_content[0])   
    name_entry.insert(0,actual_content[1])   
    Contact_entry.insert(0,actual_content[2])   
    address_entry.insert(0,actual_content[3])   
    Description_text.insert(1.0,actual_content[4])   

     

def treeview_data(treeview):
        cursor,connection=connect_database()
        if not cursor or not connection:
            return  
        try:
            cursor.execute("use inventory")
            cursor.execute("select * from supplier_data")
            records=cursor.fetchall()
            treeview.delete(* treeview.get_children())
            for record in records:
                treeview.insert('',END,values=record)
        except Exception as e:
            messagebox.showerror("Error",f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()
             



def add_supplier(invoice,name,contact,address,description,treeview):
    if invoice=='' or name=='' or contact=='' or address=='' or description =='':
        messagebox.showerror("Error","All Fields Are Required")
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute("use inventory")
            cursor.execute("Create table if not exists supplier_data (invoice int primary key, name varchar(50), contact varchar(15), address varchar(100), description text)")
            cursor.execute('select * from supplier_data where invoice=%s',invoice)
            if cursor.fetchone():
                messagebox.showerror("Error","Invoice Number, Already Exists!")
                return
            cursor.execute('insert into supplier_data values(%s,%s,%s,%s,%s)',(invoice,name,contact,address,description))
            connection.commit()
            messagebox.showinfo("Success","Data Was Added")
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror("Error",f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()





def supplier_form(window):
    global back_image
    supplier_frame=Frame(window,width=1070,height=567,bg="white")
    supplier_frame.place(x=250,y=98,relwidth=1, width=-250, relheight=0.85) #if problem we can change x=20,y=100
    heading_lable=Label(supplier_frame,text="Manage Supplier Details",font=("times new roman", 16,"bold"),bg="#594236",fg="white")
    heading_lable.place(x=0,y=0,relwidth=1)
    back_image=PhotoImage(file="images/back.png")
    back_button=Button(supplier_frame,image=back_image,bd=0,cursor="hand2",bg="white",command=lambda:supplier_frame.place_forget())
    back_button.place(x=10,y=30 )

    left_frame=Frame(supplier_frame,bg='white')
    left_frame.place(x=10,y=100)

    #invoice lable
    invoice_lable=Label(left_frame,text='Invoice No.',font=("new times roman",14),bg="white")
    invoice_lable.grid(row=0,column=0,padx=(20,40),sticky='w')
    invoice_entry=Entry(left_frame,font=("new times roman",12),bg="lightyellow")
    invoice_entry.grid(row=0,column=1)

    #name lable
    name_lable=Label(left_frame,text='Supplier Name',font=("new times roman",14),bg="white")
    name_lable.grid(row=1,column=0,padx=(20,40),pady=25,sticky='w')
    name_entry=Entry(left_frame,font=("new times roman",12),bg="lightyellow")
    name_entry.grid(row=1,column=1)

    #Contact lable
    Contact_lable=Label(left_frame,text='Supplier Contact',font=("new times roman",14),bg="white")
    Contact_lable.grid(row=2,column=0,padx=(20,40),sticky='w')
    Contact_entry=Entry(left_frame,font=("new times roman",12),bg="lightyellow")
    Contact_entry.grid(row=2,column=1)


    #address lable
    address_lable=Label(left_frame,text='Supplier Address',font=("new times roman",14),bg="white")
    address_lable.grid(row=3,column=0,padx=(20,40),pady=25,sticky='w')
    address_entry=Entry(left_frame,font=("new times roman",12),bg="lightyellow")
    address_entry.grid(row=3,column=1)

    #Description lable
    description_lable=Label(left_frame,text='Description',font=("new times roman",14),bg="white")
    description_lable.grid(row=4,column=0,padx=(20,40),sticky='nw',pady=25)
    Description_text=Text(left_frame,width=25,height=6,bd=1,bg='lightyellow')
    Description_text.grid(row=4,column=1,pady=25)



    #Button on the left-frame
    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=5,columnspan=2,pady=20)
    #add button
    add_button=Button(button_frame,text="ADD",font=("new times roman",12),width=8,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:add_supplier(invoice_entry.get(),name_entry.get(),Contact_entry.get(),address_entry.get(),Description_text.get(1.0,END).strip(),treeview))
    add_button.grid(row=0,column=0,padx=20)  

    #update button
    update_button=Button(button_frame,text="UPDATE",font=("new times roman",12),width=8,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:update_supplier(invoice_entry.get(),name_entry.get(),Contact_entry.get(),address_entry.get(),Description_text.get(1.0,END).strip(),treeview))
    update_button.grid(row=0,column=1)

    #delete button
    delete_button=Button(button_frame,text="DELETE",font=("new times roman",12),width=8,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:delete_supplier(invoice_entry.get(),treeview))
    delete_button.grid(row=0,column=2,padx=20)

    #clear button
    clear_button=Button(button_frame,text="CLEAR",font=("new times roman",12),width=8,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda: clear(invoice_entry,name_entry,Contact_entry,address_entry,Description_text,treeview))
    clear_button.grid(row=0,column=3)

    #Working on the right frame
    right_frame=Frame(supplier_frame,bg='white')
    right_frame.place(x=520,y=95,width=500,height=350)
    search_frame=Frame(right_frame,bg='white')
    search_frame.pack(pady=(0,20))
    #invoice lable on right side
    num_lable=Label(search_frame,text='Invoice No.',font=("new times roman",14),bg="white")
    num_lable.grid(row=0,column=0,padx=(0,15),sticky='w')
    search_entry=Entry(search_frame,font=("new times roman",12),bg="lightyellow",width=14)
    search_entry.grid(row=0,column=1)

    #search button
    search_button=Button(search_frame,text="SEARCH",font=("new times roman",12),width=8,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:search_supplier(search_entry.get(),treeview))
    search_button.grid(row=0,column=2,padx=15)

    #show_all button
    show_button=Button(search_frame,text="SHOW ALL",font=("new times roman",12),width=9,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:show_all(treeview,search_entry))
    show_button.grid(row=0,column=3)

    #treeview on right frame
    scrolly=Scrollbar(right_frame,orient=VERTICAL)
    scrollx=Scrollbar(right_frame,orient=HORIZONTAL)
    treeview=ttk.Treeview(right_frame,columns=('Invoice','Name','Contact','Address','Description'),show='headings',
                          yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH,expand=1)
    treeview.heading('Invoice',text="Invoice ID")
    treeview.heading('Name',text="Supplier Name")
    treeview.heading('Contact',text="Supplier Contact")
    treeview.heading('Address',text='Supplier Address')
    treeview.heading('Description',text="Description")


    treeview.column('Invoice',width=80)
    treeview.column('Name',width=140)
    treeview.column('Contact',width=140)
    treeview.column('Address',width=150)
    treeview.column('Description',width=140)

    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',lambda event:select_data(event,invoice_entry,name_entry,Contact_entry,address_entry,Description_text,treeview))
    return supplier_frame
