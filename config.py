
class Config(object):
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'test'
    USERNAME = 'root'
    PASSWORD = 'Lili0517'
    DB_URI = 'mysql+pymysql://{username}:{password}@{host}:{port}/{db}'.format(username=USERNAME, password=PASSWORD,
                                                                               host=HOSTNAME, port=PORT, db=DATABASE)

    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False