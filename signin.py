from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
from employees import connect_database
# ===================== FUNCTIONS =====================
def login_user():
    # basic empty-check (also ignore placeholder text)
    u = usernameEntry.get().strip()
    p = password_Entry.get().strip()
    if not u or not p or u == 'Username' or p == 'Password':
        messagebox.showerror("Error", "All fields are required")
        return False

    cursor, connection = connect_database()
    if not cursor or not connection:
        return False

    try:
        cursor.execute("USE inventory")
        query = "SELECT 1 FROM User_signin_details WHERE username=%s AND password=%s"
        cursor.execute(query, (u, p))
        row = cursor.fetchone()
        if row is None:
            messagebox.showerror("Error", "Invalid Username or Password")
            return False
        else:
            messagebox.showinfo("Success", "Login was Successful")
            return True
    except Exception as e:
        messagebox.showerror("Error", f"Error due to {e}")
        return False
    finally:
        cursor.close()
        connection.close()


def combined_command():
    # Only launch dashboard if login succeeded
    if login_user():
        growpilot()


def hide():
    open_eye.config(file='images/close_eye.png')
    password_Entry.config(show='*')
    eye_button.config(command=show)

def show():
    open_eye.config(file='images/open_eye.png')
    password_Entry.config(show='')
    eye_button.config(command=hide)

def user_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)

def password_enter(event):
    if password_Entry.get() == 'Password':
        password_Entry.delete(0, END)

def signup_page():
    login_window.destroy()
    import signup

def growpilot():
    login_window.destroy()
    import dashboard

# ===================== GUI SETUPfor forgetpassword =====================

def forget_password():

    def chnage_password():
        # 1) Validate inputs from the RESET form widgets
        u = username_entry.get().strip()
        p1 = password_entry.get()
        p2 = confirm_entry.get()
        if not u or not p1 or not p2:
            messagebox.showerror("Error","Fill All The Fields", parent=forget_window)
            return
        if p1 != p2:
            messagebox.showerror("Error","Password and Confirm Password are not the same", parent=forget_window)
            return
        # 2) DB work
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute("USE inventory")
            # use the username from the RESET form (username_entry) and pass a 1-tuple
            cursor.execute("SELECT 1 FROM User_signin_details WHERE username=%s", (u,))
            row = cursor.fetchone()

            if row is None:
                messagebox.showerror("Error", "Incorrect Username", parent=forget_window)
            else:
                # UPDATE syntax: SET ... WHERE ...
                cursor.execute(
                    "UPDATE User_signin_details SET password=%s WHERE username=%s",
                    (p1, u)
                )
                connection.commit()
                messagebox.showinfo(
                    "Update",
                    "Password was updated. Please log in with your new password.",
                    parent=forget_window
                )
                forget_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to {e}")
        finally:
            cursor.close()
            connection.close()


    forget_window = Toplevel()
    forget_window.title("Reset Password")
    forget_window.geometry('985x575+200+100')
    forget_window.resizable(False, False)

    # Background image
    forget_window.bgpic = ImageTk.PhotoImage(file="images/signin_background.png")
    bglabel = Label(forget_window, image=forget_window.bgpic)
    bglabel.place(x=0, y=0)

    # ===================== BORDERED FRAME FOR FORGET PASSWORD=====================
    form_frame = Frame(forget_window, bg='white', bd=3, relief=RIDGE,
                       highlightbackground="#0d6b3d", highlightthickness=2)
    form_frame.place(x=60, y=100, width=400, height=320)
    form_frame.grid_columnconfigure(0, weight=1)

    # ===================== RESET PASSWORD FORM =====================
    heading = Label(form_frame, text='Reset Password',
                    font=("Segoe UI", 25, "bold"),
                    bg='white', fg='#0d6b3d')
    heading.grid(row=0, column=0, padx=70, pady=(15, 10), sticky='w')

    # Username
    username_lable = Label(form_frame, text='Username',
                           font=("new times roman", 12), bg="white")
    username_lable.grid(row=1, column=0, padx=40, sticky='w', pady=(5, 0))
    username_entry = Entry(form_frame, font=("new times roman", 10),
                           bg="lightyellow", width=40)
    username_entry.grid(row=2, column=0, padx=40, pady=(0, 5), sticky='w')

    # Password
    password_lable = Label(form_frame, text='Password',
                           font=("new times roman", 12), bg="white")
    password_lable.grid(row=3, column=0, padx=40, sticky='w', pady=(5, 0))
    password_entry = Entry(form_frame, font=("new times roman", 10),
                           bg="lightyellow", width=40)
    password_entry.grid(row=4, column=0, padx=40, pady=(0, 5), sticky='w')

    # Confirm Password
    confirm_lable = Label(form_frame, text='Confirm Password',
                          font=("new times roman", 12), bg="white")
    confirm_lable.grid(row=5, column=0, padx=40, sticky='w', pady=(5, 0))
    confirm_entry = Entry(form_frame, font=("new times roman", 10),
                          bg="lightyellow", width=40)
    confirm_entry.grid(row=6, column=0, padx=40, pady=(0, 10), sticky='w')

    # Reset Button
    reset_button = Button(form_frame, text='Reset Password',
                          font=("Segoe UI", 12, "bold"),
                          fg='white', bg='#0d6b3d', width=20,
                          activebackground='#0a5231', activeforeground='white',
                          cursor='hand2', bd=0,command=chnage_password)
    reset_button.grid(row=7, column=0, padx=20, pady=(10, 5))


