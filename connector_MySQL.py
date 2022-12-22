import pymysql


class Database:
    def __init__(self):
        self.coon = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='Lili0517',
            db='test',
            charset='utf8'
        )
        self.myCursor = self.coon.cursor()

    def print(self):
        self.myCursor.execute("SELECT name FROM Customer;")
        self.coon.commit()
        result = self.myCursor.fetchone()
        # result = self.myCursor.fetchall()
        print(result[0])