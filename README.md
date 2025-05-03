# 🎬 Casting Agency

The **Casting Agency** models a company responsible for creating movies and managing/assigning actors to those movies. You are an **Executive Producer** working to streamline this process via a web-based system.

---

## 💡 Motivation for the Project

The **Casting Agency** project was developed to demonstrate the implementation of a role-based access control system in a real-world scenario. It showcases how to securely manage resources (movies and actors) while ensuring that users with different roles (e.g., Casting Assistant, Casting Director, Executive Producer) have appropriate permissions. This project also highlights the integration of modern authentication and authorization techniques using Auth0, along with best practices for building scalable and secure APIs.

---

## 🧩 Models

### Movies

* `title`: *string*
* `release_date`: *date*

### Actors

* `name`: *string*
* `age`: *integer*
* `gender`: *string*

---

## 🌐 Endpoints

| Method | Endpoint       | Description                  |
| ------ | -------------- | ---------------------------- |
| GET    | `/actors`      | Retrieve all actors          |
| GET    | `/movies`      | Retrieve all movies          |
| POST   | `/actors`      | Add a new actor              |
| POST   | `/movies`      | Add a new movie              |
| DELETE | `/actors/<id>` | Delete an actor by ID        |
| DELETE | `/movies/<id>` | Delete a movie by ID         |
| PATCH  | `/actors/<id>` | Update partial actor details |
| PATCH  | `/movies/<id>` | Update partial movie details |
| PUT    | `/actors/<id>` | Replace actor details        |
| PUT    | `/movies/<id>` | Replace movie details        |

---

## 🔐 Roles and Permissions

### 1. Casting Assistant

* ✅ View actors
* ✅ View movies

### 2. Casting Director

* ✅ All Casting Assistant permissions
* ➕ Add/Delete actors
* ✏️ Modify actors or movies

### 3. Executive Producer

* ✅ All Casting Director permissions
* ➕ Add/Delete movies

---

## 🛠️ Installation & Setup

### Prerequisites

* Python 3.7+
* `pip` package manager
* Virtual environment tool (recommended)

### 📦 Project Dependencies

The following dependencies are required for the project:

```
alembic==1.10.4  
blinker==1.6.2  
click==8.1.3  
dotenv==0.9.9  
ecdsa==0.19.1  
exceptiongroup==1.2.2  
Flask==2.2.5  
Flask-Migrate==3.1.0  
Flask-SQLAlchemy==2.5.1  
importlib-metadata==6.7.0  
importlib-resources==5.12.0  
iniconfig==2.0.0  
itsdangerous==2.1.2  
Jinja2==3.1.2  
jose==1.0.0  
Mako==1.2.4  
MarkupSafe==2.1.3  
packaging==24.0  
pluggy==1.2.0  
psycopg2==2.9.9  
pyasn1==0.5.1  
pytest==7.4.2  
python-dotenv==0.21.0  
python-jose==3.3.0  
rsa==4.9.1  
six==1.17.0  
SQLAlchemy==1.4.49  
tomli==2.0.1  
typing_extensions==4.5.0  
Werkzeug==2.2.3  
zipp==3.15.0  
```

### Steps

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python3.7 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**

   * Create a `.env` file in the root directory.
   * Add necessary variables like:

     ```
     FLASK_APP=app.py
     FLASK_ENV=development
     DATABASE_URL=<your_database_url>
     ```

5. **Run Database Migrations**

   ```bash
   flask db upgrade
   ```

6. **Start the Application**

   ```bash
   flask run
   ```

7. **Access the App**

   * Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)
   * Visit [https://fswd-capstone.onrender.com](https://fswd-capstone.onrender.com) where the app is deployed.

---

## 🧪 Testing

### Running Tests

1. **Activate Virtual Environment**

   ```bash
   source .venv/bin/activate
   ```

2. **Run Tests**

   ```bash
   python -m unittest tests/test_app.py
   python -m unittest tests/role_based_test.py
   ```

### Test Coverage

#### 🎞 Movies

* `GET /movies` (success/failure)
* `GET /movies/<id>`
* `POST /movies` (valid/invalid)
* `PUT /movies/<id>`
* `DELETE /movies/<id>`

#### 👨‍🎤 Actors

* `GET /actors` (success/failure)
* `GET /actors/<id>`
* `POST /actors` (valid/invalid)
* `PUT /actors/<id>`
* `DELETE /actors/<id>`

---
