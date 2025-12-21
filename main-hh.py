import customtkinter as ctk
import sqlite3
import hashlib
from tkcalendar import Calendar
from tkinter import messagebox
from datetime import date

# Hashing function for password security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Database connection
def connect_to_db():
    return sqlite3.connect('househelp.db')  # Change the path as needed 

# Function to initialize the database and create tables if they don't exist
def initialize_database():
    conn = connect_to_db()
    cursor = conn.cursor()
    
    
    conn.commit()
    conn.close()

# Function to show a back button
def create_back_button(frame, command):
    ctk.CTkButton(master=frame, text="Back", command=command, width=150).place(x=10, y=10)


# Function to create the menu

# Function for worker login window
def login_worker(user_type):
    

    login_label = ctk.CTkLabel(content_frame, text=f"{user_type.capitalize()} Login", font=("Arial", 24, "bold"))
    login_label.place(relx=0.5, rely=0.1, anchor="center")

    username_var = ctk.StringVar()
    password_var = ctk.StringVar()

    ctk.CTkLabel(content_frame, text="Username",font=( "Arial",18)).place(x=150, y=150)
    ctk.CTkEntry(content_frame, textvariable=username_var, width=250).place(x=300, y=150)

    ctk.CTkLabel(content_frame, text="Password", font=( "Arial",18)).place(x=150, y=200)
    ctk.CTkEntry(content_frame, textvariable=password_var, show='*', width=250).place(x=300, y=200)

    ctk.CTkButton(content_frame, text="Login", command=lambda: wauthenticate(username_var, password_var), width=150).place(x=300, y=270)

   
     # Back button to go back to login options
    ctk.CTkButton(content_frame, text="Back", command=lambda: show_frame("login_options"), width=20, height=40).place(x=50, y=350)

def reset_password():
    # Clear the content area
    for widget in content_frame.winfo_children():
        widget.destroy()

    create_back_button(content_frame, create_worker_menu)
    ctk.CTkLabel(content_frame, text="Reset Password", font=("Arial", 20, "bold")).place(x=200, y=10)

    conn = connect_to_db()  # Assuming this function connects to your database
    cursor = conn.cursor()

    # Variables to hold old and new password
    old_password_var = ctk.StringVar()
    new_password_var = ctk.StringVar()

    # UI Elements for old and new password input
    ctk.CTkLabel(content_frame, text="Old password:").place(x=50, y=100)
    old_password_entry = ctk.CTkEntry(content_frame, textvariable=old_password_var, width=250, show="*")
    old_password_entry.place(x=160, y=100)

    ctk.CTkLabel(content_frame, text="New password:").place(x=50, y=150)
    new_password_entry = ctk.CTkEntry(content_frame, textvariable=new_password_var, width=250, show="*")
    new_password_entry.place(x=160, y=150)

    # Button to submit and change the password
    ctk.CTkButton(content_frame, text="Change Password", command=lambda: change_password(old_password_var, new_password_var)).place(x=160, y=250)

    # Close the connection when done
    conn.close()

def change_password(old_password_var, new_password_var):
    conn = connect_to_db()  
    cursor = conn.cursor()
    
    old_password = old_password_var.get().strip()  # Remove leading/trailing spaces
    new_password = new_password_var.get().strip()  # Remove leading/trailing spaces

    # Check if old password or new password is empty or just spaces
    if not old_password or not new_password:
        messagebox.showerror("Error", "Password cannot be empty or just spaces.")
        return

    # SQL query to check if the old password exists
    cursor.execute("SELECT * FROM worker WHERE username = ? AND password_hash = ?", (logged_in_username, old_password))
    result = cursor.fetchone()

    if result:
        # Old password exists, update with new password
        cursor.execute("UPDATE worker SET password_hash = ? WHERE password_hash = ? AND username = ?", (new_password, old_password, logged_in_username))
        conn.commit()
        # Show success message box
        messagebox.showinfo("Success", "Password successfully changed!")
        old_password_var.set("")
        new_password_var.set("")

    else:
        # Old password not found, show error message box
        messagebox.showerror("Error", "Old password is incorrect.")
        old_password_var.set("")
        new_password_var.set("")
    conn.close()


