from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
 
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Mysql!123@127.0.0.1:3306/MyDB_one'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
 
 
class Phone(db.Model):
    __tablename__ = 'Phone_tb'
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    person_id = db.Column(db.Integer, db.ForeignKey('Person_tb.mid'))
 
    def __repr__(self):
        return 'Phone_name: {}'.format(self.name)
 
 
class Person(db.Model):
    __tablename__ = 'Person_tb'
    mid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    age = db.Column(db.Integer)
    phones = db.relationship('Phone', backref='person', lazy='dynamic')
 
    def __repr__(self):
        return 'Person_name: {}'.format(self.name)
 
 
db.drop_all()
db.create_all()
 
 
if __name__ == '__main__':
 
    per_one = Person(name='You', age=18)
    per_two = Person(name='Me', age=81)
    per_three = Person(name='JackMa', age=60)
    per_four = Person(name='Panshiyi', age=50)
    per_five = Person(name='DingLei', age=40)
    db.session.add_all([per_one, per_two, per_three, per_four, per_five])
 
    phone_one = Phone(name='IPhone', person_id=1)
    phone_two = Phone(name='Mi', person_id=3)
    phone_three = Phone(name='NOKIA', person_id=2)
    phone_four = Phone(name='HUAWEI', person_id=4)
    phone_five = Phone(name='OPPO', person_id=5)
    phone_six = Phone(name='VIVO', person_id=1)
    db.session.add_all([phone_one, phone_two, phone_three, phone_four, phone_five, phone_six])
    db.session.commit()
 
    app.run(debug=True)
