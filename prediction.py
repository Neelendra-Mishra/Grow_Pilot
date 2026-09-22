from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

# Cache model in memory so it loads only once per app session
_CACHED_MODEL = None

def _load_or_train_model():
    global _CACHED_MODEL
    if _CACHED_MODEL is not None:
        return _CACHED_MODEL
    try:
        _CACHED_MODEL = joblib.load("model.pkl")  # safest load for sklearn
        return _CACHED_MODEL
    except Exception:
        # Retrain on current environment to fix incompatibility
        df = pd.read_csv("Crop_recommendation.csv")
        X = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]
        y = df["label"]
        model = RandomForestClassifier(n_estimators=200, random_state=42)
        model.fit(X, y)
        joblib.dump(model, "model.pkl")
        _CACHED_MODEL = model
        return _CACHED_MODEL

def crop_prediction_form(window):

    try:
        model = _load_or_train_model()
    except Exception as e:
        messagebox.showerror("Model error", f"Could not load or train model.\n\n{e}")
        return

    # ---- Frame setup ----
    cp = Frame(window, width=1070, height=567, bg="white")
    cp.place(x=250, y=98, relwidth=1, width=-250, relheight=0.85)

    # Header
    heading = Label(cp, text="Crop Prediction", font=("times new roman", 16, "bold"),
                    bg="#594236", fg="white")
    heading.place(x=0, y=0, relwidth=1)

    # Back button
    back_img = PhotoImage(file="images/back.png")
    cp._back_img = back_img
    Button(cp, image=back_img, bd=0, cursor="hand2", bg="white",
           command=lambda: cp.place_forget()).place(x=10, y=30)

    # ---- Left Image Section ----
    left = Frame(cp, bg="white")
    left.place(x=40, y=90, width=420, height=420)
    try:
        raw = Image.open("images/crop_re.png")  # Replace with your illustration
        raw.thumbnail((390, 390))
        hero = ImageTk.PhotoImage(raw)
        cp._hero = hero
        Label(left, image=hero, bg="white").place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        Canvas(left, bg="#e8f2ec", highlightthickness=0).place(relwidth=1, relheight=1)
        Label(left, text="(Add images/crop_reco.png)", font=("new times roman", 10),
              fg="#0f4d7d", bg="#e8f2ec").place(relx=0.5, rely=0.5, anchor="center")

    # ---- Right Form Section ----
    right = Frame(cp, bg="white")
    right.place(x=500, y=90, width=420, height=420)
    right.grid_columnconfigure(1, weight=1)

    def add_row(r, label_txt, width=28):
        Label(right, text=label_txt, font=("new times roman", 14), bg="white") \
            .grid(row=r, column=0, sticky="w", padx=(0, 18), pady=(6, 14))
        e = Entry(right, font=("new times roman", 12), bg="lightyellow", width=width)
        e.grid(row=r, column=1, sticky="we", pady=(6, 14))
        return e

    n_entry = add_row(0, "Nitrogen (N)")
    p_entry = add_row(1, "Phosphorus (P)")
    k_entry = add_row(2, "Potassium (K)")
    t_entry = add_row(3, "Temperature (°C)")
    h_entry = add_row(4, "Humidity (%)")
    ph_entry = add_row(5, "Soil pH")
    r_entry = add_row(6, "Rainfall (mm)")

    # ---- Result Section ----
    result_card = Frame(cp, bg="white", bd=0)
    result_card.place(x=500, y=480, width=470, height=62)
    result_label = Label(result_card, text="Prediction will appear here",
                         font=("Segoe UI", 12, "bold"), fg="green", bg="white")
    result_label.place(relx=0.5, rely=0.5, anchor="center")

    # ---- Buttons ----
    btns = Frame(cp, bg="white")
    btns.place(x=600, y=440, width=530, height=40)

    def clear_all():
        for e in (n_entry, p_entry, k_entry, t_entry, h_entry, ph_entry, r_entry):
            e.delete(0, END)
        result_label.config(text="Prediction will appear here")

    def predict_crop():
        try:
            # Create DataFrame with same column names as training
            X = pd.DataFrame([{
                "N": float(n_entry.get().strip()),
                "P": float(p_entry.get().strip()),
                "K": float(k_entry.get().strip()),
                "temperature": float(t_entry.get().strip()),
                "humidity": float(h_entry.get().strip()),
                "ph": float(ph_entry.get().strip()),
                "rainfall": float(r_entry.get().strip()),
            }])[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]

            pred = model.predict(X)[0]
            result_label.config(text=f"Recommended Crop: {pred}")
        except ValueError:
            messagebox.showerror("Input Error", "Please fill all fields with valid numbers.")
        except Exception as e:
            messagebox.showerror("Prediction Error", f"Could not predict.\n\n{e}")

    get_btn = Button(btns, text="PREDICT", width=14,
                     font=("new times roman", 12, "bold"), fg="white", bg="#0f4d7d",
                     activebackground="#0f4d7d", cursor="hand2", bd=0,
                     command=predict_crop)
    get_btn.pack(side=LEFT, padx=20)

    clr_btn = Button(btns, text="CLEAR", width=10,
                     font=("new times roman", 12, "bold"), fg="white", bg="#0f4d7d",
                     activebackground="#0f4d7d", cursor="hand2", bd=0,
                     command=clear_all)
    clr_btn.pack(side=LEFT)

    return cp