# Function to authenticate worker login
def wauthenticate(username_var, password_var):
    username = username_var.get().strip()
    password_hash = password_var.get().strip()

    if not all([username, password_hash]):
        messagebox.showerror("Error", "Fields cannot be empty.")
        return

    conn = connect_to_db()
    cursor = conn.cursor()

    # Authenticate the worker without password hashing
    cursor.execute('''SELECT worker_id, skills FROM worker WHERE username = ? AND password_hash = ?''', 
                   (username, password_hash))
    result = cursor.fetchone()

    if result:
        global worker_id, worker_skills, logged_in_username, logged_in_password
        worker_id = result[0]
        worker_skills = result[1]  # Store worker skills
        logged_in_username = username
        logged_in_password = password_hash
        messagebox.showinfo("Login Successful", "Welcome back!")
        create_worker_menu()  # Navigate to worker dashboard
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password.")
    
    conn.close()

# Function to create the post-login menu for workers
def create_worker_menu():
    # Clear the content area
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Title label
    title_label = ctk.CTkLabel(master=content_frame, text="Worker Portal", font=("Arial", 24, "bold"))
    title_label.place(relx=0.5, rely=0.1, anchor="center")

    # My Jobs button
    my_jobs_btn = ctk.CTkButton(master=content_frame, text="My Jobs", width=150)
    my_jobs_btn.place(relx=0.5, rely=0.3, anchor="center")

    # Logout button
    logout_btn = ctk.CTkButton(master=content_frame, text="Logout", width=150, command=show_login_options)
    logout_btn.place(relx=0.5, rely=0.4, anchor="center")

# Function to show different frames based on navigation
def show_frame(frame_name):
    # Clear the content area
    for widget in content_frame.winfo_children():
        widget.destroy()

    if frame_name == "home":
        show_home_with_start()
    elif frame_name == "login":
        login("resident")
    elif frame_name == "login_worker":
        login_worker("worker")
    elif frame_name == "signup":
        signup()
    elif frame_name == "login_options":
        show_login_options()


# Function to display the home screen
def show_home_with_start():
    clear_content_frame()  # Clear previous content

    title_label = ctk.CTkLabel(master=content_frame, text="Home Maintenance", font=("Arial", 30, "bold"))
    title_label.place(relx=0.5, rely=0.3, anchor="center")

    desc_label = ctk.CTkLabel(master=content_frame, text="Simplify your Home Upkeep", font=("Arial", 16))
    desc_label.place(relx=0.5, rely=0.4, anchor="center")

    start_button = ctk.CTkButton(content_frame, text="Start", command=lambda: show_frame("login_options"))
    start_button.place(relx=0.5, rely=0.6, anchor="center")

# Function to show login/signup options
def show_login_options():
    clear_content_frame()  # Clear previous content
    ctk.CTkLabel(content_frame, text="Login as Resident or Worker", font=("Arial", 20,"bold")).place(relx=0.5, rely=0.2, anchor="center")

    ctk.CTkButton(content_frame, text="Resident Login", command=lambda: show_frame("login"), width=20, height=40).place(x=150, y=200)
    ctk.CTkButton(content_frame, text="Worker Login", command=lambda: show_frame("login_worker"), width=20, height=40).place(x=350, y=200)
    ctk.CTkButton(content_frame, text="  Signup  ", command=lambda: show_frame("signup"), width=20, height=40).place(x=550, y=200)

    # Back button to go back to home screen
    ctk.CTkButton(content_frame, text="  Back  ", command=lambda: show_frame("home"), width=20, height=40).place(x=50, y=350)




# Function to clear the content frame before loading new content
def clear_content_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()

