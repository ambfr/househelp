


# 🏠 Home Maintenance Management System

A Python-based desktop application that connects residents with skilled workers for booking, managing, and completing household services.


## 📌 Project Overview

The **Home Maintenance Management System** is a desktop application developed using **Python**, **CustomTkinter**, and **SQLite**.  
It provides a simple and efficient platform for residents to book home services and for workers to manage and complete assigned jobs.

## 🎥 Project Demo

[▶ Watch the Project Demo](https://drive.google.com/file/d/16VEkJlhQyhVCTAZs71hNwJvaa88Lvp_o/view?usp=sharing)

## 🎯 Project Objective

The main objective of this project is to **simplify the booking and management of home maintenance services** by offering an easy-to-use, role-based system for residents and workers.


## 🛠 Technologies Used

- Python  
- CustomTkinter (GUI)  
- SQLite (Database)  
- Tkcalendar  
- Hashlib (for password security)


## 👥 User Roles & Features

### 🧑‍💼 Resident
- Signup and secure login  
- Book home services (Cleaning, Cooking, Plumbing, etc.)  
- Select service date and time slot  
- View previous bookings  
- Cancel pending bookings  
- Provide feedback and ratings after service completion  

### 👷 Worker
- Secure login  
- View pending bookings based on skills  
- Filter bookings by date range  
- Accept or decline service requests  
- View confirmed bookings  
- Mark jobs as completed  
- Reset password  


## ✨ Key Features

- Role-based authentication system  
- Secure password hashing  
- Service booking with calendar and time slots  
- Booking status tracking (Pending, Confirmed, Completed)  
- Feedback and rating system  
- SQLite database integration  
- Interactive and user-friendly GUI  


## 🗂 Database Tables

- `resident`  
- `worker`  
- `booking`  
- `feedback`  

## ▶ How to Run the Project

1. Install the required libraries:
   ```bash
   pip install customtkinter tkcalendar


2. Ensure the SQLite database file `househelp.db` exists with required tables.

3. Run the application:

   ```bash
   python main-hh.py
   ```



## 🚀 Future Enhancements

* Admin dashboard
* Worker availability management
* Notification system (Email/SMS)
* Online payment integration



## 📄 Conclusion

This project demonstrates the use of **Python GUI development**, **database management**, and **role-based access control** to build a real-world home maintenance management system.

