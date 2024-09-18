# Project Setup Instructions

Follow these steps to set up the project environment and run the application:

1. **Create a Python 3.12.4 Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install Requirements**
   ```sh
   pip install -r requirements.txt
   ```

3. **Launch Docker Compose**
   ```sh
   cd local-env
   docker-compose up -d
   cd ..
   ```

4. **Run Database Migrations**
   ```sh
   alembic upgrade head
   ```

5. **Set PYTHONPATH**
   ```sh
   export PYTHONPATH=$PWD
   ```

6. **Create Admin User**
   ```sh
   python create_admin_user.py
   ```

7. **Run FastAPI Development Server**
   ```sh
   uvicorn app.main:app --reload
   ```

8. **Check Endpoints**
   Open your browser and go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to see all the available endpoints.
