Here’s a consolidated and well-formatted version of your `.md` file for the **Casting Agency** project:

---

# 🎬 Casting Agency

The **Casting Agency** models a company responsible for creating movies and managing/assigning actors to those movies. You are an **Executive Producer** working to streamline this process via a web-based system.

---

## 🧩 Models

### Movies
- `title`: *string*
- `release_date`: *date*

### Actors
- `name`: *string*
- `age`: *integer*
- `gender`: *string*

---

## 🌐 Endpoints

| Method | Endpoint         | Description                  |
|--------|------------------|------------------------------|
| GET    | `/actors`        | Retrieve all actors          |
| GET    | `/movies`        | Retrieve all movies          |
| POST   | `/actors`        | Add a new actor              |
| POST   | `/movies`        | Add a new movie              |
| DELETE | `/actors/<id>`   | Delete an actor by ID        |
| DELETE | `/movies/<id>`   | Delete a movie by ID         |
| PATCH  | `/actors/<id>`   | Update partial actor details |
| PATCH  | `/movies/<id>`   | Update partial movie details |
| PUT    | `/actors/<id>`   | Replace actor details        |
| PUT    | `/movies/<id>`   | Replace movie details        |

---

## 🔐 Roles and Permissions

### 1. Casting Assistant
- ✅ View actors
- ✅ View movies

### 2. Casting Director
- ✅ All Casting Assistant permissions
- ➕ Add/Delete actors
- ✏️ Modify actors or movies

### 3. Executive Producer
- ✅ All Casting Director permissions
- ➕ Add/Delete movies

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7+
- `pip` package manager
- Virtual environment tool (recommended)

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
   - Create a `.env` file in the root directory.
   - Add necessary variables like:
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
   - Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧪 Testing

### Running Tests

1. **Activate Virtual Environment**
   ```bash
   source .venv/bin/activate
   ```

2. **Run Tests**
   ```bash
   python -m unittest discover
   ```

### Test Coverage

#### 🎞 Movies
- `GET /movies` (success/failure)
- `GET /movies/<id>`
- `POST /movies` (valid/invalid)
- `PUT /movies/<id>`
- `DELETE /movies/<id>`

#### 👨‍🎤 Actors
- `GET /actors` (success/failure)
- `GET /actors/<id>`
- `POST /actors` (valid/invalid)
- `PUT /actors/<id>`
- `DELETE /actors/<id>`

---
