"""
Program: Veteran's Assistance Portal
Author: Hilton Brown
Date:
Description: This Python Tkinter application provides a GUI-based portal for veterans to schedule appointments, request assistance,
and access various veteran services. It includes user authentication, appointment scheduling, and request handling.
"""

import tkinter as tk  # Importing tkinter for GUI
from tkinter import messagebox  # Importing messagebox for pop-up notifications
from tkinter import ttk  # Importing ttk for styling widgets like comboboxes
from tkcalendar import DateEntry  # Importing DateEntry for calendar widget
import sqlite3  # Importing sqlite3 to interact with the database
from PIL import Image, ImageTk  # Importing PIL for image handling
import os  # Importing os for path handling

# ---------------------- Database Initialization ----------------------
def initialize_database():
    # Connecting to the SQLite database
    conn = sqlite3.connect("veteran_assistance.db")
    cursor = conn.cursor()  # Creating a cursor object to execute SQL queries
    
    # Creating the appointments table if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL,
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                      )''')
    
    # Creating the assistance_requests table if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS assistance_requests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        assistance_type TEXT NOT NULL,
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                      )''')
    
    # Creating the users table if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                      )''')
    
    conn.commit()  # Committing the changes to the database
    conn.close()  # Closing the database connection

# Initialize the database
initialize_database()  # Calling the function to initialize the database

# ---------------------- User Authentication ----------------------
def authenticate_user(username, password):
    # Connecting to the SQLite database to check user credentials
    conn = sqlite3.connect("veteran_assistance.db")
    cursor = conn.cursor()  # Creating a cursor to execute the SQL query
    
    # Querying the database to check if the username exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()  # Fetching the user record
    
    conn.close()  # Closing the database connection
    
    # Checking if the user exists and if the password matches
    if user and user[2] == password: 
        return user[0], user[1]  # Returning the user ID and username if credentials are correct
    return None, None  # Returning None if credentials are incorrect

# ---------------------- User Registration ----------------------
def register_user(username, password):
    # Connecting to the SQLite database to register a new user
    conn = sqlite3.connect("veteran_assistance.db")
    cursor = conn.cursor()  # Creating a cursor to execute the SQL query
    
    # Inserting a new user into the users table
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()  # Committing the changes to the database
    conn.close()  # Closing the database connection

# ---------------------- Logout Function ----------------------
def logout():
    # Creating a new window for the logout screen
    logout_screen = tk.Toplevel(root)
    logout_screen.title("Goodbye")  # Setting the title of the window
    logout_screen.geometry("400x300")  # Setting the size of the window
    
    # Attempting to load and display the goodbye image
    try:
        goodbye_image = Image.open(r"C:\Users\hilto\OneDrive\Desktop\Vet Portal\goodbye screen.png")
        goodbye_image = goodbye_image.resize((100, 100), Image.Resampling.LANCZOS)  # Resizing the image
        goodbye_photo = ImageTk.PhotoImage(goodbye_image)  # Converting the image to PhotoImage format
        
        # Creating a label to display the image
        goodbye_label = tk.Label(logout_screen, image=goodbye_photo)
        goodbye_label.image = goodbye_photo  # Storing a reference to the image to prevent garbage collection
        goodbye_label.pack(pady=10)  # Packing the label with padding
    except Exception as e:
        print(f"Error loading image: {e}")  # Printing an error message if the image fails to load
    
    # Creating a label to display the goodbye message
    message_label = tk.Label(logout_screen, text="Thank you for your service! Have a good day!", font=("Arial", 14))
    message_label.pack(pady=10)  # Packing the label with padding
    
    # Creating a button to close the logout screen
    close_button = tk.Button(logout_screen, text="Close", command=logout_screen.quit)
    close_button.pack(pady=20)  # Packing the button with padding

    # Closing the window automatically after 5 seconds
    logout_screen.after(5000, logout_screen.quit)  

    logout_screen.mainloop()  # Running the logout screen window loop

