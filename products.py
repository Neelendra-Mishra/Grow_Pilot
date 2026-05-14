from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employees import connect_database


def show_all(treeview,search_combobox,search_entry):
    treeview_data(treeview)
    search_combobox.set('Search By')
    search_entry.delete(0,END)


def search_product(treeview,search_combobox,search_entry):
    if search_combobox.get()=='Select By':
        messagebox.showwarning("Warning","Please Select an Option")
    elif search_entry.get()=='':
        messagebox.showwarning("Warning","Please Enter The Value")
    else:
            cursor,connection=connect_database()
            if not cursor or not connection:
                return 
            try:
                cursor.execute("use inventory")
                cursor.execute(f'select * from product_data where {search_combobox.get()}=%s',search_entry.get())
                records=cursor.fetchall()
                if len(records)==0:
                    messagebox.showerror("Error","No Record Was Found")
                    return
                treeview.delete(*treeview.get_children())
                for record in records:
                    treeview.insert('',END,values=record)
            except Exception as e:
                messagebox.showerror("Error",f'Error due to {e}')
            finally:
                    cursor.close()
                    connection.close()





def clear_fields(treeview,category_combobox,Supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox):
    treeview.selection_remove(treeview.selection())
    category_combobox.set('Select')
    Supplier_combobox.set('Select')
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    quantity_entry.delete(0,END)
    status_combobox.set('Select Status')

