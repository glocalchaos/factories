from flask import request, g
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from flask_caching import Cache
from .config import Config
import os



# Path to the client cache directory used by Apache
CREDENTIAL_CACHE_PATH = "/krb_clients_cache"  # Matches your Apache config: GssapiDelegCcacheDir

# Dictionary to hold the database sessions for each user
user_sessions = {}

def get_user_krb5_cache():
    """
    Retrieves the Kerberos credential cache for the authenticated user.
    """
    user_session_id = request.headers.get('Remote-User') or request.headers.get('X-Custom-User')
    print(user_session_id)
    if not user_session_id:
        raise Exception("User's Kerberos principal is not available in REMOTE_USER.")

    user_cache_file = os.path.join(CREDENTIAL_CACHE_PATH, f"{user_session_id}")

    if not os.path.exists(user_cache_file):
        raise Exception(f"Kerberos cache file not found for user {user_session_id} at {user_cache_file}")

    return f"FILE:{user_cache_file}"


def create_db_session(user_session_id):
    """
    Create a new database session for the given user.
    """
    krb5_cache_path = get_user_krb5_cache()
    os.environ['KRB5CCNAME'] = krb5_cache_path

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{Config.DATABASE}:{Config.PORT}/ISKAO_DATA'

    # Create the SQLAlchemy engine using GSSAPI with the correct user context
    engine = create_engine(
        SQLALCHEMY_DATABASE_URI + "?gssencmode=require",
        connect_args={
            "krbsrvname": "postgres",
            "user": user_session_id.split("@")[0].upper(),
        },
        pool_size=10
    )

    # Create a scoped session for this user
    return scoped_session(sessionmaker(bind=engine))


if Config.DATABASE_MODE == 'DIRECT':
    # Создание движка SQLAlchemy
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_size=10)
    db = scoped_session(sessionmaker(bind=engine))
cache = Cache()



def set_db_connection():
    if Config.DATABASE_MODE == 'DIRECT':
        from cabinet_back.database import db
        return db
    elif Config.DATABASE_MODE == 'DOMAIN':
        db = g.db
        return db