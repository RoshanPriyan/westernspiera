WesternSpiera Project Structure

westernspiera/
    |- backend/
        |- users/   each module
            |- models.py
            |- router.py
            |- schemas.py
            |- services/ contain each api logic like login.py, register.py
            |- utils.py
        |- custom_middleware.py
        |- database.py
        |- global_utils.py
        |- main.py
        |- readme.md
    |- frontend/