def delete_product(treeview,category_combobox,Supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox):
    index = treeview.selection()
    if not index:
        messagebox.showerror("Error",'No Row Was Selected')
        return
    item_id = index[0]                    
    dict = treeview.item(item_id)
    content = dict.get('values', ())
    if not content:
        messagebox.showerror("Error","No data found for selected row")
        return
    id = content[0]
    result = messagebox.askyesno('Confirm',"Do you really wanna delete the record?")
    if result:
        cursor,connection = connect_database()
        if not cursor or not connection:
            return 
        try:
            cursor.execute("use inventory")
            cursor.execute("delete from product_data where id=%s", (id,))
            connection.commit()
            treeview_data(treeview)
            messagebox.showinfo("Success","Selected Data Was Deleted")
            clear_fields(treeview,category_combobox,Supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox)
        except Exception as e:
            messagebox.showerror("Error",f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()


def update_product(category,supplier,name,price,quantity,status,treeview):
    index=treeview.selection()
    dict=treeview.item(index)
    content=dict['values']
    id=content[0]
    if not index:
        messagebox.showerror("Error",'No Row Was Selected')
        return
    cursor,connection=connect_database()
    if not cursor or not connection:
        return 
    try:
        cursor.execute("use inventory")
        cursor.execute('select * from product_data where id=%s',id)
        current_data=cursor.fetchone()
        current_data=current_data[1:]
        current_data=list(current_data)
        current_data[3]=str(current_data[3])
        current_data=tuple(current_data)
        quantity=int(quantity)
        new_data=(category,supplier,name,price,quantity,status)
        if current_data==new_data:
            messagebox.showinfo('Information',"No chnages were made")
            return
        cursor.execute('update product_data set category=%s, supplier=%s, name=%s, price=%s, quantity=%s ,status=%s where id=%s',(category,supplier,name,price,quantity,status,id))
        connection.commit()
        messagebox.showinfo("Success","Data Was Updated Successfully")
        treeview_data(treeview)    
    except Exception as e:
        messagebox.showerror("Error",f'Error due to {e}')
    finally:
            cursor.close()
            connection.close()




def select_data(event,treeview,category_combobox,Supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox):
    index=treeview.selection()
    dict=treeview.item(index)
    actual_content=dict['values']
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    quantity_entry.delete(0,END)
    category_combobox.set(actual_content[1])
    Supplier_combobox.set(actual_content[2])
    name_entry.insert(0,actual_content[3])
    price_entry.insert(0,actual_content[4])
    quantity_entry.insert(0,actual_content[5])
    status_combobox.set(actual_content[6])
   


def treeview_data(treeview):
        cursor,connection=connect_database()
        if not cursor or not connection:
            return  
        try:
            cursor.execute("use inventory")
            cursor.execute("select * from product_data")
            records=cursor.fetchall()
            treeview.delete(* treeview.get_children())
            for record in records:
                treeview.insert('',END,values=record)
        except Exception as e:
            messagebox.showerror("Error",f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()
             
#function for dropdown menu box to select from differnt tables
def fetch_supplier_category(category_combobox,Supplier_combobox):
    category_option=[]
    supplier_option=[]
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    #Fill the values of supplier from supplier data table
    cursor.execute('use inventory')
    cursor.execute('select name from category_data')
    names=cursor.fetchall()
    if len(names)>0:
        category_combobox.set('Select')
        for name in names:
            category_option.append(name[0])
        category_combobox.config(values=category_option)
    
    #Fill the values of supplier from supplier data table
    cursor.execute('select name from supplier_data')
    names=cursor.fetchall()
    if len(names)>0:
        Supplier_combobox.set('Select')
        for name in names:
            supplier_option.append(name[0])
        Supplier_combobox.config(values=supplier_option)


def add_product(category,supplier,name,price,quantity,status,treeview):
    if category=='Empty':
        messagebox.showerror("Error","Please Add Category")
    elif supplier=='Empty':
        messagebox.showerror("Error","Please Add Category")
    elif category=='Select' or supplier=='Select' or name=='' or price=='' or quantity=='' or status=='Select Status':
        messagebox.showerror("Error","All Fields Are Required")
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory')
            cursor.execute('Create table if not exists product_data (id int auto_increment primary key, category varchar(100), supplier varchar(100), name varchar(100), price decimal(12,2), quantity int, status varchar(50))')
            cursor.execute('select * from product_data where category=%s and supplier=%s and name=%s',(category,supplier,name))
            existing_product=cursor.fetchone()
            if existing_product:
                messagebox.showerror("Error","Product, Already Exists!")
                return
            cursor.execute('insert into product_data (category,supplier,name,price,quantity,status) values(%s,%s,%s,%s,%s,%s)',(category,supplier,name,price,quantity,status))
            connection.commit()
            messagebox.showinfo("Success","Data Was Added")
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror("Error",f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()
          




def product_form(window):
    global back_image
    product_frame=Frame(window,width=1070,height=567,bg="white")
    product_frame.place(x=250,y=98,relwidth=1, width=-250, relheight=0.85) #if problem we can change x=20,y=100
    back_image=PhotoImage(file="images/back.png")
    back_button=Button(product_frame,image=back_image,bd=0,cursor="hand2",bg="white",command=lambda:product_frame.place_forget())
    back_button.place(x=10,y=10 )

    #left_Frame for supplier manange deatils
    left_frame=Frame(product_frame,bg='white',bd=2,relief=RIDGE)
    left_frame.place(x=20,y=80)
    heading_lable=Label(left_frame,text="Manage Products Details",font=("times new roman", 16,"bold"),bg="#594236",fg="white")
    heading_lable.grid(row=0,columnspan=2,sticky='we')

    #category combobox
    category_lable=Label(left_frame,text='Category',font=("new times roman",14),bg="white")
    category_lable.grid(row=1,column=0,padx=20,sticky='w')
    category_combobox=ttk.Combobox(left_frame,font=("new times roman",12),width=18,state='readonly')
    category_combobox.grid(row=1,column=1,pady=20)
    category_combobox.set('Empty')

    #Supplier combobox
    Supplier_lable=Label(left_frame,text='Supplier',font=("new times roman",14),bg="white")
    Supplier_lable.grid(row=2,column=0,padx=20,sticky='w')
    Supplier_combobox=ttk.Combobox(left_frame,font=("new times roman",12),width=18,state='readonly')
    Supplier_combobox.grid(row=2,column=1)
    Supplier_combobox.set('Empty')

    #name lable
    name_lable=Label(left_frame,text='Name',font=("new times roman",14),bg="white")
    name_lable.grid(row=3,column=0,padx=20,sticky='w')
    name_entry=Entry(left_frame,font=("new times roman",12),bg="lightyellow")
    name_entry.grid(row=3,column=1,pady=20)

    #price lable
    price_lable=Label(left_frame,text='Price',font=("new times roman",14),bg="white")
    price_lable.grid(row=4,column=0,padx=20,sticky='w')
    price_entry=Entry(left_frame,font=("new times roman",12),bg="lightyellow")
    price_entry.grid(row=4,column=1,pady=20)

    #quantity lable
    quantity_lable=Label(left_frame,text='Quantity',font=("new times roman",14),bg="white")
    quantity_lable.grid(row=5,column=0,padx=20,sticky='w')
    quantity_entry=Entry(left_frame,font=("new times roman",12),bg="lightyellow")
    quantity_entry.grid(row=5,column=1,pady=20)

    #status combobox
    status_lable=Label(left_frame,text='Status',font=("new times roman",14),bg="white")
    status_lable.grid(row=6,column=0,padx=20,sticky='w')
    status_combobox=ttk.Combobox(left_frame,values=('Active','Inactive'),font=("new times roman",12),width=18,state='readonly')
    status_combobox.grid(row=6,column=1)
    status_combobox.set('Select Status')

    #button for this section

    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=7,columnspan=2,pady=(30,10))
    #Add button
    add_button=Button(button_frame,text="ADD",font=("new times roman",12),width=8,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:add_product(category_combobox.get(),Supplier_combobox.get(),
                                                                                                                                                    name_entry.get(),price_entry.get(),quantity_entry.get(),status_combobox.get(),treeview))
    add_button.grid(row=0,column=0,padx=10)

    #update button
    update_button=Button(button_frame,text="UPDATE",font=("new times roman",12),width=8,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:update_product(category_combobox.get(),Supplier_combobox.get(),
                                                                                                                                                    name_entry.get(),price_entry.get(),quantity_entry.get(),status_combobox.get(),treeview))
    update_button.grid(row=0,column=1,padx=10)

    #delete button
    delete_button=Button(button_frame,text="DELETE",font=("new times roman",12),width=8,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:delete_product(treeview,category_combobox,Supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox))
    delete_button.grid(row=0,column=2,padx=10)

    #clear button
    clear_button=Button(button_frame,text="CLEAR",font=("new times roman",12),width=8,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:clear_fields(treeview,category_combobox,Supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox))
    clear_button.grid(row=0,column=3,padx=10)

#Working on the right side  
    search_frame=LabelFrame(product_frame,text='Search Product',font=("new times roman",12,'bold'),bg='white')
    search_frame.place(x=480,y=80)

    search_combobox=ttk.Combobox(search_frame,values=('Category','Supplier','Name','Status',),state='readonly',width=16,font=("new times roman",12))
    search_combobox.grid(row=0,column=0,padx=10)
    search_combobox.set("Search By")

    #search
    search_entry=Entry(search_frame,font=("new times roman",12),bg="lightyellow",width=16)
    search_entry.grid(row=0,column=1)

    #search button
    search_button=Button(search_frame,text="SEARCH",font=("new times roman",12),width=8,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:search_product(treeview,search_combobox,search_entry))
    search_button.grid(row=0,column=2,padx=(10,0),pady=10)

    #show_all button
    show_all_button=Button(search_frame,text="SHOW ALL",font=("new times roman",12),width=9,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:show_all(treeview,search_combobox,search_entry))
    show_all_button.grid(row=0,column=3,padx=10)

    #treeviewframe
    treeview_frame=Frame(product_frame,bg='white')
    treeview_frame.place(x=480,y=160,width=540,height=330)
    scrolly=Scrollbar(treeview_frame,orient=VERTICAL)
    scrollx=Scrollbar(treeview_frame,orient=HORIZONTAL)
    treeview=ttk.Treeview(treeview_frame,columns=('ID','Category','Supplier','Name','Price','Quantity','Status'),show='headings',
                          yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH,expand=1)
    #headings
    treeview.heading('ID',text="ID")
    treeview.heading('Category',text="Category")
    treeview.heading('Supplier',text="Supplier")
    treeview.heading('Name',text="Product Name")
    treeview.heading('Price',text="Price")
    treeview.heading('Quantity',text="Quantity")
    treeview.heading('Status',text="Status")

    treeview.column('ID',width=80)
    treeview.column('Category', width=150) 
    treeview.column('Supplier', width=150) 
    treeview.column('Name', width=200) 
    treeview.column('Price', width=80)
    treeview.column('Quantity', width=80)
    treeview.column('Status', width=100) 

    fetch_supplier_category(category_combobox,Supplier_combobox)
    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',lambda event:select_data(event,treeview,category_combobox,Supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox))
    return product_frame