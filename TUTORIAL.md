# Project Setup and Local Running Tutorial

This guide explains how to set up and run the backend and frontend services for this project on your local machine.

## Prerequisites

*   **Python** (version 3.8+ recommended) and **pip**
*   **Node.js** (version 16+ recommended) and **npm**
*   **Git** (for cloning the repository if you haven't already)

## Backend Setup (Django)

1.  **Navigate to the Backend Directory:**
    ```bash
    cd backend
    ```

2.  **Create and Activate a Virtual Environment:**
    *   It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    ```
    *   Activate the environment:
        *   On macOS/Linux:
            ```bash
            source venv/bin/activate
            ```
        *   On Windows:
            ```bash
            .\venv\Scripts\activate
            ```

3.  **Install Dependencies:**
    *   Ensure `requirements.txt` is up-to-date (it should now include `django-cors-headers` and `python-decouple`).
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables (.env file):**
    *   The backend uses `python-decouple` to manage settings. Create a `.env` file in the `backend/` directory.
    *   You'll need to define at least the `SECRET_KEY` and `FERNET_KEY`. You can generate these:
        *   `SECRET_KEY`: Use a Django secret key generator (many online tools available, or use Python: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
        *   `FERNET_KEY`: Generate using Python: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
    *   Your `.env` file should look something like this:
        ```env
        SECRET_KEY=your_django_secret_key_here
        DEBUG=True
        FERNET_KEY=your_fernet_key_here
        # Add other settings like database credentials if not using SQLite default
        # DB_ENGINE=django.db.backends.postgresql
        # DB_NAME=your_db_name
        # DB_USER=your_db_user
        # DB_PASSWORD=your_db_password
        # DB_HOST=localhost
        # DB_PORT=5432
        ```
    *   **Important Security Note:** The `FERNET_KEY` is used for encrypting sensitive patient data. Keep it secure. If you lose it or change it, previously encrypted data will not be decipherable.

5.  **Run Database Migrations:**
    *   This will create the necessary database tables based on your models. The default is SQLite.
    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser (Optional but Recommended):**
    *   This allows access to the Django admin interface.
    ```bash
    python manage.py createsuperuser
    ```
    *   Follow the prompts to set a username, email, and password.

7.  **Run the Backend Development Server:**
    ```bash
    python manage.py runserver
    ```
    *   By default, this will run on `http://localhost:8000`. The API will be accessible at `http://localhost:8000/api/`.

## Frontend Setup (React + Vite)

1.  **Navigate to the Frontend Directory:**
    *   Open a new terminal window/tab.
    ```bash
    cd frontend
    ```

2.  **Install Dependencies:**
    ```bash
    npm install
    ```

3.  **Run the Frontend Development Server:**
    ```bash
    npm run dev
    ```
    *   This will typically start the server on `http://localhost:5173` (Vite's default). Check your terminal output for the exact URL.

## Accessing the Application

1.  Once both backend and frontend servers are running:
    *   Open your web browser.
    *   Navigate to the frontend URL (usually `http://localhost:5173`).

2.  You should see the login page. You can:
    *   Register a new user via the backend's registration endpoint if you implemented one and integrated it (check `backend/usuarios/urls.py` for a `/register/` path).
    *   Or, if you created a superuser, you can use those credentials to log in if the `/api/token/` endpoint is used by the frontend login form. (Note: The frontend `Login.jsx` uses `/api/token/` which is standard for JWT, so superuser credentials should work).

## Important Notes

*   **CORS:** The backend is configured with `django-cors-headers`. `settings.py` should allow `http://localhost:5173` (or your frontend's port). If you encounter CORS errors, double-check `CORS_ALLOWED_ORIGINS` or `CORS_ALLOW_ALL_ORIGINS` in `backend/core/settings.py`.
*   **API Base URL:** The frontend's `api.js` is configured to point to `http://localhost:8000/api`. Ensure your backend server is running on port 8000.
*   **Troubleshooting:**
    *   Check terminal outputs for both frontend and backend for any error messages.
    *   Use your browser's developer tools (Network tab and Console) to inspect API requests and responses.
