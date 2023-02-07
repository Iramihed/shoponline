from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout

api = Api(merchant_id=1396424,
          secret_key='test')
checkout = Checkout(api=api)
data = {
    "currency": "USD",
    "amount": 10000
}
url = checkout.url(data).get('checkout_url')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    number = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title

@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create', methods=['POST','GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        number = request.form['number']
        desc = request.form['desc']

        item = Item(title=title, price=price, number=number, desc=desc)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Произошла ошибка"
    else:
        return render_template('create.html')

@app.route('/receipt')
def receipt():
    return render_template('receipt.html')

@app.route('/basket')
def basket():
    return render_template('basket.html')



if __name__ == '__main__':
    app.run(debug=True)