# ===================== GUI SETUP for signup page =====================
login_window = Tk()  
login_window.geometry('985x575+200+100')
login_window.resizable(0, 0)
login_window.title("SignIn Page")

# Background image
bg_image = ImageTk.PhotoImage(file='images/signin_background.png')
bg_label = Label(login_window, image=bg_image)
bg_label.place(x=0, y=0)

# ===================== BORDERED LOGIN FRAME =====================
form_frame = Frame(login_window, bg='white', bd=3, relief=RIDGE,
                   highlightbackground="#0d6b3d", highlightthickness=2)
form_frame.place(x=80, y=90, width=360, height=370)

# ===================== LOGIN FORM =====================
heading = Label(form_frame, text='USER LOGIN',
                font=("Segoe UI", 25, "bold"),
                bg='white', fg='#0d6b3d')
heading.place(x=85, y=25)

# Username Entry
usernameEntry = Entry(form_frame, width=28,
                      font=("Segoe UI", 13, "bold"),
                      bd=0, fg='#0d6b3d', highlightthickness=0,
                      insertbackground='#0d6b3d')
usernameEntry.place(x=40, y=90)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', user_enter)
Frame(form_frame, width=280, height=2, bg='#0d6b3d').place(x=40, y=115)

# Password Entry
password_Entry = Entry(form_frame, width=28,
                       font=("Segoe UI", 13, "bold"),
                       bd=0, fg='#0d6b3d', highlightthickness=0,
                       insertbackground='#0d6b3d',show='*')
password_Entry.place(x=40, y=140)
password_Entry.insert(0, 'Password')
password_Entry.bind('<FocusIn>', password_enter)
Frame(form_frame, width=280, height=2, bg='#0d6b3d').place(x=40, y=165)

# Eye Button
open_eye = PhotoImage(file='images/close_eye.png')
eye_button = Button(form_frame, image=open_eye, bd=0, bg='white',
                    activebackground='white', cursor='hand2', command=show)
eye_button.place(x=300, y=138)

# Forgot Password
forgot_button = Button(form_frame, text='Forgot Password?',
                       bd=0, bg='white', activebackground='white',
                       cursor='hand2', font=("Segoe UI", 9, "bold"),
                       fg='#1665c1', activeforeground='#1665c1',command=forget_password)
forgot_button.place(x=200, y=180)

# Login Button
login_button = Button(form_frame, text='Log In',
                      font=("Segoe UI", 12, "bold"),
                      fg='white', bg='#0d6b3d', width=24,
                      activebackground='#0a5231', activeforeground='white',
                      cursor='hand2', bd=0,command=combined_command)
login_button.place(x=50, y=220)

# Signup Section
signup_label = Label(form_frame, text="Don't have an account?",
                     font=("Segoe UI", 9, 'bold'),
                     bg='white', fg='#334155')
signup_label.place(x=40, y=280)

newaccount_button = Button(form_frame, text='Create New Account',
                           font=("Segoe UI", 9, 'bold'),
                           fg='#1665c1', bg='white',
                           activebackground='white', activeforeground='#1665c1',
                           cursor='hand2', bd=0,command=signup_page)
newaccount_button.place(x=200, y=280)

login_window.mainloop()
