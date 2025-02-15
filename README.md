# **ESN Buddy Program** 🎓🌍

## **Overview**  
The **ESN Buddy Program** is a web-based application designed to facilitate the matching of international students (buddies) with local ESN members (ESNers). This system helps incoming exchange students integrate smoothly by connecting them with experienced local students who share similar interests, languages, and faculties.  

The platform provides **admin** and **manager** functionalities to oversee registrations, manage users, and generate reports.  

---

## **Features** 🚀  

✅ **User Authentication & Roles**  
- Admins and managers can log in securely.  
- Role-based access control (RBAC) ensures only authorized users can access specific features.  

✅ **Buddy & ESNer Registration**  
- Students can register as a **Buddy** (exchange student) or an **ESNer** (mentor).  
- Registration fields include **name, nationality, languages, faculty, interests**, and more.  

✅ **Automated Matching System**  
- Uses a **scoring algorithm** based on shared **languages, interests, faculty, and gender preferences**.  
- Ensures a balanced and personalized matching process.  

✅ **Admin & Manager Functionalities**  
- View and manage registered users.  
- Add or remove admins and managers.  
- Export all registrations in an **Excel file**.  
- **Batch delete** all data after export (for GDPR compliance).  

✅ **Data Export & Backup**  
- Generate and **download an Excel report** containing all registered Buddies and ESNers.  

✅ **Secure Authentication & Session Management**  
- Secure password hashing using **Werkzeug’s password hash functions**.  
- Session management to persist admin logins.  

✅ **Email Notifications**  
- Send confirmation emails upon registration and notifications for matches and unmatches.

---

## **Installation & Setup** 🔧  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/Horghe20/ESN-Buddy-Program.git
cd ESN-Buddy-Program
```
### **2️⃣ Create a Virtual Environment (Recommended)**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **4️⃣ Set Up Environment Variables**
modify the utils/config.py file
- Add your database
- Add your email info

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **5️⃣  Run the Application**
```bash
python app.py
```

---

## **Usage Guide** 📚  

### **User Roles & Authentication**  
- Admins log in via `/auth/login`.  
- After logging in, they can access the **Admin Dashboard** at `/admin/index`.  
- Admins can **add**, **remove**, or **update** managers and other admins.  

### **Buddy & ESNer Registration**  
- New users register through dedicated endpoints.  
- The system **automatically matches** Buddies and ESNers based on compatibility.  

### **Export & Data Management**  
- Admins can **export** all user data as an Excel file (`.xlsx`).  
- Optionally, admins can **delete all data** after export.  

---

## **Project Structure** 📝  
```
ESN-Buddy-Program/
│── app.py                 # Application entry point
│── database/
│   ├── db.py              # Database connection
│   └── tables.py          # ORM models
│── controller/
│   ├── auth.py            # Authentication & session management
│   ├── registration.py    # Buddy & ESNer registration logic
│   ├── admin.py           # Admin functionalities
│   └── match.py           # Matching functionalities
│── utils/
│   ├── match.py           # Match calculation utilities
|   ├── populated_database.py # Dummy data generation
|   ├── config.py          # Configuration settings
│   ├── email_service.py   # Email notification service
│   └── options.json       # Configuration options
│── static/                # Static files (CSS, JS, images)
│── templates/             # HTML templates for frontend
│── tests/                 # Unit & integration tests
│── requirements.txt       # Dependencies
│── nixpacks.toml          # Configuration file for Nixpacks deployment
│── README.md              # Documentation
```

---

## **Matching Algorithm** 🔍  
The **matching system** assigns a compatibility score based on:  
✔️ **Languages Spoken** (higher weight)  
✔️ **Shared Interests**  
✔️ **Faculty**  
✔️ **Gender Preferences**  

The system ensures **optimal pairings** while maintaining fairness and balancing the number of available ESNers and Buddies.

---

## **Security Considerations** 🔒  
🔹 **Password Hashing:** Secure storage with `werkzeug.security.generate_password_hash()`  
🔹 **Role-Based Access Control (RBAC):** Only authorized users can access admin routes  
🔹 **Session Management:** Prevents unauthorized access  
🔹 **Input Validation:** Sanitization of user input to prevent SQL injection & XSS  

---

## **Contributing** 🤝  
1. **Fork the Repository**  
2. **Create a Feature Branch**  
   ```bash
   git checkout -b feature-branch-name
   ```
3. **Make Changes & Commit**  
   ```bash
   git commit -m "Description of changes"
   ```
4. **Push Changes**  
   ```bash
   git push origin feature-branch-name
   ```
5. **Submit a Pull Request** 🎉  

---

## **License** 📝  
This project is licensed under the **MIT License** – feel free to use and modify it!  

---


## **Contact & Support** 📩  
For issues or feature requests, open an issue on GitHub or contact the **ESN team**!  

📧 **Support Email:** giorgiodicristofalo77@gmail.com 

