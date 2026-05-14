from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk
from employees import connect_database

def delete_category(treeview):
    index=treeview.selection()
    content=treeview.item(index)
    row=content['values']
    id=row[0]
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
                cursor.execute("delete from category_data where id=%s",id)
                connection.commit()
                treeview_data(treeview)
                messagebox.showinfo("Success","Selected Data Was Deleted")
            except Exception as e:
                messagebox.showerror("Error",f'Error due to {e}')
            finally:
                    cursor.close()
                    connection.close()


def clear(id_entry,category_name_entry,description_text,treeview):
    id_entry.delete(0,END)
    category_name_entry.delete(0,END)
    description_text.delete(1.0,END)
    treeview.selection_remove(treeview.selection())


def treeview_data(treeview):
        cursor,connection=connect_database()
        if not cursor or not connection:
            return  
        try:
            cursor.execute("use inventory")
            cursor.execute("select * from category_data")
            records=cursor.fetchall()
            treeview.delete(* treeview.get_children())
            for record in records:
                treeview.insert('',END,values=record)
        except Exception as e:
            messagebox.showerror("Error",f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()
             


def add_category(id,name,description,treeview):
    if id==''or name=='' or description=='':
        messagebox.showerror("Error","All Fields Are Required")
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute("use inventory")
            cursor.execute("Create table if not exists category_data (id int primary key, name varchar(50),description text)")
            cursor.execute('select * from category_data where id=%s',id)
            if cursor.fetchone():
                messagebox.showerror("Error","ID, Already Exists!")
                return
            cursor.execute('insert into category_data values(%s,%s,%s)',(id,name,description))
            connection.commit()
            messagebox.showinfo("Success","Data Was Added")
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror("Error",f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()
            


def category_form(window):
    global back_image,logo
    category_frame=Frame(window,width=1070,height=567,bg="white")
    category_frame.place(x=250,y=98,relwidth=1, width=-250, relheight=0.85) #if problem we can change x=20,y=100
    heading_lable=Label(category_frame,text="Manage Category Details",font=("times new roman", 16,"bold"),bg="#594236",fg="white")
    heading_lable.place(x=0,y=0,relwidth=1)
    back_image=PhotoImage(file="images/back.png")
    back_button=Button(category_frame,image=back_image,bd=0,cursor="hand2",bg="white",command=lambda:category_frame.place_forget())
    back_button.place(x=10,y=30 )

    #background image
    logo=ImageTk.PhotoImage(file='images/category2.png')
    label=Label(category_frame,image=logo,bg='white')
    label.place(x=40,y=150) #to change height and width of the image

    #Details frame
    detail_frame=Frame(category_frame,bg='white')
    detail_frame.place(x=500,y=60)

    #invoice lable
    id_lable=Label(detail_frame,text='ID No.',font=("new times roman",14),bg="white")
    id_lable.grid(row=0,column=0,padx=20,sticky='w')
    id_entry=Entry(detail_frame,font=("new times roman",12),bg="lightyellow")
    id_entry.grid(row=0,column=1)

    #invoice lable
    category_name_lable=Label(detail_frame,text='Category Name',font=("new times roman",14),bg="white")
    category_name_lable.grid(row=1,column=0,padx=20,sticky='w')
    category_name_entry=Entry(detail_frame,font=("new times roman",12),bg="lightyellow")
    category_name_entry.grid(row=1,column=1,pady=20)

    #Description lable
    description_lable=Label(detail_frame,text='Description',font=("new times roman",14),bg="white")
    description_lable.grid(row=2,column=0,padx=(20,40),sticky='nw',pady=25)
    description_text=Text(detail_frame,width=25,height=6,bd=1,bg='lightyellow')
    description_text.grid(row=2,column=1,pady=20)

    #button for this section

    button_frame=Frame(category_frame,bg='white')
    button_frame.place(x=590,y=285)

    #Add button
    add_button=Button(button_frame,text="ADD",font=("new times roman",12),width=8,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:add_category(id_entry.get(),category_name_entry.get(),description_text.get(1.0,END).strip(),treeview))
    add_button.grid(row=0,column=0,padx=20)
    #delete button
    delete_button=Button(button_frame,text="DELETE",font=("new times roman",12),width=8,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda:delete_category(treeview))
    delete_button.grid(row=0,column=1,padx=20)
    #clear button
    clear_button=Button(button_frame,text="CLEAR",font=("new times roman",12),width=8,cursor="hand2",fg="white",bg="#0f4d7d",command=lambda: clear(id_entry,category_name_entry,description_text,treeview))
    clear_button.grid(row=0,column=3,padx=20)

    #treeview frame
    treeview_frame=Frame(category_frame)
    treeview_frame.place(x=510,y=340,height=200,width=500)
    scrolly=Scrollbar(treeview_frame,orient=VERTICAL)
    scrollx=Scrollbar(treeview_frame,orient=HORIZONTAL)
    treeview=ttk.Treeview(treeview_frame,columns=('ID','Name','Description'),show='headings',
                          yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH,expand=1)

    #headings
    treeview.heading('ID',text="Category ID")
    treeview.heading('Name',text="Category Name")
    treeview.heading('Description',text='Description')
    treeview.column('ID',width=80)
    treeview.column('Name',width=140)
    treeview.column('Description',width=140)
    treeview_data(treeview)
    return category_frame