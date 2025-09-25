

# Centralized Real-Time KPI Dashboard

A full-stack, role-based KPI dashboard application built with React and Flask. It provides a secure, real-time, and responsive interface for visualizing data from sources like Google Ads and Google Analytics.

## ✨ Core Features

  - **Role-Based Access Control**: Tailored dashboard views for **Admin**, **Marketing**, and **Finance** roles.
  - **Real-Time Data Visualization**: Interactive and responsive charts powered by **Chart.js**.
  - **Secure JWT Authentication**: Stateless and secure user authentication and session management.
  - **RESTful API**: A well-structured backend API with comprehensive error handling and role-based data fetching.
  - **Data Caching**: In-memory caching with a 5-minute TTL to boost performance and reduce redundant data fetching.
  - **Responsive, Modern UI**: A sleek, dark-themed interface that looks great on all devices.
  - **Mock Data Simulation**: Built-in services to simulate realistic data from Google Ads and Analytics for development.

-----

## 🛠️ Technology Stack

| Area      | Technology                                                                                                    |
| :-------- | :------------------------------------------------------------------------------------------------------------ |
| **Backend** | **Python 3.8+**, **Flask**, **Flask-SQLAlchemy**, **Flask-JWT-Extended**, **Flask-CORS** |
| **Frontend** | **React 18** (with Hooks), **Vite**, **React Router**, **Chart.js**, **Axios** |
| **Database** | **SQLite** (for Development), **MySQL** (for Production)                                                      |
| **Styling** | Modern CSS with a responsive, mobile-first approach                                                         |

-----

## 🚦 Getting Started

Follow these instructions to get the project running on your local machine for development and testing.

### Prerequisites

  - **Python 3.8+** and `pip`
  - **Node.js 16+** and `npm`
  - **Git**

### 1\. Clone the Repository

First, clone the project to your local machine:

```bash
git clone <your-repository-url>
cd KPI
```

### 2\. Backend Setup (Flask)

1.  **Navigate to the backend directory:**

    ```bash
    cd backend
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    ```bash
    # On macOS/Linux
    cp .env.example .env

    # On Windows
    copy .env.example .env
    ```

    *The default `.env` is pre-configured to use SQLite, so no other database setup is needed for development.*

5.  **Initialize and seed the database:**
    This command will create the database tables and populate them with the demo users.

    ```bash
    # This is a hypothetical command, you may need to create a seed script.
    python seed.py 
    ```

6.  **Run the Flask application:**

    ```bash
    flask run
    ```

    The backend server will start on `http://127.0.0.1:5000`.

### 3\. Frontend Setup (React)

1.  **Navigate to the frontend directory (from the root):**

    ```bash
    cd frontend
    ```

2.  **Install Node.js dependencies:**

    ```bash
    npm install
    ```

3.  **Start the development server:**

    ```bash
    npm run dev
    ```

    The frontend will be available at `http://localhost:5173`.

-----

## 👤 Usage & Demo Accounts

Once both the backend and frontend servers are running, open your browser to `http://localhost:5173`. You can log in with one of the pre-configured demo accounts to explore the different role-based dashboards.

| Role        | Email                   | Password     | Access Level                                |
| :---------- | :---------------------- | :----------- | :------------------------------------------ |
| **Admin** | `admin@company.com`     | `admin123`   | Full access to all marketing & finance data |
| **Marketing** | `marketing@company.com` | `marketing123` | Access to engagement and performance metrics  |
| **Finance** | `finance@company.com`   | `finance123` | Access to cost, revenue, and ROAS metrics   |

-----

## 🔧 API Endpoints

The backend provides a RESTful API for all frontend operations.

| Method | Endpoint              | Description                                        | Access       |
| :----- | :-------------------- | :------------------------------------------------- | :----------- |
| `POST` | `/api/login`          | Authenticates a user and returns a JWT.            | Public       |
| `GET`  | `/api/user/profile`   | Retrieves the profile of the logged-in user.       | Authenticated |
| `GET`  | `/api/kpi-data`       | Fetches KPI data based on the user's role.         | Authenticated |
| `POST` | `/api/cache/clear`    | Clears the in-memory data cache.                   | Admin only   |
| `GET`  | `/api/cache/stats`    | Returns statistics about the cache.                | Admin only   |
| `GET`  | `/api/health`         | Checks the health status of the API.               | Public       |

#### Example: `POST /api/login`

**Request Body:**

```json
{
  "email": "admin@company.com",
  "password": "admin123"
}
```

**Response Body:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

-----

## 🚀 Production Deployment

To deploy this application to a production environment, you should:

1.  **Database:** Switch from SQLite to a robust database like MySQL or PostgreSQL and update the `DATABASE_URI` in your `.env` file.
2.  **Environment Variables:** Set a strong `JWT_SECRET_KEY` and other production-level configurations. Never use development defaults.
3.  **API Keys:** Replace the mock data services with real API clients for Google Ads and Analytics.
4.  **Frontend Build:** Run `npm run build` in the `frontend` directory to create an optimized, static build.
5.  **Web Server:** Use a production-grade web server like Gunicorn or uWSGI for the Flask app and serve the frontend build through a web server like Nginx.
6.  **Security:** Ensure HTTPS is enabled, CORS origins are restricted to your frontend domain, and consider adding rate limiting.

-----

## 🤝 Contributing

Contributions are welcome\! Please feel free to fork the repository, create a feature branch, and open a pull request.

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

-----

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

-----

**Built with ❤️ using React and Flask**