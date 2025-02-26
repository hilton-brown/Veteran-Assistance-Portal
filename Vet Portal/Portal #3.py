"""
Program: Veteran's Assistance Portal
Author: Hilton Brown
Date:
Description: This Python Tkinter application provides a GUI-based portal for veterans to schedule appointments, request assistance,
and access various veteran services. It includes user authentication, appointment scheduling, and request handling.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
from PIL import Image, ImageTk
import os

# ---------------------- Database Initialization ----------------------
def initialize_database():
    conn = sqlite3.connect("veteran_assistance.db")
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL,
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                      )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS assistance_requests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        assistance_type TEXT NOT NULL,
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                      )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                      )''')
    
    conn.commit()
    conn.close()

# Initialize the database
initialize_database()

# ---------------------- User Authentication ----------------------
def authenticate_user(username, password):
    conn = sqlite3.connect("veteran_assistance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and user[2] == password: 
        return user[0], user[1]  
    return None, None

# ---------------------- User Registration ----------------------
def register_user(username, password):
    conn = sqlite3.connect("veteran_assistance.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# ---------------------- Logout Function ----------------------
def logout():
    logout_screen = tk.Toplevel(root)
    logout_screen.title("Goodbye")
    logout_screen.geometry("400x300")
    
    # Load and display the goodbye image above the text
    try:
        goodbye_image = Image.open(r"C:\Users\hilto\OneDrive\Desktop\Vet Portal\goodbye screen.png")
        goodbye_image = goodbye_image.resize((100, 100), Image.Resampling.LANCZOS)
        goodbye_photo = ImageTk.PhotoImage(goodbye_image)
        
        # Create a label for the image and place it at the top
        goodbye_label = tk.Label(logout_screen, image=goodbye_photo)
        goodbye_label.image = goodbye_photo  
        goodbye_label.pack(pady=10) 
    except Exception as e:
        print(f"Error loading image: {e}")
    
    # Display Goodbye text in the same window
    message_label = tk.Label(logout_screen, text="Thank you for your service! Have a good day!", font=("Arial", 14))
    message_label.pack(pady=10)
    
    # Optional: Add a button to close the logout window
    close_button = tk.Button(logout_screen, text="Close", command=logout_screen.quit)
    close_button.pack(pady=20)

    # Close the window after a few seconds automatically if desired
    logout_screen.after(5000, logout_screen.quit)  

    logout_screen.mainloop()

# ---------------------- Home Screen ----------------------
def home_screen(user_id, user_name):
    home_screen = tk.Toplevel(root)
    home_screen.title("Welcome!")
    home_screen.geometry("400x300")
    
    # Welcome message
    welcome_label = tk.Label(home_screen, text=f"Welcome, {user_name}!", font=("Arial", 14))
    welcome_label.pack(pady=10)
    
    # Buttons
    services_button = tk.Button(home_screen, text="View Services & Assistance", command=show_services)
    services_button.pack(pady=10)
    
    schedule_button = tk.Button(home_screen, text="Schedule Appointment", command=lambda: schedule_appointment(user_id))
    schedule_button.pack(pady=10)
    
    assistance_button = tk.Button(home_screen, text="Request Assistance", command=lambda: request_assistance(user_id))
    assistance_button.pack(pady=10)
    
    logout_button = tk.Button(home_screen, text="Logout", command=logout)
    logout_button.pack(pady=10)

# ---------------------- Services & Assistance ----------------------
def show_services():
    service_window = tk.Toplevel(root)
    service_window.title("Available Services")
    service_window.geometry("400x300")
    
    services = [
        ("Medical Assistance", "Free healthcare for veterans with service-related disabilities."),
        ("Housing Support", "Help finding and securing affordable housing for veterans."),
        ("Job Assistance", "Career counseling and job placement services for veterans."),
        ("Disability Benefits", "Support in applying for disability benefits through VA.")
    ]
    
    for idx, (service, details) in enumerate(services):
        label = tk.Label(service_window, text=f"{service}: {details}", font=("Arial", 12))
        label.pack(pady=5)

# ---------------------- Appointment Scheduling ----------------------
def schedule_appointment(user_id):
    appointment_window = tk.Toplevel(root)
    appointment_window.title("Schedule Appointment")
    appointment_window.geometry("400x400")
    
    # Label
    label = tk.Label(appointment_window, text="Select a Date & Time for your Appointment", font=("Arial", 14))
    label.pack(pady=10)
    
    # Load and display the calendar image beneath the label
    try:
        calendar_image = Image.open(r"C:\Users\hilto\OneDrive\Desktop\Vet Portal\calendar.png") 
        calendar_image = calendar_image.resize((100, 100), Image.Resampling.LANCZOS)
        calendar_photo = ImageTk.PhotoImage(calendar_image)
        
        calendar_label = tk.Label(appointment_window, image=calendar_photo)
        calendar_label.image = calendar_photo 
        calendar_label.pack(pady=10)
    except Exception as e:
        print(f"Error loading image: {e}")
    
    # Date Picker
    date_picker = DateEntry(appointment_window, width=12, background='darkblue', foreground='white', borderwidth=2)
    date_picker.pack(pady=10)
    
    # Time Picker
    time_options = [f"{hour}:{minute:02d}" for hour in range(7, 17) for minute in [0, 30]]
    time_picker = ttk.Combobox(appointment_window, values=time_options)
    time_picker.pack(pady=10)
    
    # Submit Button
    submit_button = tk.Button(appointment_window, text="Submit Appointment", 
                              command=lambda: submit_appointment(appointment_window, date_picker.get(), time_picker.get(), user_id))
    submit_button.pack(pady=20)

# ---------------------- Appointment Submission ----------------------
def submit_appointment(window, selected_date, selected_time, user_id):
    conn = sqlite3.connect("veteran_assistance.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO appointments (date, time, user_id) VALUES (?, ?, ?)", (selected_date, selected_time, user_id))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Appointment Scheduled", f"Your appointment has been scheduled for {selected_date} at {selected_time}. Please arrive 30 minutes prior for check-in.")
    window.destroy()

# ---------------------- Assistance Request ----------------------
def request_assistance(user_id):
    assistance_window = tk.Toplevel(root)
    assistance_window.title("Request Assistance")
    assistance_window.geometry("400x300")
    
    # Request form
    label = tk.Label(assistance_window, text="Select the type of assistance you need:", font=("Arial", 12))
    label.pack(pady=20)
    
    # Load and display the assistance image beneath the label
    try:
        assistance_image = Image.open(r"C:\Users\hilto\OneDrive\Desktop\Vet Portal\assistance.png") 
        assistance_image = assistance_image.resize((100, 100), Image.Resampling.LANCZOS)
        assistance_photo = ImageTk.PhotoImage(assistance_image)
        
        assistance_label = tk.Label(assistance_window, image=assistance_photo)
        assistance_label.image = assistance_photo
        assistance_label.pack(pady=10)
    except Exception as e:
        print(f"Error loading image: {e}")
    
    # Assistance type dropdown
    assistance_type = ttk.Combobox(assistance_window, values=["Medical", "Housing", "Job", "Disability"])
    assistance_type.pack(pady=10)
    
    # Submit button
    submit_button = tk.Button(assistance_window, text="Submit Request", command=lambda: submit_request(assistance_window, assistance_type, user_id))
    submit_button.pack(pady=20)

# ---------------------- Request Submission ----------------------
def submit_request(window, assistance_type, user_id):
    selected_assistance = assistance_type.get()
    if selected_assistance:
        conn = sqlite3.connect("veteran_assistance.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO assistance_requests (assistance_type, user_id) VALUES (?, ?)", (selected_assistance, user_id))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Request Submitted", f"Your request for {selected_assistance} assistance has been submitted. Please allow 1-3 business days for a follow-up via email.")
        window.destroy()
    else:
        messagebox.showwarning("No Selection", "Please select a type of assistance.")

# ---------------------- Exit Application ----------------------
root = tk.Tk()
root.title("Login Screen")
root.geometry("500x400")

#  ---------------------- Load and Display Flag Image ----------------------
try:
    flag_image = Image.open(r"C:\Users\hilto\OneDrive\Desktop\Vet Portal\american_flag.jpg")
    flag_image = flag_image.resize((100, 60), Image.Resampling.LANCZOS)
    flag_photo = ImageTk.PhotoImage(flag_image)
    

    flag_label = tk.Label(root, image=flag_photo)
    flag_label.image = flag_photo  
    flag_label.grid(row=0, column=0, columnspan=2, pady=10)  
except Exception as e:
    print(f"Error loading image: {e}")

# ---------------------- Login Window ----------------------
def login_window():
    root.title("Login Screen")
    
    # Labels and Entry widgets
    username_label = tk.Label(root, text="Username:", font=("Arial", 12))
    username_label.grid(row=1, column=0, padx=10, pady=10)
    username_entry = tk.Entry(root, font=("Arial", 12))
    username_entry.grid(row=1, column=1, padx=10, pady=10)
    
    password_label = tk.Label(root, text="Password:", font=("Arial", 12))
    password_label.grid(row=2, column=0, padx=10, pady=10)
    password_entry = tk.Entry(root, font=("Arial", 12), show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=10)
    
    # Login function
    def on_login():
        username = username_entry.get()
        password = password_entry.get()
        user_id, user_name = authenticate_user(username, password)
        if user_id:
            home_screen(user_id, user_name)  # Navigate to home screen
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    
    # Login and Register Buttons
    login_button = tk.Button(root, text="Login", width=20, command=on_login)
    login_button.grid(row=3, column=0, columnspan=2, pady=10)
    
    register_button = tk.Button(root, text="Register", width=20, command=register_window)
    register_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    # Emergency Message at the bottom in red
    emergency_message = tk.Label(root, text="If this is an emergency, please close out of the application and dial 9-1-1", 
                                 font=("Arial", 10), fg="red")
    emergency_message.grid(row=5, column=0, columnspan=2, pady=10)

# ---------------------- Register Window ----------------------
def register_window():
    register_screen = tk.Toplevel(root)
    register_screen.title("Register")
    register_screen.geometry("400x300")
    
    # Labels and Entry widgets
    username_label = tk.Label(register_screen, text="Username:", font=("Arial", 12))
    username_label.pack(pady=10)
    username_entry = tk.Entry(register_screen, font=("Arial", 12))
    username_entry.pack(pady=5)
    
    password_label = tk.Label(register_screen, text="Password:", font=("Arial", 12))
    password_label.pack(pady=10)
    password_entry = tk.Entry(register_screen, font=("Arial", 12), show="*")
    password_entry.pack(pady=5)
    
    # Register function
    def on_register():
        username = username_entry.get()
        password = password_entry.get()
        register_user(username, password)
        messagebox.showinfo("Registration Success", "You have successfully registered!")
        register_screen.destroy()
    
    # Register Button
    register_button = tk.Button(register_screen, text="Register", width=20, command=on_register)
    register_button.pack(pady=10)

# ---------------------- Initialize Login Window ----------------------
login_window()

root.mainloop()
