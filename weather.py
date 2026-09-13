# -*- coding: utf-8 -*-
# ---- Weather form (dashboard-compatible, two-panel layout) ----
import os
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from dotenv import load_dotenv

load_dotenv()

def weather_form(window):
    from datetime import datetime, timezone, timedelta
    import requests
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()

    wf = Frame(window, width=1070, height=567, bg="white")
    wf.place(x=250, y=98, relwidth=1, width=-250, relheight=0.85)

    # Header bar (same look as other screens)
    heading = Label(wf, text="Current Weather", font=("times new roman", 16, "bold"),
                    bg="#594236", fg="white")
    heading.place(x=0, y=0, relwidth=1)

    # Back button (keep a ref to image)
    back_img = PhotoImage(file="images/back.png")
    wf._back_img = back_img
    Button(wf, image=back_img, bd=0, cursor="hand2", bg="white",
           command=lambda: wf.place_forget()).place(x=10, y=30)

    # -------- LEFT: Illustration --------
    left = Frame(wf, bg="white")
    left.place(x=40, y=90, width=420, height=420)
    try:
        raw = Image.open("images/Copy of logo.png")
        raw.thumbnail((380, 380))
        hero = ImageTk.PhotoImage(raw)
        wf._hero = hero
        Label(left, image=hero, bg="white").place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        Canvas(left, bg="#e8f2ec", highlightthickness=0).place(relwidth=1, relheight=1)
        Label(left, text="(Add weather illustration at images/Copy of logo.png)",
              font=("new times roman", 10), fg="#0f4d7d", bg="#e8f2ec").place(relx=0.5, rely=0.5, anchor="center")

    # -------- RIGHT: Form/values --------
    right = Frame(wf, bg="white")
    right.place(x=500, y=70, width=480, height=420)
    #right.grid_columnconfigure(1, weight=1)

    # City row
    Label(right, text="Enter City Name", font=("new times roman", 14,'bold'), bg="white").grid(row=0, column=0, sticky="w", padx=(0, 15), pady=(5, 12))
    city_entry = Entry(right, font=("new times roman", 12), bg="lightyellow", width=17)
    city_entry.place(x=170,y=10)
    

    # Time + “CURRENT WEATHER” line
    name = Label(right, text="", font=('arial', 12, 'bold'), bg="white")
    name.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 6))
    clock = Label(right, text="", font=('helvetica', 14), bg="white")
    clock.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 10))

    # Big temp + desc
    t = Label(right, text="--°C", font=("arial", 48, 'bold'), fg='#ee666d', bg="white")
    t.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 6))
    c = Label(right, text="—", font=("arial", 14, 'bold'), bg="white")
    c.grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 14))

    # Bottom stats bar (inside right)
    stats = Frame(right, bg="white")
    stats.grid(row=5, column=0, columnspan=2, sticky="we", pady=(10, 10))
    for i in range(4):
        stats.grid_columnconfigure(i, weight=1)

    def stat_cell(col, title):
        Label(stats, text=title, font=('helvetica', 11, 'bold'), fg='white', bg='#1ab5ef',
              padx=10, pady=4).grid(row=0, column=col, sticky="we", padx=3)
        val = Label(stats, text='—', font=("arial", 12, 'bold'), bg='#1ab5ef', padx=10, pady=6)
        val.grid(row=1, column=col, sticky="we", padx=3)
        return val

    w = stat_cell(0, "WIND")
    h = stat_cell(1, "HUMIDITY")
    d = stat_cell(2, "DESCRIPTION")
    p = stat_cell(3, "PRESSURE")

    # Buttons (centered under right panel)
    btns = Frame(wf, bg="white")
    btns.place(x=500, y=450, width=530, height=40)

    # ---- fetch function (uses your original logic & values) ----
    def getWeather():
        if not OPENWEATHER_API_KEY:
            messagebox.showerror("Configuration Error", "OpenWeatherMap API key not found.\nPlease set OPENWEATHER_API_KEY in your .env file.")
            return

        city = city_entry.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name.")
            return

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

        try:
            r = requests.get(url, timeout=10)
            data = r.json()
            if r.status_code != 200:
                message = data.get("message", "Unknown error from weather service")
                if "city not found" in message.lower():
                    messagebox.showwarning("Not found", f"No match for '{city}'. Try a more specific name.")
                else:
                    messagebox.showerror("Weather error", message.capitalize())
                return
        except Exception as e:
            messagebox.showerror("Network error", f"Could not fetch weather.\n\n{e}")
            return

        offset_seconds = data.get("timezone", 0)
        tz = timezone(timedelta(seconds=offset_seconds))
        local_time = datetime.now(tz)
        current_time = local_time.strftime("%I:%M %p")

        temp_c = round(data["main"]["temp"])
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_ms  = data["wind"]["speed"]
        desc     = data["weather"][0]["description"].title()
        city_name = data.get("name", city)

        clock.config(text=f"Time: {current_time}")
        name.config(text=f"{city_name} — CURRENT WEATHER")
        t.config(text=f"{temp_c}°C")
        c.config(text=desc)
        w.config(text=f"{wind_ms} m/s")
        h.config(text=f"{humidity}%")
        d.config(text=desc)
        p.config(text=f"{pressure} hPa")

    def clear_all():
        city_entry.delete(0, END)
        name.config(text="")
        clock.config(text="")
        t.config(text="--°C")
        c.config(text="—")
        for lab in (w, h, d, p):
            lab.config(text="—")

    get_btn = Button(btns, text="GET WEATHER", width=18,
                     font=("new times roman", 12, "bold"), fg="white", bg="#0f4d7d",
                     activebackground="#0f4d7d", cursor="hand2", bd=0, command=getWeather)
    get_btn.pack(side=LEFT, padx=20)
    city_entry.bind('<Return>', lambda event: getWeather())

    clr_btn = Button(btns, text="CLEAR", width=10,
                     font=("new times roman", 12, "bold"), fg="white", bg="#0f4d7d",
                     activebackground="#0f4d7d", cursor="hand2", bd=0, command=clear_all)
    clr_btn.pack(side=LEFT)

    return wf
