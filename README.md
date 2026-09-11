# Python Bank Management System + Jenkins DevOps project


# 🏦 Bank Management System – Python + Jenkins CI

A simple **Bank Management System** developed using Python and
Object-Oriented Programming (OOP).

This project is also integrated with **Jenkins** to demonstrate a basic
Continuous Integration (CI) workflow.

---

## 📌 Project Overview

The Bank Management System provides basic banking operations through a
console-based Python application.

### Banking Features

- Create a bank account
- Login using account number
- Deposit money
- Withdraw money
- Check account balance
- Calculate interest for Savings Account
- Logout
- Exit the application

---

## 🛠️ Technologies Used

- **Python 3.14**
- **Object-Oriented Programming (OOP)**
- **Jenkins**
- **Git & GitHub**
- **Windows**
- **Command Prompt / VS Code**

---

## 📂 Project Structure

```text
Bank_Project/
│
├── banking/
│   ├── __init__.py
│   ├── account.py
│   └── transactions.py
│
├── main.py
├── README.md
└── Jenkinsfile
````

---

## 🏗️ Application Architecture

```text
                 Bank Management System
                          │
                          ▼
                       main.py
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
        account.py             transactions.py
              │                       │
              └───────────┬───────────┘
                          ▼
                    Banking Operations
```

---

# 🚀 Running the Project Locally

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Go into the project directory:

```bash
cd Bank_Project
```

---

## 2. Check Python Installation

```bash
python --version
```

Expected output:

```text
Python 3.14.x
```

---

## 3. Run the Application

```bash
python main.py
```

The application displays:

```text
======== WELCOME to SBI Bank ==========

1. Create Account
2. Login
3. Exit

Enter your choice:
```

---

# 🔧 Jenkins CI Setup

Jenkins is used to automate the project build and validation process.

## Jenkins Workflow

```text
Developer
    │
    ▼
GitHub Repository
    │
    ▼
Jenkins
    │
    ▼
Checkout Source Code
    │
    ▼
Python Compilation
    │
    ▼
Automated Tests
    │
    ▼
Build SUCCESS / FAILURE
```

---

## Jenkins Configuration

### Step 1 – Create Jenkins Job

Create a new Jenkins job:

```text
Bank_Project
```

Job type:

```text
Freestyle Project
```

---

## Step 2 – Configure Python

Jenkins uses the Python executable installed on the Windows system.

Example:

```text
C:\Users\rohit\AppData\Local\Python\pythoncore-3.14-64\python.exe
```

---

## Step 3 – Jenkins Build Step

The current Jenkins build validates the Python source files using:

```bat
cd C:\Users\rohit\Desktop\Bank_Project

"C:\Users\rohit\AppData\Local\Python\pythoncore-3.14-64\python.exe" --version

"C:\Users\rohit\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m py_compile main.py banking\account.py banking\transactions.py

echo Python project compilation successful
```

### Expected Jenkins Output

```text
Python 3.14.x
Python project compilation successful

Finished: SUCCESS
```

---

# 🧪 Testing

The project will be extended with automated testing using **pytest**.

Planned CI workflow:

```text
Source Code
     │
     ▼
Jenkins
     │
     ▼
Install Dependencies
     │
     ▼
Compile Python Files
     │
     ▼
Run Pytest
     │
     ▼
Test Results
     │
     ▼
Jenkins SUCCESS
```

---

# 📈 DevOps Implementation

This project demonstrates the following DevOps concepts:

* Git version control
* GitHub repository management
* Jenkins installation and configuration
* Jenkins agents
* Continuous Integration
* Automated build validation
* Python project compilation
* Automated testing
* Jenkins build history
* CI pipeline documentation

---

# 🔄 Future Improvements

The project can be improved by adding:

* [ ] Automated pytest test cases
* [ ] Jenkinsfile Pipeline
* [ ] GitHub integration
* [ ] Automatic Jenkins builds after GitHub commits
* [ ] Requirements management
* [ ] Test result publishing
* [ ] Code quality checks
* [ ] Docker containerization
* [ ] Jenkins Pipeline automation
* [ ] Deployment stage

---

# 📸 Jenkins Proof

Screenshots can be added to this repository to demonstrate the Jenkins
implementation.

Recommended screenshots:

```text
screenshots/
│
├── jenkins-dashboard.png
├── jenkins-job.png
├── jenkins-build-success.png
└── jenkins-console-output.png
```

These screenshots demonstrate the Jenkins job configuration and
successful CI execution.

---

# 🎯 Project Objective

The main objective of this project is to develop a Python-based banking
application while gaining practical experience with **DevOps and
Continuous Integration using Jenkins**.

The project demonstrates how source code can be validated automatically
through a Jenkins CI workflow.

---

# 👨‍💻 Author

**Rohit Bilwal**

Python Developer | DevOps Engineer – Fresher

---

## ⭐ Key Skills Demonstrated

```text
Python
OOP
Git
GitHub
Jenkins
Continuous Integration
CI/CD Fundamentals
Automated Testing
Linux/Windows Command Line
DevOps Practices
```

---

## 📄 License

This project is created for learning and educational purposes.

````

### One important change

Because MY project is **Python**, don't create the `Jenkinsfile` yet. We will create it in the next phase after your Jenkins build and pytest test are working.

For now, save the above as:

```text
Bank_Project/README.md
````

Then we'll add **pytest + Jenkins testing**, and after that create the real `Jenkinsfile`.
## 📸 Jenkins Proof

### Jenkins Dashboard

![Jenkins Dashboard](screenshots/jenkins-dashboard.png)

### Jenkins Build Success

![Jenkins Build Success](screenshots/jenkins-build-success.png)

### Jenkins Console Output

![Jenkins Console Output](screenshots/jenkins-console-output.png)
