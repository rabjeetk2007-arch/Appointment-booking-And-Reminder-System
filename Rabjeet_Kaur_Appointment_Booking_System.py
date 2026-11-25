import sqlite3
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
conn = sqlite3.connect("appointments.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    time TEXT,
    purpose TEXT
)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    institution TEXT
)
""")
conn.commit()

root.title("Appointment Booking System")
root.geometry("500x550")
root.configure(bg="#eaf2f8")

title = tk.Label(
    root, text="User Registration",
    font=("Arial", 22, "bold"),
    bg="#eaf2f8", fg="#1a5276"
)
title.pack(pady=25)

def open_booking_window():
    booking = tk.Toplevel(root)
    booking.title("Book Appointment")
    booking.geometry("500x550")
    booking.configure(bg="#eaf2f8")

    tk.Label(
        booking, text="Book Your Appointment",
        font=("Arial", 20, "bold"),
        bg="#eaf2f8", fg="#1a5276"
    ).pack(pady=20)

    tk.Label(booking, text="Full Name", bg="#eaf2f8").pack()
    name = tk.Entry(booking, width=35)
    name.pack(pady=8)

    tk.Label(booking, text="Appointment Date (DD-MM-YYYY)", bg="#eaf2f8").pack()
    date = tk.Entry(booking, width=35)
    date.pack(pady=8)

    tk.Label(booking, text="Appointment Time", bg="#eaf2f8").pack()
    time = tk.Entry(booking, width=35)
    time.pack(pady=8)

    tk.Label(booking, text="Purpose", bg="#eaf2f8").pack()
    purpose = tk.Entry(booking, width=35)
    purpose.pack(pady=8)

    def save_appointment():
        if not name.get() or not date.get() or not time.get() or not purpose.get():
            messagebox.showerror("Error", "Please fill all fields")
            return

        cursor.execute("""
        INSERT INTO appointments (name, date, time, purpose)
        VALUES (?, ?, ?, ?)
        """, (name.get(), date.get(), time.get(), purpose.get()))
        conn.commit()
        messagebox.showinfo("Success", "Appointment Booked Successfully!")
        booking.destroy()

    tk.Button(
        booking, text="Book Appointment",
        font=("Arial", 12, "bold"),
        bg="#2874a6", fg="white",
        command=save_appointment
    ).pack(pady=25)

def register():
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    institution = institution_entry.get()

    if not name or not email or not phone or not institution:
        messagebox.showerror("Error", "Please fill all fields")
    else:
        cursor.execute(
            "INSERT INTO users (name, email, phone, institution) VALUES (?, ?, ?, ?)",
            (name, email, phone, institution)
        )
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        institution_entry.delete(0, tk.END)

def view_appointments():
    view = tk.Toplevel(root)
    view.title("All Appointments")
    view.geometry("650x500")
    view.configure(bg="#eaf2f8")

    tk.Label(
        view, text="All Booked Appointments",
        font=("Arial", 20, "bold"),
        bg="#eaf2f8", fg="#1a5276"
    ).pack(pady=20)

    appointment_list = tk.Listbox(view, width=75, height=12, font=("Arial", 10))
    appointment_list.pack(pady=10)

    cursor.execute("SELECT * FROM appointments")
    records = cursor.fetchall()

    for record in records:
        appointment_list.insert(
            tk.END,
            f"ID: {record[0]} | Name: {record[1]} | Date: {record[2]} | "
            f"Time: {record[3]} | Purpose: {record[4]}"
        )

    def cancel_appointment():
        selected = appointment_list.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select an appointment")
            return

        record = records[selected[0]]
        cursor.execute("DELETE FROM appointments WHERE id=?", (record[0],))
        conn.commit()
        messagebox.showinfo("Success", "Appointment Cancelled!")
        view.destroy()
        view_appointments()

    def update_appointment():
        selected = appointment_list.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select an appointment")
            return

        record = records[selected[0]]
        edit = tk.Toplevel(view)
        edit.title("Update Appointment")
        edit.geometry("400x400")
        edit.configure(bg="#eaf2f8")

        tk.Label(
            edit, text="Update Appointment",
            font=("Arial", 18, "bold"), bg="#eaf2f8"
        ).pack(pady=15)

        fields = {}
        for label, value in [
            ("Name", record[1]), ("Date", record[2]),
            ("Time", record[3]), ("Purpose", record[4])
        ]:
            tk.Label(edit, text=label, bg="#eaf2f8").pack()
            entry = tk.Entry(edit, width=30)
            entry.insert(0, value)
            entry.pack(pady=5)
            fields[label] = entry

        def save_update():
            values = [
                fields[x].get().strip()
                for x in ["Name", "Date", "Time", "Purpose"]
            ]
            if not all(values):
                messagebox.showerror("Error", "Fill all fields")
                return

            cursor.execute("""
                UPDATE appointments
                SET name=?, date=?, time=?, purpose=?
                WHERE id=?
            """, (*values, record[0]))
            conn.commit()
            messagebox.showinfo("Success", "Appointment Updated!")
            edit.destroy()
            view.destroy()
            view_appointments()

        tk.Button(
            edit, text="Save Changes",
            bg="#239b56", fg="white",
            command=save_update
        ).pack(pady=20)

    tk.Button(
        view, text="Cancel Selected Appointment",
        bg="#c0392b", fg="white",
        command=cancel_appointment
    ).pack(pady=10)

    tk.Button(
        view, text="Update Selected Appointment",
        bg="#2874a6", fg="white",
        command=update_appointment
    ).pack(pady=10)

def create_field(label_text):
    label = tk.Label(root, text=label_text, font=("Arial", 12), bg="#eaf2f8")
    label.pack(pady=5)
    entry = tk.Entry(root, width=35, font=("Arial", 12))
    entry.pack(pady=5)
    return entry

name_entry = create_field("Full Name")
email_entry = create_field("Email Address")
phone_entry = create_field("Phone Number")
institution_entry = create_field("Institution")

register_btn = tk.Button(
    root, text="Register",
    font=("Arial", 13, "bold"),
    bg="#2874a6", fg="white", width=20,
    command=register
)
register_btn.pack(pady=25)

tk.Button(
    root, text="Book Appointment",
    font=("Arial", 12, "bold"),
    bg="#239b56", fg="white",
    command=open_booking_window
).pack(pady=10)
tk.Button(
    root, text="View Appointments",
    font=("Arial", 12, "bold"),
    bg="#8e44ad", fg="white",
    command=view_appointments
).pack(pady=10)

root.mainloop()