# Function for signup window
def signup():
    signup_label = ctk.CTkLabel(content_frame, text="Resident Signup", font=("Arial", 24, "bold"))
    signup_label.place(relx=0.5, rely=0.1, anchor="center")

    # Entry fields for signup
    name_var = ctk.StringVar()
    email_var = ctk.StringVar()
    phone_var = ctk.StringVar()
    address_var = ctk.StringVar()
    username_var = ctk.StringVar()
    password_var = ctk.StringVar()

    ctk.CTkLabel(content_frame, text="Name").place(x=150, y=80)
    ctk.CTkEntry(content_frame, textvariable=name_var, width=250).place(x=350, y=80)

    ctk.CTkLabel(content_frame, text="Email").place(x=150, y=120)
    ctk.CTkEntry(content_frame, textvariable=email_var, width=250).place(x=350, y=120)

    ctk.CTkLabel(content_frame, text="Phone Number").place(x=150, y=160)
    ctk.CTkEntry(content_frame, textvariable=phone_var, width=250).place(x=350, y=160)

    ctk.CTkLabel(content_frame, text="Address").place(x=150, y=200)
    ctk.CTkEntry(content_frame, textvariable=address_var, width=250).place(x=350, y=200)

    ctk.CTkLabel(content_frame, text="Username").place(x=150, y=240)
    ctk.CTkEntry(content_frame, textvariable=username_var, width=250).place(x=350, y=240)

    ctk.CTkLabel(content_frame, text="Password").place(x=150, y=280)
    ctk.CTkEntry(content_frame, textvariable=password_var, show='*', width=250).place(x=350, y=280)

    ctk.CTkButton(content_frame, text="Signup", command=lambda: register_user(name_var, email_var, phone_var, address_var, username_var, password_var)).place(x=300, y=320)

     # Back button to go back to login options
    ctk.CTkButton(content_frame, text="Back", command=lambda: show_frame("login_options"), width=20, height=40).place(x=50, y=350)

# Function to handle user registration
def register_user(name_var, email_var, phone_var, address_var, username_var, password_var):
    # Get input values
    name = name_var.get().strip()
    email = email_var.get().strip()
    phone_number = phone_var.get().strip()
    address = address_var.get().strip()
    username = username_var.get().strip()
    password = password_var.get().strip()

    # Check for empty strings
    if not all([name, email, phone_number, address, username, password]):
        messagebox.showerror("Error", "Fields cannot be empty or contain only spaces.")
        return

    password_hash = hash_password(password)  # Hash the password

    conn = connect_to_db()  # Connect to your existing database
    cursor = conn.cursor()

    try:
        cursor.execute('''INSERT INTO resident (name, email, phone_number, address, username, password_hash)
                          VALUES (?, ?, ?, ?, ?, ?)''', (name, email, phone_number, address, username, password_hash))
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists. Please choose a different one.")
    finally:
        conn.close()

# Function for login window
def login(user_type):
    # Clear any previous content on the frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    login_label = ctk.CTkLabel(content_frame, text=f"{user_type.capitalize()} Login", font=("Arial", 24, "bold"))
    login_label.place(relx=0.5, rely=0.1, anchor="center")

    username_var = ctk.StringVar()
    password_var = ctk.StringVar()

    ctk.CTkLabel(content_frame, text="Username", font=("Arial", 18)).place(x=150, y=150)
    ctk.CTkEntry(content_frame, textvariable=username_var, width=250).place(x=300, y=150)

    ctk.CTkLabel(content_frame, text="Password", font=("Arial", 18)).place(x=150, y=200)
    ctk.CTkEntry(content_frame, textvariable=password_var, show='*', width=250).place(x=300, y=200)

    # Login button
    ctk.CTkButton(content_frame, text="Login", command=lambda: rauthenticate(username_var, password_var), width=150).place(x=300, y=270)

    

    # Back button to go back to login options
    ctk.CTkButton(content_frame, text="  Back  ", command=lambda: show_frame("login_options"), width=20, height=40).place(x=50, y=370)


