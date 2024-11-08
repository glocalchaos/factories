from app import app
from flask import session, request, g
from app.config import Config
from app.utils.db_utils import upload_regions
from flask_migrate import Migrate
from app.database import user_sessions, create_db_session, cache
from app import routes

cache.init_app(app)
migrate = Migrate(app, db)


if Config.DATABASE_MODE == 'DIRECT':
    # Создание движка SQLAlchemy
    from app.database import db, engine
    with app.app_context():
        if Config.DATABASE_MODE == 'DIRECT':
            db.create_all()
            upload_regions(db)


if Config.SERVERBASE_MODE == 'PYTHON':
    app.run(debug=True)

elif Config.SERVERBASE_MODE == 'WSGI':
    application = app




@app.before_request
def set_user_session():
    """
    Set the database session for the user based on Flask's session management.
    Only executes if DATABASE_MODE is set to 'DOMAIN' in the configuration.
    """
    # Check if DATABASE_MODE is set to 'DOMAIN'
    if Config.DATABASE_MODE != 'DOMAIN':
        return  # Skip if not in DOMAIN mode

    user_session_id = request.headers.get('Remote-User') or request.headers.get('X-Custom-User')
    if not user_session_id:
        return

    # Store user session ID in the Flask session (persistent across requests)
    if 'user_session_id' not in session:
        session['user_session_id'] = user_session_id

    # Check if a database session already exists for this user
    if user_session_id not in user_sessions:
        # Create a new session for this user
        user_sessions[user_session_id] = create_db_session(user_session_id)

    # Attach the user session to Flask's `g` for request handling
    g.db = user_sessions[user_session_id]

