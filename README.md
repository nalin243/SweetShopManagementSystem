
---

# Sweet Shop Management System

### **Overview**

The **Sweet Shop Management System** is a full-stack web application built using **FastAPI (Python)** for the backend and **React** for the frontend.
It provides an end-to-end solution to manage sweets inventory, user authentication, and purchasing workflows with both **user** and **admin** privileges.

This project demonstrates strong software engineering practices, including:

* **Test-Driven Development (TDD)**
* **RESTful API design**
* **Modern frontend architecture**
* **Secure authentication using JWT**
* **AI-assisted development transparency**

---

## Features

### **User Roles**

* **Regular User:**

  * Add,Browse, search, and purchase sweets.
* **Admin:**

  * Update, delete, and restock sweets.

### **Core Functionality**

#### Authentication (JWT)

* `POST /api/auth/signup` — Register a new user
* `POST /api/auth/login` — Log in and receive an access token

#### Sweets Management (Protected)

* `GET /sweets` — View all sweets
* `GET /sweets/search` — Search sweets by name, category, or price
* `POST /sweet` — Add a new sweet
* `PUT /sweets/{id}` — Update sweet details *(Admin only)*
* `DELETE /sweets/{id}` — Delete a sweet *(Admin only)*

#### Inventory Operations

* `POST /sweets/{id}/purchase` — Purchase a sweet (reduce quantity)
* `POST /sweets/{id}/restock` — Restock sweets *(Admin only)*

---

## Tech Stack

### **Backend**

* FastAPI
* MongoDB (via Motor)
* PyJWT
* Pydantic
* Pytest

### **Frontend**

* React 18 + Vite
* Axios
* React Router
* TailwindCSS

---

## Project Setup

### **Clone the Repository**

```
git clone https://github.com/nalin243/SweetShopManagementSystem.git
cd SweetShopManagementSystem
```

---

### **Backend Setup**

**Navigate**

```
cd backend
```

**Create Virtual Environment**

```
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

**Install Dependencies**

```
pip install -r requirements.txt
```

**Run the Server**

```
uvicorn app.main:app --reload
```

Backend runs at: **[http://localhost:8000](http://localhost:8000)**

---

### **Frontend Setup**

**Navigate**

```
cd frontend
```

**Install Dependencies**

```
npm install
```

**Configure Environment Variables**

```
VITE_API_URL=http://localhost:8000
```

**Run the Frontend**

```
npm run dev
```

Frontend runs at: **[http://localhost:5173](http://localhost:5173)**

---

## Testing (TDD Approach)

* Follow the **Red → Green → Refactor** cycle.
* Write unit and integration tests before implementing features.
* Run all tests:

  ```
  pytest -v        # Python backend
  npm test            # React frontend
  ```

**Test Coverage Targets**

* Authentication
* Sweets CRUD operations
* Purchase and restock

---

## Directory Structure

```
sweet-shop-management-system/
│
├── backend/
│   ├── app/
│   │   ├── api/                # Routes and service for sweets api
│   │   ├── auth/               # Routes and service for authentication logic
│   │   ├── core/               # Configuration
│   │   ├── users/              # Routes and service for users
│   │   └── main.py             # FastAPI entrypoint
│   ├── tests/                  # Pytest cases
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/         # UI components
│   │   ├── pages/              # React pages
│   │   ├── api/                # Axios API handlers
│   │   ├── context/            # Auth & global state
│   │   └── main.jsx
│   ├── public/
│   └── package.json
│
└── README.md
```

---

## My AI Usage

### **Tools Used**

* **ChatGPT (OpenAI)** — Backend and frontend debugging, endpoint brainstorming and test case writing

### **How I Used AI**

* I used AI for boilerplate code generation as well as general debugging. I also used it to write test cases and to write code that I otherwise knew and would just take up time typing it out.
  I double checked all the code and made sure I knew what it was doing. I also made the AI explain some parts I was unfamiliar with. 

---

## Screenshots

<img width="1898" height="892" alt="registerpage" src="https://github.com/user-attachments/assets/1d47d8b1-4485-461b-b4d2-fff81cc9ae51" />
<img width="1668" height="863" alt="loginpage" src="https://github.com/user-attachments/assets/150547d7-6744-428d-a418-0472f3386d7a" />
<img width="1908" height="892" alt="dashboarduser" src="https://github.com/user-attachments/assets/ca0b1c08-73c9-41a2-8125-e2677cd46ada" />
<img width="1907" height="919" alt="dashboardadmin" src="https://github.com/user-attachments/assets/c2be584c-e79f-42da-88b1-051a2d37b41b" />
<img width="1822" height="873" alt="addmodal" src="https://github.com/user-attachments/assets/91e92e8c-f7b9-40e4-99d5-279c567a792d" />

## Tests Coverage

<img width="1905" height="549" alt="backendtest" src="https://github.com/user-attachments/assets/9b73e50b-e959-48b7-918c-86415b5c01df" />
<img width="1110" height="567" alt="frontendtest" src="https://github.com/user-attachments/assets/dbc736dd-e2e6-40e4-97d1-f0f0637502c1" />

---
