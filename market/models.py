from market import db
from market import bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(length=30),nullable=False,unique=True)
    email = db.Column(db.String(length=50),nullable=False,unique=True)
    password = db.Column(db.String(length=60),nullable=False)
    budget = db.Column(db.Integer(),nullable=False,default=100)
    items = db.relationship('Item',backref = 'owned_user',lazy=True)

    @property
    def prety_budget(self):
        if len(str(self.budget))>=4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"

    @property
    def password1(self):
        return self.password1

    @password1.setter
    def password1(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)


class Item(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    name = db.Column(db.String(length=30),nullable =False,unique=True)
    barcode = db.Column(db.String(length=12), nullable=False,unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1024),nullable=False)
    owner = db.Column(db.Integer(),db.ForeignKey('user.id'))


    def __repr__(self):

        return f'Item {self.name}'