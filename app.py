from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)

params = {
    'database': 'HW3',
    'user': 'raywu1990',
    'password': 'test',
    'host': 'localhost',
    'port': '5432'
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://raywu1990:test@localhost:5432/HW3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class BasketA(db.Model):
    a = db.Column(db.Integer, primary_key=True)
    fruit_a = db.Column(db.String(100), nullable=False)

class BasketB(db.Model):
    b = db.Column(db.Integer, primary_key=True)
    fruit_b = db.Column(db.String(100), nullable=False)

@app.route('/api/update_basket_a', methods=['GET'])
def update_basket_a():
    try:
        max_id = db.session.query(db.func.max(BasketA.a)).scalar() or 0
        new_id = max_id + 1
        new_entry = BasketA(a=new_id, fruit_a='Cherry')
        db.session.add(new_entry)
        db.session.commit()
        return 'Success!'
    except Exception as e:
        db.session.rollback()
        return str(e)

@app.route('/api/unique')
def get_unique_fruits():
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        cur.execute("SELECT DISTINCT fruit_a FROM basket_a;")
        unique_fruits_a = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT DISTINCT fruit_b FROM basket_b;")
        unique_fruits_b = [row[0] for row in cur.fetchall()]

        max_length = max(len(unique_fruits_a), len(unique_fruits_b))
        
        while len(unique_fruits_a) < max_length:
            unique_fruits_a.append('')
        while len(unique_fruits_b) < max_length:
            unique_fruits_b.append('')

        zipped_fruits = list(zip(unique_fruits_a, unique_fruits_b))
        cur.close()
        conn.close()
        return render_template('fruits.html', zipped_fruits=zipped_fruits)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