# Function to authenticate resident user login
def rauthenticate(username_var, password_var):
    username = username_var.get().strip()
    password = password_var.get().strip()

    # Check for empty strings
    if not all([username, password]):
        messagebox.showerror("Error", "Fields cannot be empty or contain only spaces.")
        return
    password_hash = hash_password(password)  # Hash the entered password

    conn = connect_to_db()  # Connect to your existing database
    cursor = conn.cursor()

    cursor.execute('''SELECT resident_id, address FROM resident WHERE username = ? AND password_hash = ?''', (username, password_hash))
    result = cursor.fetchone()

    if result:
        global resident_id, user_address  # Use global variables to store
        resident_id = result[0]  # Get resident_id
        user_address = result[1]  # Get address
        messagebox.showinfo("Login Successful", "Welcome back!")
        create_resident_menu()  # Show resident-specific menu with buttons
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password.")  # Updated message

    conn.close()  # Close the database connection

# Function to create the post-login menu for residents
def create_resident_menu():
    # Clear the content area
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Title label
    title_label = ctk.CTkLabel(master=content_frame, text="Welcome to Home Maintenance", font=("Arial", 24, "bold"))
    title_label.place(relx=0.5, rely=0.1, anchor="center")

    # Book Service button
    book_service_btn = ctk.CTkButton(master=content_frame, text="Book Service", width=150, command=book_service)
    book_service_btn.place(relx=0.5, rely=0.3, anchor="center")

    # My Bookings button
    my_bookings_btn = ctk.CTkButton(master=content_frame, text="My Bookings", width=150, command= my_bookings)
    my_bookings_btn.place(relx=0.5, rely=0.4, anchor="center")

    # Logout button
    logout_btn = ctk.CTkButton(master=content_frame, text="Logout", width=150, command=show_login_options)
    logout_btn.place(relx=0.5, rely=0.6, anchor="center")

    global register_user  # Make sure resident_username is globally available after login


# Function to show book service page
def book_service():
    for widget in content_frame.winfo_children():
        widget.destroy()

    create_back_button(content_frame, create_resident_menu)

    # Service dropdown
    ctk.CTkLabel(content_frame, text="Select Service").place(x=50, y=50)
    service_var = ctk.StringVar()
    service_options = ["Cleaning", "Cooking", "Plumbing", "Electrician", "Gardening","Carpentry"]
    ctk.CTkOptionMenu(content_frame, variable=service_var, values=service_options).place(x=200, y=50)

    # Calendar for date selection (disable past dates)
    ctk.CTkLabel(content_frame, text="Select Date").place(x=50, y=100)
    today = date.today()
    cal = Calendar(content_frame, selectmode='day', mindate=today)
    cal.place(x=200, y=100)

    # Time slot dropdown
    ctk.CTkLabel(content_frame, text="Select Time Slot").place(x=50, y=250)
    time_var = ctk.StringVar()
    time_options = ["9 AM - 11 AM", "11 AM - 1 PM", "1 PM - 3 PM", "3 PM - 5 PM", "5 PM - 6 PM"]
    ctk.CTkOptionMenu(content_frame, variable=time_var, values=time_options).place(x=200, y=250)

    # Confirm button
    ctk.CTkButton(content_frame, text="Confirm Booking", command=lambda: confirm_booking(service_var, cal, time_var)).place(x=200, y=300)