# ---------------------- Home Screen ----------------------
def home_screen(user_id, user_name):
    # Creating a new window for the home screen
    home_screen = tk.Toplevel(root)
    home_screen.title("Welcome!")  # Setting the title of the window
    home_screen.geometry("400x300")  # Setting the size of the window
    
    # Creating a label to display the welcome message
    welcome_label = tk.Label(home_screen, text=f"Welcome, {user_name}!", font=("Arial", 14))
    welcome_label.pack(pady=10)  # Packing the label with padding
    
    # Creating a button for viewing services and assistance
    services_button = tk.Button(home_screen, text="View Services & Assistance", command=show_services)
    services_button.pack(pady=10)  # Packing the button with padding
    
    # Creating a button for scheduling an appointment
    schedule_button = tk.Button(home_screen, text="Schedule Appointment", command=lambda: schedule_appointment(user_id))
    schedule_button.pack(pady=10)  # Packing the button with padding
    
    # Creating a button for requesting assistance
    assistance_button = tk.Button(home_screen, text="Request Assistance", command=lambda: request_assistance(user_id))
    assistance_button.pack(pady=10)  # Packing the button with padding
    
    # Creating a button for logging out
    logout_button = tk.Button(home_screen, text="Logout", command=logout)
    logout_button.pack(pady=10)  # Packing the button with padding

# ---------------------- Services & Assistance ----------------------
def show_services():
    # Creating a new window for displaying available services
    service_window = tk.Toplevel(root)
    service_window.title("Available Services")  # Setting the title of the window
    service_window.geometry("400x300")  # Setting the size of the window
    
    # List of services and their details
    services = [
        ("Medical Assistance", "Free healthcare for veterans with service-related disabilities."),
        ("Housing Support", "Help finding and securing affordable housing for veterans."),
        ("Job Assistance", "Career counseling and job placement services for veterans."),
        ("Disability Benefits", "Support in applying for disability benefits through VA.")
    ]
    
    # Displaying each service in the service window
    for idx, (service, details) in enumerate(services):
        label = tk.Label(service_window, text=f"{service}: {details}", font=("Arial", 12))
        label.pack(pady=5)  # Packing the label with padding

# ---------------------- Appointment Scheduling ----------------------
def schedule_appointment(user_id):
    # Creating a new window for scheduling an appointment
    appointment_window = tk.Toplevel(root)
    appointment_window.title("Schedule Appointment")  # Setting the title of the window
    appointment_window.geometry("400x400")  # Setting the size of the window
    
    # Creating a label for the date and time selection
    label = tk.Label(appointment_window, text="Select a Date & Time for your Appointment", font=("Arial", 14))
    label.pack(pady=10)  # Packing the label with padding
    
    # Attempting to load and display the calendar image
    try:
        calendar_image = Image.open(r"C:\Users\hilto\OneDrive\Desktop\Vet Portal\calendar.png")
        calendar_image = calendar_image.resize((100, 100), Image.Resampling.LANCZOS)  # Resizing the image
        calendar_photo = ImageTk.PhotoImage(calendar_image)  # Converting the image to PhotoImage format
        
        # Creating a label to display the image
        calendar_label = tk.Label(appointment_window, image=calendar_photo)
        calendar_label.image = calendar_photo  # Storing a reference to the image to prevent garbage collection
        calendar_label.pack(pady=10)  # Packing the label with padding
    except Exception as e:
        print(f"Error loading image: {e}")  # Printing an error message if the image fails to load
    
    # Creating a date picker widget
    date_picker = DateEntry(appointment_window, width=12, background='darkblue', foreground='white', borderwidth=2)
    date_picker.pack(pady=10)  # Packing the date picker with padding
    
    # Creating a time picker widget with available time options
    time_options = [f"{hour}:{minute:02d}" for hour in range(7, 17) for minute in [0, 30]]
    time_picker = ttk.Combobox(appointment_window, values=time_options)
    time_picker.pack(pady=10)  # Packing the time picker with padding
    
    # Creating a button to submit the appointment
    submit_button = tk.Button(appointment_window, text="Submit Appointment", 
                              command=lambda: submit_appointment(appointment_window, date_picker.get(), time_picker.get(), user_id))
    submit_button.pack(pady=20)  # Packing the button with padding

