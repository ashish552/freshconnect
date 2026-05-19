class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/freshconnect_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'freshconnectsecret'