# CS-458 Project Part 3

## 📘 Overview

This project is submitted for **CS458 - Software Verification and Validation** (2024-2025 Spring).  
It is a **responsive full-stack web application** developed using the **Test-Driven Development (TDD)** methodology.

### ✅ Key Features

- **Backend**: FastAPI (Python)
- **Frontend**: TypeScript + React
- **Testing**: Pytest (backend), Jest + React Testing Library (frontend)
- **Screens**:
  - Login Page
  - Survey Page
  - Custom Survey Builder (with conditional logic and multiple question types)

---

## 🚀 Getting Started

### 🔧 Backend Setup (FastAPI)

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:

   **macOS/Linux:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```

   - Runs at: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 🌐 Frontend Setup (React + TypeScript)

1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   or alternatively
   ```bash
   npm install
   ```

4. Start the development server:
   ```bash
   npm run dev   # or: npm start
   ```

   - Runs at: [http://localhost:3000](http://localhost:3000)

---

### Running the test cases

```bash
cd selenium/project_3
pip install selenium
```
## Running Singular Test File

  # Windows
  ```bash
   python test1.py  
   python test2.py
   ...
   python test20.py
   ```
  # Macos/Linux
  ```bash
   python3.10 test1.py  
   python3.10 test2.py
   ...
   python3.10 test20.py
   ```
## Running All Test File

  # Windows
  ```bash
   python run_tests.py  
   ```
  # Macos/Linux
  ```bash
   python3 run_tests.py
   ```

---