# Function to handle booking confirmation
def confirm_booking(service_var, cal, time_var):
    service_type = service_var.get()  # Get service type from dropdown
    booking_date = cal.get_date()  # Get date from calendar (YYYY-MM-DD format)
    booking_time = time_var.get()  # Get time slot from dropdown

    if not all([service_type, booking_date, booking_time]):
        messagebox.showerror("Error", "All fields must be filled.")
        return

    # Convert the time slot to a standard time format, e.g., 9 AM - 11 AM -> '09:00'
    time_mapping = {
        "9 AM - 11 AM": "09:00",
        "11 AM - 1 PM": "11:00",
        "1 PM - 3 PM": "13:00",
        "3 PM - 5 PM": "15:00",
        "5 PM - 6 PM": "17:00"
    }
    booking_time_standard = time_mapping.get(booking_time)

    conn = connect_to_db()
    cursor = conn.cursor()

    # Insert booking into the database with the new date and time columns
    cursor.execute('''
        INSERT INTO booking (resident_id, service_type, booking_date, booking_time, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (resident_id, service_type, booking_date, booking_time_standard, 'pending'))

    # Get the booking ID of the last inserted record
    booking_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Display a confirmation message with the booking ID
    messagebox.showinfo("Booking Confirmed", f"Your booking (ID: {booking_id}) for {service_type} on {booking_date} at {booking_time} has been confirmed.")
def my_bookings():
    for widget in content_frame.winfo_children():
        widget.destroy()

    create_back_button(content_frame, create_resident_menu)

    ctk.CTkLabel(content_frame, text="My Previous Bookings", font=("Arial", 20)).place(x=200, y=10)

    conn = connect_to_db()
    cursor = conn.cursor()

    # Fetch previous bookings for the logged-in resident, including booking_id, service_type, date, time, and status
    cursor.execute('''
        SELECT booking_id, service_type, booking_date, booking_time, status
        FROM booking
        WHERE resident_id = ?
        ORDER BY booking_id DESC
    ''', (resident_id,))
    previous_bookings = cursor.fetchall()

    conn.close()

    # Display the fetched bookings with booking ID, service type, date, time, and status
    if previous_bookings:
        for idx, booking in enumerate(previous_bookings):
            booking_id, service_type, booking_date, booking_time, status = booking

            # Y-coordinate for each booking row
            y_position = 60 + idx * 100

            ctk.CTkLabel(content_frame, text=f"Booking ID: {booking_id} - {service_type} on {booking_date} at {booking_time}, Status: {status}").place(x=50, y=y_position)

            # Show delete button only if the task is not completed
            if status != 'completed':
                delete_button = ctk.CTkButton(content_frame, text="Delete",
                                              command=lambda b_id=booking_id: delete_booking(b_id))
                delete_button.place(x=500, y=y_position)

            # Show feedback button if the status is completed
            if status == 'completed':
                feedback_button = ctk.CTkButton(content_frame, text="Give Feedback",
                                                command=lambda b_id=booking_id, idx=idx: show_feedback_form(b_id, resident_id, idx))
                feedback_button.place(x=500, y=y_position + 30)  # Adjust the feedback button placement

    else:
        ctk.CTkLabel(content_frame, text="No bookings found.", font=("Arial", 16)).place(x=50, y=60)
def delete_booking(booking_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Delete the booking
    cursor.execute('''
        DELETE FROM booking
        WHERE booking_id = ?
    ''', (booking_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Deleted", "Booking deleted successfully.")

    # Refresh the bookings list
    my_bookings()

def show_feedback_form(booking_id, resident_id, idx):
    # Clear previous feedback fields (if any)
    for widget in content_frame.winfo_children():
        if hasattr(widget, "is_feedback_form"):
            widget.destroy()

    conn = connect_to_db()
    cursor = conn.cursor()

    # Check if feedback already exists for this booking
    cursor.execute('''
        SELECT comments, rating FROM feedback WHERE booking_id = ?
    ''', (booking_id,))
    feedback = cursor.fetchone()

    conn.close()

    # Calculate the Y-position for the feedback form based on the booking row index
    feedback_y_position = 150 + idx * 100

    # If feedback exists, show it and disable further submission
    if feedback:
        comments, rating = feedback
        feedback_text = f"Feedback already given: {comments}, Rating: {rating}/5"
        ctk.CTkLabel(content_frame, text=feedback_text, font=("Arial", 12)).place(x=70, y=feedback_y_position)
    else:
        # Allow feedback submission
        feedback_label = ctk.CTkLabel(content_frame, text="Provide Feedback:", font=("Arial", 12))
        feedback_label.is_feedback_form = True
        feedback_label.place(x=50, y=feedback_y_position)

        # Comments input
        comments_entry = ctk.CTkEntry(content_frame, width=300, placeholder_text="Enter your comments")
        comments_entry.is_feedback_form = True
        comments_entry.place(x=50, y=feedback_y_position + 30)

        # Rating input (1 to 5)
        rating_entry = ctk.CTkEntry(content_frame, width=100, placeholder_text="Rating (out of 5)")
        rating_entry.is_feedback_form = True
        rating_entry.place(x=370, y=feedback_y_position + 30)

        # Submit Button with correct resident_id passed
        submit_button = ctk.CTkButton(content_frame, text="Submit Feedback", 
                                      command=lambda: submit_feedback(booking_id, resident_id, comments_entry.get(), rating_entry.get()))
        submit_button.is_feedback_form = True
        submit_button.place(x=500, y=feedback_y_position + 30)

def submit_feedback(booking_id, resident_id, comments, rating):
    # Validate rating input
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            messagebox.showerror("Invalid Input", "Rating should be between 1 and 5.")
            return
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for rating.")
        return

    # Insert feedback into the database
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO feedback (booking_id, resident_id, comments, rating)
        VALUES (?, ?, ?, ?)
    ''', (booking_id, resident_id, comments, rating))

    conn.commit()
    conn.close()

    # Show success message and refresh the bookings UI
    messagebox.showinfo("Success", "Thank you for your feedback!")
    
    # Refresh the bookings to update the UI
    my_bookings
