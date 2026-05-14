from tkinter import *
from PIL import ImageTk
from employees import connect_database
from tkinter import messagebox
# ===================== FUNCTIONS =====================
def login_page():
    signup_window.destroy()
    import signin

def clear():
    email_entry.delete(0,END)
    password_entry.delete(0,END)
    username_entry.delete(0,END)
    confirm_entry.delete(0,END)
    check.set(0)

def checking_form():
    if email_entry.get()=='' or username_entry.get()=='' or password_entry.get()=='' or confirm_entry.get()=='':
        messagebox.showerror("Error","All Fields are Required")
    elif password_entry.get()!=confirm_entry.get():
        messagebox.showerror("Error","Password Missmatch")
    elif check.get()==0:
        messagebox.showerror("Error","Accept Terms & Condition")
    else:
        connect_database()
        cursor,connection=connect_database()
        try:
            cursor.execute("use inventory")
            cursor.execute("create table if not exists User_signin_details (id int auto_increment primary key not null, email varchar(100), username varchar(70), password varchar(40))")
        except:
            cursor.execute("use inventory")
        query="select * from User_signin_details where username=%s"
        cursor.execute(query,(username_entry.get()))
        row=cursor.fetchone()
        if row!= None:
            messagebox.showerror("Error","User Already Exists")
        else:
            query="insert into User_signin_details (email,username,password) values(%s,%s,%s)"
            cursor.execute(query,(email_entry.get(),username_entry.get(),password_entry.get()))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success","Registration Was Successful")
            clear()
            signup_window.destroy()
            import signin





signup_window=Tk()
signup_window.title('SignUp Page')
signup_window.resizable(False,False)
signup_window.geometry('985x575+200+100')

bg_image = ImageTk.PhotoImage(file='images/signin_background.png')
bg_label = Label(signup_window, image=bg_image)
bg_label.grid()

# ===================== BORDERED SIGNUP FRAME =====================
form_frame = Frame(signup_window, bg='white', bd=3, relief=RIDGE,
                   highlightbackground="#0d6b3d", highlightthickness=2)
form_frame.place(x=60, y=80, width=400, height=430)


# left card/frame
left_frame = Frame(signup_window, bg='white')
left_frame.place(x=80, y=85, width=360, height=420)

# let the single column expand so right-aligned items work
left_frame.grid_columnconfigure(0, weight=1)

heading = Label(left_frame, text='Create An Account',
                font=("Segoe UI", 25, "bold"),
                bg='white', fg='#0d6b3d')
heading.grid(row=0, column=0, padx=20, pady=(10, 8), sticky='w')

# Email
email_lable = Label(left_frame, text='Email', font=("new times roman", 12), bg="white")
email_lable.grid(row=1, column=0, padx=20, sticky='w', pady=(6, 0))
email_entry = Entry(left_frame, font=("new times roman", 10), bg="lightyellow", width=45)
email_entry.grid(row=2, column=0, sticky='w', padx=20)

# Username
username_lable = Label(left_frame, text='Username', font=("new times roman", 12), bg="white")
username_lable.grid(row=3, column=0, padx=20, sticky='w', pady=(10, 0))
username_entry = Entry(left_frame, font=("new times roman", 10), bg="lightyellow", width=45)
username_entry.grid(row=4, column=0, sticky='w', padx=20)

# Password
password_lable = Label(left_frame, text='Password', font=("new times roman", 12), bg="white")
password_lable.grid(row=5, column=0, padx=20, sticky='w', pady=(10, 0))
password_entry = Entry(left_frame, font=("new times roman", 10), bg="lightyellow", width=45)
password_entry.grid(row=6, column=0, sticky='w', padx=20)

# Confirm Password
confirm_lable = Label(left_frame, text='Confirm Password', font=("new times roman", 12), bg="white")
confirm_lable.grid(row=7, column=0, padx=20, sticky='w', pady=(10, 0))
confirm_entry = Entry(left_frame, font=("new times roman", 10), bg="lightyellow", width=45)
confirm_entry.grid(row=8, column=0, sticky='w', padx=20)

# Terms & Conditions
check=IntVar()
terms = Checkbutton(left_frame, text='I Agree To The Terms & Condition',
                    font=("new times roman", 9, 'bold'),
                    bg="white", cursor='hand2', anchor='w',variable=check)
terms.grid(row=9, column=0, padx=20, pady=(8, 6), sticky='w')

# Sign-Up button
login_button = Button(left_frame, text='Sign-Up',
                      font=("Segoe UI", 12, "bold"),
                      fg='white', bg='#0d6b3d', width=24,
                      activebackground='#0a5231', activeforeground='white',
                      cursor='hand2', bd=0,command=checking_form)
login_button.grid(row=10, column=0, padx=55, pady=(8, 6), sticky='w')

# Bottom row: text (left) + link (right)
alreadyhaveanaccount = Label(left_frame, text="Already have an account?",
                             font=("Segoe UI", 9, 'bold'),
                             bg='white', fg='#334155')
alreadyhaveanaccount.grid(row=11, column=0, padx=20, pady=(8, 4), sticky='w')

already_login_button = Button(left_frame, text='Login',
                              font=("Segoe UI", 9, 'bold'),
                              fg='#1665c1', bg='white',
                              activebackground='white', activeforeground='#1665c1',
                              cursor='hand2', bd=0, command=login_page)
# use grid (not place) and right-align in the same column
already_login_button.grid(row=11, column=0, padx=20, pady=(8, 4), sticky='e')

signup_window.mainloop()