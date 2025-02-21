import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import calendar
from datetime import datetime

# Create the main application window
root = tk.Tk()
root.title("Veteran Assistance Portal")
root.geometry("500x450")

# Function to show detailed services
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

# Function to show appointment scheduling window
def schedule_appointment():
    appointment_window = tk.Toplevel(root)
    appointment_window.title("Schedule Appointment")
    appointment_window.geometry("400x300")
    
    # Add a label for scheduling
    label = tk.Label(appointment_window, text="Select a Date for your Appointment", font=("Arial", 14))
    label.pack(pady=20)
    
    # Add a Calendar to select a date
    current_date = datetime.now()
    cal = calendar.TextCalendar(calendar.SUNDAY)
    month_year = current_date.strftime("%B %Y")
    month_view = cal.monthdayscalendar(current_date.year, current_date.month)
    
    month_label = tk.Label(appointment_window, text=month_year, font=("Arial", 12))
    month_label.pack(pady=10)
    
    # Display the calendar in text format
    for week in month_view:
        week_str = " ".join([f"{day:2}" if day != 0 else "  " for day in week])
        week_label = tk.Label(appointment_window, text=week_str)
        week_label.pack()

    # Submit Button
    submit_button = tk.Button(appointment_window, text="Submit Appointment", command=lambda: submit_appointment(appointment_window))
    submit_button.pack(pady=20)

# Function to handle appointment submission
def submit_appointment(window):
    # Simple prompt for confirmation
    date_selected = simpledialog.askstring("Appointment", "Please enter the date you wish to schedule (DD/MM/YYYY):")
    if date_selected:
        messagebox.showinfo("Appointment Scheduled", f"Your appointment has been scheduled for {date_selected}.")
        window.destroy()

# Function to show request assistance form
def request_assistance():
    assistance_window = tk.Toplevel(root)
    assistance_window.title("Request Assistance")
    assistance_window.geometry("400x300")
    
    # Request form
    label = tk.Label(assistance_window, text="Select the type of assistance you need:", font=("Arial", 12))
    label.pack(pady=20)
    
    assistance_type = ttk.Combobox(assistance_window, values=["Medical", "Housing", "Job", "Disability"])
    assistance_type.pack(pady=10)
    
    # Submit button
    submit_button = tk.Button(assistance_window, text="Submit Request", command=lambda: submit_request(assistance_window, assistance_type))
    submit_button.pack(pady=20)

# Function to handle request submission
def submit_request(window, assistance_type):
    selected_assistance = assistance_type.get()
    if selected_assistance:
        messagebox.showinfo("Request Submitted", f"Your request for {selected_assistance} assistance has been submitted.")
        window.destroy()
    else:
        messagebox.showwarning("No Selection", "Please select a type of assistance.")

# Function to close the application
def exit_app():
    messagebox.showinfo("Goodbye", "Thank you for your service, have a good day!")
    root.quit()

# Create the main screen with buttons
welcome_label = tk.Label(root, text="Welcome to the Veteran Assistance Portal", font=("Arial", 16))
welcome_label.pack(pady=20)

services_button = tk.Button(root, text="View Services", width=20, command=show_services)
services_button.pack(pady=10)

appointment_button = tk.Button(root, text="Schedule Appointment", width=20, command=schedule_appointment)
appointment_button.pack(pady=10)

request_button = tk.Button(root, text="Request Assistance", width=20, command=request_assistance)
request_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", width=20, command=exit_app)
exit_button.pack(pady=20)

# Emergency message at the bottom of the start screen
emergency_label = tk.Label(root, text="If this is an emergency, please exit and dial 911", font=("Arial", 10), fg="red")
emergency_label.pack(side="bottom", pady=10)

# Run the main event loop
root.mainloop()