# Function for worker dashboard after login
def create_worker_menu():
    # Clear the content area
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Title label
    title_label = ctk.CTkLabel(master=content_frame, text="Worker Portal", font=("Arial", 24, "bold"))
    title_label.place(relx=0.5, rely=0.1, anchor="center")

    # Pending Bookings button
    pending_btn = ctk.CTkButton(master=content_frame, text="Pending Bookings", width=150, command=show_pending_bookings)
    pending_btn.place(relx=0.5, rely=0.3, anchor="center")

    # Confirmed Bookings button
    confirmed_btn = ctk.CTkButton(master=content_frame, text="Confirmed Bookings", width=150, command=show_confirmed_bookings)
    confirmed_btn.place(relx=0.5, rely=0.4, anchor="center")

    # Logout button
    logout_btn = ctk.CTkButton(master=content_frame, text="Logout", width=150, command=show_login_options)
    logout_btn.place(relx=0.5, rely=0.6, anchor="center")

    reset_btn = ctk.CTkButton(master=content_frame, text="Reset Password", width=150, command=reset_password)
    reset_btn.place(relx=0.5, rely=0.5, anchor="center")

from tkcalendar import DateEntry

from datetime import date

def show_pending_bookings():
    # Clear the content area
    for widget in content_frame.winfo_children():
        widget.destroy()

    create_back_button(content_frame, create_worker_menu)

    # Display the title
    ctk.CTkLabel(content_frame, text="Pending Bookings", font=("Arial", 20, "bold")).place(x=200, y=10)

    # Set today as the minimum selectable date
    today = date.today()

    # Add date range filter with past dates disabled
    ctk.CTkLabel(content_frame, text="From:").place(x=50, y=50)
    start_date = DateEntry(content_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern="mm/dd/yy", mindate=today)
    start_date.place(x=100, y=50)

    ctk.CTkLabel(content_frame, text="To:").place(x=250, y=50)
    end_date = DateEntry(content_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern="mm/dd/yy", mindate=today)
    end_date.place(x=300, y=50)

    # Add filter button
    ctk.CTkButton(content_frame, text="Filter", command=lambda: apply_filter(start_date.get(), end_date.get())).place(x=450, y=50)