# ---------------------- Appointment Submission ----------------------
def submit_appointment(window, selected_date, selected_time, user_id):
    # Connecting to the SQLite database to submit the appointment
    conn = sqlite3.connect("veteran_assistance.db")
    cursor = conn.cursor()  # Creating a cursor to execute the SQL query
    
    # Inserting the appointment into the appointments table
    cursor.execute("INSERT INTO appointments (date, time, user_id) VALUES (?, ?, ?)", (selected_date, selected_time, user_id))
    conn.commit()  # Committing the changes to the database
    conn.close()  # Closing the database connection
    
    # Displaying a message to confirm the appointment has been scheduled
    messagebox.showinfo("Appointment Scheduled", f"Your appointment has been scheduled for {selected_date} at {selected_time}. Please arrive 30 minutes prior for check-in.")
    window.destroy()  # Closing the appointment window

# ---------------------- Assistance Request ----------------------
def request_assistance(user_id):
    # Creating a new window for requesting assistance
    assistance_window = tk.Toplevel(root)
    assistance_window.title("Request Assistance")  # Setting the title of the window
    assistance_window.geometry("400x300")  # Setting the size of the window
    
    # Creating a label to prompt the user for selecting an assistance type
    label = tk.Label(assistance_window, text="Select the type of assistance you need:", font=("Arial", 12))
    label.pack(pady=20)  # Packing the label with padding
    
    # Attempting to load and display the assistance image
    try:
        assistance_image = Image.open(r"C:\Users\hilto\OneDrive\Desktop\Vet Portal\assistance.png")
        assistance_image = assistance_image.resize((100, 100), Image.Resampling.LANCZOS)  # Resizing the image
        assistance_photo = ImageTk.PhotoImage(assistance_image)  # Converting the image to PhotoImage format
        
        # Creating a label to display the image
        assistance_label = tk.Label(assistance_window, image=assistance_photo)
        assistance_label.image = assistance_photo  # Storing a reference to the image to prevent garbage collection
        assistance_label.pack(pady=10)  # Packing the label with padding
    except Exception as e:
        print(f"Error loading image: {e}")  # Printing an error message if the image fails to load
    
    # Creating a dropdown for selecting the assistance type
    assistance_type = ttk.Combobox(assistance_window, values=["Medical", "Housing", "Job", "Disability"])
    assistance_type.pack(pady=10)  # Packing the dropdown with padding
    
    # Creating a button to submit the assistance request
    submit_button = tk.Button(assistance_window, text="Submit Request", command=lambda: submit_request(assistance_window, assistance_type, user_id))
    submit_button.pack(pady=20)  # Packing the button with padding

# ---------------------- Request Submission ----------------------
def submit_request(window, assistance_type, user_id):
    selected_assistance = assistance_type.get()  # Getting the selected assistance type
    if selected_assistance:  # If an assistance type was selected
        # Connecting to the SQLite database to submit the request
        conn = sqlite3.connect("veteran_assistance.db")
        cursor = conn.cursor()  # Creating a cursor to execute the SQL query
        
        # Inserting the assistance request into the assistance_requests table
        cursor.execute("INSERT INTO assistance_requests (assistance_type, user_id) VALUES (?, ?)", (selected_assistance, user_id))
        conn.commit()  # Committing the changes to the database
        conn.close()  # Closing the database connection
        
        # Displaying a message to confirm the request has been submitted
        messagebox.showinfo("Request Submitted", f"Your request for {selected_assistance} assistance has been submitted. Please allow 1-3 business days for a follow-up via email.")
        window.destroy()  # Closing the assistance window
    else:
        # If no assistance type was selected, show a warning message
        messagebox.showwarning("No Selection", "Please select a type of assistance.")

# ---------------------- Exit Application ----------------------
root = tk.Tk()  # Creating the root window
root.title("Login Screen")  # Setting the title of the window
root.geometry("500x400")  # Setting the size of the window

