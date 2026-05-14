from tkinter import *
from employees import employee_form
from supplier import supplier_form
from category import category_form
from products import product_form
from weather import weather_form
from prediction import crop_prediction_form
from tkinter import messagebox
import time
from employees import connect_database


def exit_app():
    result = messagebox.askyesno("Confirm Exit", "Do you really want to exit?")
    if result:
        window.destroy()  # closes the entire app


def update():
    #updating front page numbers
    cursor,connection=connect_database()
    if not cursor or not connection:
        return 
    cursor.execute("use inventory")
    #for employee
    cursor.execute('select * from employee_data')
    records=cursor.fetchall()
    total_emp_count_lable.config(text=len(records))

    #for supplier
    cursor.execute('select * from supplier_data')
    records=cursor.fetchall()
    total_supply_count_lable.config(text=len(records))

    #for category
    cursor.execute('select * from category_data')
    records=cursor.fetchall()
    total_category_count_lable.config(text=len(records))

    #for product
    cursor.execute('select * from product_data')
    records=cursor.fetchall()
    total_products_count_lable.config(text=len(records))



    date_time = time.strftime('%I:%M:%S %p')  
    current_date = time.strftime('%A, %B %d, %Y')
    subtitle_lable.config(
    text=f"Welcome\t\t\t\t{current_date}\t\t\tTime: {date_time}"
    )
    subtitle_lable.after(1000, update)


current_frame=None
def show_form(form_function):
    global current_frame
    if current_frame:
        current_frame.place_forget()
    current_frame=form_function(window)
    

#Gui part
window=Tk()
window.title("GrowPilot")
window.geometry("1290x665+100+50")
window.resizable(0,0)
window.config(bg="white")

bg_image=PhotoImage(file="images/logo.png")
titleLable1=Label(window,image=bg_image,compound=LEFT,text=" Welcome To GrowPilot",font=("times new roman",30,"bold"),bg="#411d13",fg="white",anchor="w",padx=30)
titleLable1.place(x=0,y=0,relwidth=1)

logout_button=Button(window,text="Logout",font=("times new roman",20,"bold"),fg="black",command=lambda:exit_app(),cursor='hand2')
logout_button.place(x=1100,y=10)

subtitle_lable=Label(window,text="Welcome Admin\t\t Date: 08-08-2003\t\t Time: 12:36:34 pm", font=("times new roman",15),bg="#9c6644",fg="white")
subtitle_lable.place(x=0,y=70,relwidth=1)
#
heading_lable=Label(window,text="\t\t\tFarm  Management  Overview",font=("times new roman", 16,"bold"),bg="#594236",fg="white")
heading_lable.place(x=0,y=98,relwidth=1)

#left-frame
left_frame=Frame(window)
left_frame.place(x=0,y=98,width=250,height=800)
logo_image=PhotoImage(file="images/farmer.png")
image_lable=Label(left_frame,image=logo_image)
image_lable.pack()

menu_lable=Label(left_frame,text="Menu",font=("times new roman",20,"bold"),bg="#533e2d",height=1,fg='white')
menu_lable.pack(fill=X)
                 
#Employee
employee_icon=PhotoImage(file="images/employee.png")
employee_button=Button(left_frame,image=employee_icon,compound=LEFT,text=" Employees", font=("times new roman",22,"bold"),anchor="w",padx=10,height=50,command=lambda: show_form(employee_form),cursor='hand2')
employee_button.pack(fill=X)

#Supplier
supplier_icon=PhotoImage(file="images/supplier2.png")
supplier_button=Button(left_frame,image=supplier_icon,compound=LEFT,text=" Suppliers", font=("times new roman",22,"bold"),anchor="w",padx=10,height=60,command=lambda:show_form(supplier_form),cursor='hand2')
supplier_button.pack(fill=X)

#Category
category_icon=PhotoImage(file="images/allocated.png")
category_button=Button(left_frame,image=category_icon,compound=LEFT,text=" Categories", font=("times new roman",22,"bold"),anchor="w",padx=10,height=60,command=lambda:show_form(category_form),cursor='hand2')#to reduce height we can remove or reduce the height=60
category_button.pack(fill=X)