def apply_filter(start_date, end_date):
    # Debugging: print the dates to ensure they are captured correctly
    print(f"Filtering from {start_date} to {end_date}")  # You can remove this later

    # Clear the content area to refresh with filtered data
    for widget in content_frame.winfo_children():
        widget.destroy()

    create_back_button(content_frame, create_worker_menu)

    # Display the title
    ctk.CTkLabel(content_frame, text="Filtered Pending Bookings", font=("Arial", 20, "bold")).place(x=200, y=10)

    conn = connect_to_db()
    cursor = conn.cursor()

    # Query to fetch bookings within the specified date range (adjust the format as MM/DD/YY)
    cursor.execute('''
        SELECT booking_id, resident_id, service_type, booking_date, booking_time
        FROM booking 
        WHERE service_type = ? 
        AND status = 'pending'
        AND booking_date BETWEEN ? AND ?
    ''', (worker_skills, start_date, end_date))
    
    pending_bookings = cursor.fetchall()
    conn.close()

    # Display the filtered pending bookings
    if pending_bookings:
        for idx, booking in enumerate(pending_bookings):
            booking_id, resident_id, service_type, booking_date, booking_time = booking
            ctk.CTkLabel(content_frame, text=f"Booking ID: {booking_id}, Service: {service_type}, Date: {booking_date}, Time: {booking_time}").place(x=50, y=60 + idx * 50)

            # Accept Button
            ctk.CTkButton(content_frame, text="Accept", command=lambda b_id=booking_id: accept_booking(b_id)).place(x=300, y=85 + idx * 50)

            # Decline Button
            ctk.CTkButton(content_frame, text="Decline", command=lambda b_id=booking_id: decline_booking(b_id)).place(x=500, y=85 + idx * 50)
    else:
        ctk.CTkLabel(content_frame, text="No pending bookings matching your skills and date range.", font=("Arial", 16)).place(x=50, y=60)

def accept_booking(booking_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Update the booking status to "confirmed" for this booking
    cursor.execute('''
        UPDATE booking 
        SET status = 'confirmed', worker_id = ? 
        WHERE booking_id = ?
    ''', (worker_id, booking_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", f"Booking {booking_id} has been accepted.")
    show_pending_bookings()  # Refresh the pending bookings

def decline_booking(booking_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Update the booking status to "declined" for this booking
    cursor.execute('''
        UPDATE booking 
        SET status = 'declined'
        WHERE booking_id = ?
    ''', (booking_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Declined", f"Booking {booking_id} has been declined.")
    show_pending_bookings()  # Refresh the pending bookings

import tkinter as tk
from tkinter import messagebox

def show_confirmed_bookings():
    # Clear the content area
    for widget in content_frame.winfo_children():
        widget.destroy()

    create_back_button(content_frame, create_worker_menu)

    # Display the title
    ctk.CTkLabel(content_frame, text="Confirmed Bookings", font=("Arial", 20, "bold")).place(x=200, y=10)

    conn = connect_to_db()
    cursor = conn.cursor()

    # Fetch confirmed bookings assigned to the worker
    cursor.execute('''
        SELECT booking_id, service_type, booking_date, booking_time
        FROM booking 
        WHERE worker_id = ? AND status = 'confirmed'
    ''', (worker_id,))
    confirmed_bookings = cursor.fetchall()

    conn.close()

    # Display the confirmed bookings
    if confirmed_bookings:
        for idx, booking in enumerate(confirmed_bookings):
            booking_id, service_type, booking_date, booking_time = booking
            details = f"Date: {booking_date}, Time: {booking_time}"
            ctk.CTkLabel(content_frame, text=f"Booking ID: {booking_id}, Service: {service_type}, {details}").place(x=50, y=60 + idx * 40)

            # Mark as Completed Button
            ctk.CTkButton(content_frame, text="Mark as Completed", command=lambda b_id=booking_id: complete_booking(b_id)).place(x=400, y=60 + idx * 40)

          
    else:
        ctk.CTkLabel(content_frame, text="No confirmed bookings.", font=("Arial", 16)).place(x=50, y=60)

def complete_booking(booking_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Update the booking status to "completed"
    cursor.execute('''
        UPDATE booking 
        SET status = 'completed'
        WHERE booking_id = ?
    ''', (booking_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", f"Booking {booking_id} has been marked as completed.")

    # After marking as completed, prompt for feedback
   
    show_confirmed_bookings()  # Refresh the confirmed bookings



# Main window initialization
app = ctk.CTk()
app.geometry('800x600')

# Content frame for displaying the dynamic content
content_frame = ctk.CTkFrame(app, width=800, height=550)
content_frame.place(x=0, y=50)

# Initialize the database
initialize_database()


# Show the home screen by default
show_frame("home")

# Start the Tkinter main loop
app.mainloop()
