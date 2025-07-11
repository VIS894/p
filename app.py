from flask import Flask, render_template, request, url_for
import joblib
import pickle
import pandas as pd
import sqlite3

# Load the model
model = pickle.load(open('model.pkl', 'rb'))

app = Flask(__name__)

# Database connection
def get_db_connection():
    try:
        conn = sqlite3.connect('bike_db.db')
        conn.row_factory = sqlite3.Row  # Dict-like row access
        return conn
    except sqlite3.error as e:
        print(e)
        return None

# Create table if not exists
def create_table():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bike_prediction (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand_name TEXT,
                owner INTEGER,
                age INTEGER,
                power INTEGER,
                kms_driven INTEGER,
                predicted_price INTEGER
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

# Initialize the database
create_table()


@app.route('/history', methods=['GET', 'POST'])
def history():
    brand_name_filter = request.form.get('brand_name_filter', None)
    conn = get_db_connection()
    historical_data = []
    if conn:
        try:
            cursor = conn.cursor()
            if brand_name_filter:
                cursor.execute("SELECT * FROM bike_prediction WHERE brand_name=?", (brand_name_filter,))
            else:
                cursor.execute("SELECT * FROM bike_prediction")
            historical_data = [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    return render_template('history.html', historical_data=historical_data)




@app.route("/")
def home():
    return render_template("home.html")



@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/project')
def project():
    return render_template('project.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        brand_name = request.form['brand_name']
        owner_name = int(request.form['owner'])
        age_bike = int(request.form['age'])
        power_bike = int(request.form['power'])
        kms_driven_bike = int(request.form['kms_driven'])

        bike_numbers = {
            'TVS': 0, 'Royal Enfield': 1, 'Triumph': 2, 'Yamaha': 3,
            'Honda': 4, 'Hero': 5, 'Bajaj': 6, 'Suzuki': 7, 'Benelli': 8,
            'KTM': 9, 'Mahindra': 10, 'Kawasaki': 11, 'Ducati': 12,
            'Hyosung': 13, 'Harley-Davidson': 14, 'Jawa': 15, 'BMW': 16,
            'Indian': 17, 'Rajdoot': 18, 'LML': 19, 'Yezdi': 20,
            'MV': 21, 'Ideal': 22
        }

        brand_name_encoded = bike_numbers.get(brand_name, -1)
        if brand_name_encoded == -1:
            return 'Invalid brand name.'

        input_data = [[owner_name, brand_name_encoded, kms_driven_bike, age_bike, power_bike]]
        prediction = round(model.predict(input_data)[0], 2)

        # Insert prediction into database
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bike_prediction 
                (brand_name, owner, age, power, kms_driven, predicted_price)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (brand_name, owner_name, age_bike, power_bike, kms_driven_bike, prediction))
            conn.commit()
            cursor.close()
            conn.close()

        return render_template('project.html', prediction=prediction)

    except Exception as e:
        print("Error during prediction:", e)
        return 'Something went wrong.'


if _name__ == '__main__':
    app.run(debug=True)