#products
product_icon=PhotoImage(file="images/cubes.png")
product_button=Button(left_frame,image=product_icon,compound=LEFT,text=" Products", font=("times new roman",22,"bold"),anchor="w",padx=10,height=60,command=lambda:show_form(product_form),cursor='hand2')
product_button.pack(fill=X)

#weather
weather_icon=PhotoImage(file="images/cloudy-day.png")
weather_button=Button(left_frame,image=weather_icon,compound=LEFT,text="Weather", font=("times new roman",22,"bold"),anchor="w",padx=10,height=60,command=lambda:show_form(weather_form),cursor='hand2')
weather_button.pack(fill=X)

#exit
exit_icon=PhotoImage(file="images/predictive-chart.png")
exit_button=Button(left_frame,image=exit_icon,compound=LEFT,text="Prediction", font=("times new roman",22,"bold"),anchor="w",padx=10,height=60,command=lambda:show_form(crop_prediction_form),cursor='hand2')
exit_button.pack(fill=X)
#can add one more after the end that is chatbot for help


#centre figures
#frame1
emp_frame = Frame(window, bg="#9c6644", bd=4, relief=RIDGE)
emp_frame.place(x=430, y=190, height=170, width=280)
emp_frame.configure(highlightbackground="gray", highlightthickness=1)
total_emp_icon=PhotoImage(file="images/staff.png")
total_emp_icon_lable=Label(emp_frame,image=total_emp_icon,bg="#9c6644")
total_emp_icon_lable.pack(pady=5)

total_emp_lable=Label(emp_frame,text="Total Employees",bg="#9c6644",fg="white",font=("times new roman",20,"bold"))
total_emp_lable.pack()

total_emp_count_lable=Label(emp_frame,text="0",bg="#9c6644",fg="white",font=("times new roman",20,"bold"))
total_emp_count_lable.pack()

#Frame2
supply_frame=Frame(window,bg="#728740",bd=3,relief=RIDGE)
supply_frame.place(x=830,y=190,height=170,width=280)
supply_frame.configure(highlightbackground="gray", highlightthickness=1)

total_supply_icon=PhotoImage(file="images/supply-chain-management.png")
total_supply_icon_lable=Label(supply_frame,image=total_supply_icon,bg="#728740")
total_supply_icon_lable.pack(pady=5)

total_supply_lable=Label(supply_frame,text="Total Supply",bg="#728740",fg="white",font=("times new roman",20,"bold"))
total_supply_lable.pack()

total_supply_count_lable=Label(supply_frame,text="0",bg="#728740",fg="white",font=("times new roman",20,"bold"))
total_supply_count_lable.pack()

#frame3
category_frame=Frame(window,bg="#bc6c25",bd=3,relief=RIDGE)
category_frame.place(x=430,y=410,height=170,width=280)
category_frame.configure(highlightbackground="gray", highlightthickness=1)
total_category_icon=PhotoImage(file="images/classification.png")
total_category_icon_lable=Label(category_frame,image=total_category_icon,bg="#bc6c25")
total_category_icon_lable.pack(pady=5)

total_category_lable=Label(category_frame,text="Total Category",bg="#bc6c25",fg="white",font=("times new roman",20,"bold"))
total_category_lable.pack()

total_category_count_lable=Label(category_frame,text="0",bg="#bc6c25",fg="white",font=("times new roman",20,"bold"))
total_category_count_lable.pack()

#frame4
products_frame=Frame(window,bg="#4a0a77",bd=3,relief=RIDGE) # Changed background color for distinction
products_frame.place(x=830,y=410,height=170,width=280) # Adjusted x-coordinate to place it next to the category frame
products_frame.configure(highlightbackground="gray", highlightthickness=1)
total_products_icon=PhotoImage(file="images/products.png") # Changed image file name
total_products_icon_lable=Label(products_frame,image=total_products_icon,bg="#4a0a77") #image 64x64 karni hai yaad rakhna 
total_products_icon_lable.pack(pady=5)

total_products_lable=Label(products_frame,text="Total Products",bg="#4a0a77",fg="white",font=("times new roman",20,"bold")) # Changed text
total_products_lable.pack()

total_products_count_lable=Label(products_frame,text="0",bg="#4a0a77",fg="white",font=("times new roman",20,"bold")) # Changed label variable
total_products_count_lable.pack()


update()
window.mainloop()