#  ---------------------- Load and Display Flag Image ----------------------
try:
    flag_image = Image.open(r"C:\Users\hilto\OneDrive\Desktop\Vet Portal\american_flag.jpg")
    flag_image = flag_image.resize((100, 60), Image.Resampling.LANCZOS)  # Resizing the flag image
    flag_photo = ImageTk.PhotoImage(flag_image)  # Converting the image to PhotoImage format

    # Creating a label to display the flag image
    flag_label = tk.Label(root, image=flag_photo)
    flag_label.image = flag_photo  # Storing a reference to the image to prevent garbage collection
    flag_label.grid(row=0, column=0, columnspan=2, pady=10)  # Displaying the image on the window
except Exception as e:
    print(f"Error loading image: {e}")  # Printing an error message if the image fails to load

# ---------------------- Login Window ----------------------
def login_window():
    root.title("Login Screen")  # Setting the title of the login screen
    
    # Creating labels and entry widgets for the username and password
    username_label = tk.Label(root, text="Username:", font=("Arial", 12))
    username_label.grid(row=1, column=0, padx=10, pady=10)  # Displaying the username label
    username_entry = tk.Entry(root, font=("Arial", 12))  # Entry widget for the username
    username_entry.grid(row=1, column=1, padx=10, pady=10)  # Displaying the username entry widget
    
    password_label = tk.Label(root, text="Password:", font=("Arial", 12))
    password_label.grid(row=2, column=0, padx=10, pady=10)  # Displaying the password label
    password_entry = tk.Entry(root, font=("Arial", 12), show="*")  # Entry widget for the password
    password_entry.grid(row=2, column=1, padx=10, pady=10)  # Displaying the password entry widget

    # Creating the login button
    login_button = tk.Button(root, text="Login", font=("Arial", 12),
                             command=lambda: login_action(username_entry.get(), password_entry.get()))
    login_button.grid(row=3, column=0, columnspan=2, pady=20)  # Displaying the login button

    # Creating the register button
    register_button = tk.Button(root, text="Register", font=("Arial", 12), command=register_window)
    register_button.grid(row=4, column=0, columnspan=2, pady=10)  # Displaying the register button

#  ---------------------- Register Window ----------------------
def register_window():
    root.title("Register Screen")  # Setting the title of the register screen

    # Creating labels and entry widgets for the username and password
    username_label = tk.Label(root, text="Username:", font=("Arial", 12))
    username_label.grid(row=1, column=0, padx=10, pady=10)  # Displaying the username label
    username_entry = tk.Entry(root, font=("Arial", 12))  # Entry widget for the username
    username_entry.grid(row=1, column=1, padx=10, pady=10)  # Displaying the username entry widget

    password_label = tk.Label(root, text="Password:", font=("Arial", 12))
    password_label.grid(row=2, column=0, padx=10, pady=10)  # Displaying the password label
    password_entry = tk.Entry(root, font=("Arial", 12), show="*")  # Entry widget for the password
    password_entry.grid(row=2, column=1, padx=10, pady=10)  # Displaying the password entry widget

    # Creating the register button
    register_button = tk.Button(root, text="Register", font=("Arial", 12),
                                command=lambda: register_action(username_entry.get(), password_entry.get()))
    register_button.grid(row=3, column=0, columnspan=2, pady=20)  # Displaying the register button

    # Creating the login button
    login_button = tk.Button(root, text="Back to Login", font=("Arial", 12), command=login_window)
    login_button.grid(row=4, column=0, columnspan=2, pady=10)  # Displaying the back-to-login button

#  ---------------------- Handle Login Action ----------------------
def login_action(username, password):
    user_id, user_name = authenticate_user(username, password)
    if user_id:
        root.withdraw()  # Hiding the login window
        home_screen(user_id, user_name)  # Navigating to the home screen
    else:
        messagebox.showerror("Login Error", "Invalid username or password. Please try again.")  # Error message for failed login

# ---------------------- Start the GUI ----------------------
login_window()  # Calling the function to display the login screen
root.mainloop()  # Starting the tkinter event loop

# ---------------------- End of the Program ----------------------

