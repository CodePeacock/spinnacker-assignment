# Contact App

This project is a simple contact management application consists of a backend built with Flask and a frontend built with Create React App.

## Prerequisites

- Node.js v18.18.0 and npm 10.2.5 (for the frontend)
- Python 3.11.5+(for the backend)
- MySQL 9.0 (for the database)

## Getting Started

### Backend

1. **Navigate to the backend directory & create a virtual environment:**

    ```sh
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2. **Install the required Python packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the environment variables:**

    Create a `.env` file in the root of `backend` directory and add the necessary environment variables. For example:

    ```env
    DATABASE_URL=mysql+mysqlconnector://username:password@db/db_name
    SECRET_KEY=your_secret_key
    EMAIL_USER=your_gmail_account@gmail.com (or any other email provider with SMTP)
    EMAIL_PASSWORD=your_gmail_app_password (or your email account password)
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    FLASK_APP=run.py
    FLASK_ENV=development

    ```

5. **Run the backend server:**

    ```sh
    cd app
    python run.py
    ```

### Frontend

1. **Navigate to the frontend directory:**

    ```sh
    cd frontend
    ```

2. **Install the required npm packages:**

    ```sh
    npm install
    ```

3. **Run the frontend development server:**

    ```sh
    npm start
    ```

    Open [http://localhost:3000](http://localhost:3000) to view it in your browser. The page will reload when you make changes. You may also see any lint errors in the console.
