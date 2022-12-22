import joblib
import numpy as np
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

import connector_MySQL

connect = connector_MySQL.Database()
app = Flask(__name__)


user = 'root'
password = 'Lili0517'
database = 'final_project'
uri = 'mysql+pymysql://%s:%s@localhost:3306/%s' % (user, password, database)
app.config['SQLALCHEMY_DATABASE_URI'] = uri

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Lili0517@localhost'


class Manager(db.Model):
    __tablename__ = 'manager'
    # manager_id = Column(Integer, primary_key=True)
    manager_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def dump(self):
        # print(self.manager_id, self.name, self.password, self.email)
        # print(self.password)
        return self.password

    def acquire(self):
        return self.password

class Service(db.Model):
    __tablename__ = 'service'
    service_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    name = db.Column(db.String(50))
    call_time = db.Column(db.Integer)
    price_per_month = db.Column(db.Integer)
    price_per_year = db.Column(db.Integer)

class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(100))
    college = db.Column(db.Integer)
    handset = db.Column(db.String(20))
    income = db.Column(db.Integer)

    def check(self):
        return self.password

class Contract(db.Model):
    __tablename__ = 'contract'
    contract_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, ForeignKey(Customer.customer_id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    service_id = db.Column(db.Integer, ForeignKey(Service.service_id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    leftover = db.Column(db.Integer)
    average_of_duration = db.Column(db.Integer)
    over_15_mins_calls_per_month = db.Column(db.Integer)
    satisfaction = db.Column(db.Integer)
    usage_level = db.Column(db.Integer)
    considering_change_of_plan = db.Column(db.Integer)

# def query_students():
#     # managers = Manager.query.all()
#     # for manager in managers:
#     #     manager.dump()
#     managers = Manager.query.filter_by(name = 'Jony')
#     print(managers)
#     res = managers.first()
#     pwd = res.dump()
#     # for manager in managers:
#     #     manager.dump()
#     print(pwd)
#     print("-----------")
#     return pwd


def check_manager(username):
    managers = Manager.query.filter_by(name = username)
    manager = managers.first()
    pwd = manager.acquire()
    return pwd


def check_customer(username):
    customers = Customer.query.filter_by(username = username)
    customer = customers.first()
    pwd = customer.check()
    return pwd


def customer_exists(username):
    customers = Customer.query.filter_by(username = username)
    customer = customers.first()
    if customer == None:
        return False
    return True


def manager_exists(username):
    managers = Manager.query.filter_by(name = username)
    manager = managers.first()
    if manager == None:
        return False
    return True


@app.route('/')
def hello_world():  # put application's code here
    # test = connect.print()
    # if type(test) == "Jony":
    #     print(1)
    # pwd = query_students()
    # print(pwd)
    # return 'Hello World!'
    return render_template('base.html')


@app.route('/customerLogin', methods=['GET', 'POST'])
def cLogin():
    if request.method == 'GET':
        return render_template('customerLogin.html')

    username = request.form.get('username')
    pwd = request.form.get('pwd')

    whether_exists = customer_exists(username)
    if not whether_exists:
        password = None
        print(password)
    else:
        password = check_customer(username)

    error = 'Invalid username or password, please try again!'

    if whether_exists and pwd == password:
        return redirect('/customerFrame')
    elif pwd != password or password == None:
        return render_template('customerLogin.html', error=error)


@app.route('/managerLogin', methods=['GET', 'POST'])
def mLogin():

    if request.method == 'GET':
        return render_template('managerLogin.html')

    username = request.form.get('username')
    pwd = request.form.get('pwd')
    # print(username)
    # print(pwd)
    # print("---------")

    whether_exists = manager_exists(username)
    if not whether_exists:
        password = None
        print(password)
    else:
        password = check_manager(username)

    error = 'Invalid username or password, please try again!'

    if whether_exists and pwd == password:
        return redirect('/managerFrame')
    elif pwd != password or password == None:
        return render_template('managerLogin.html', error=error)


@app.route('/customerFrame')
def indexCustomer():
    page = request.args.get('page', 1, type=int)
    pagination = Service.query.order_by(Service.service_id).paginate(
        page=page, per_page=2)
    return render_template('customerFrame.html', pagination=pagination)


@app.route('/managerFrame')
def indexManager():
    # services = Service.query.all()
    page = request.args.get('page', 1, type=int)
    pagination = Contract.query.order_by(Contract.contract_id).paginate(
        page=page, per_page=2)
    return render_template('managerFrame.html', pagination=pagination)


@app.route('/predict')
def predict():
    if request.method == 'GET':
        return render_template('predict.html')


def prediction_model(to_predict_list):
    model = joblib.load('churn_predict_model.pkl')
    to_predict = np.array(to_predict_list).reshape(1, 12)
    result = model.predict(to_predict)
    return result[0]

# def prediction_model():
#     model = joblib.load('churn_predict_model.pkl')
#     to_predict = np.array([60533,0,73,157565,297,19,2,2,2,4,6.46,0]).reshape(1,12)
#     # result = model.predict([[60533,0,73,157565,297,19,2,2,2,4,6.46,0]])
#     result = model.predict(to_predict)
#     print(result[0])
#     # return result[0]
# prediction_model()


@app.route('/result', methods=['POST'])
def result():
    to_predict_list = request.form.to_dict()
    to_predict_list = list(to_predict_list.values())
    # to_predict_list = list(map(int, to_predict_list))
    result = prediction_model(to_predict_list)
    if result > 0.5:
        prediction = 'This customer is going to leave'
    else:
        prediction = 'This customer is going to stay'
    return render_template("result.html", prediction=prediction)


if __name__ == '__main__':
    app.run()

