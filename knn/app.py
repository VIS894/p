from flask import Flask, render_template, request,url_for,jsonify
import joblib
scaler = joblib.load('scaler.lb')
kmeans = joblib.load('kmeans_model.pkl')
df = joblib.load('crop_reco_df.lb')

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        n = int(request.form['nitrogen'])
        p = int(request.form['phosphorus']) 
        k = int(request.form['potassium'])
        t = float(request.form['temperature'])
        h = float(request.form['humidity'])
        ph = float(request.form['ph'])
        r = float(request.form['rainfall'])
        user_data = [[n, p, k, t, h, ph, r]]
        trans_data = scaler.transform(user_data)
        prediction = kmeans.predict(trans_data)[0]
        print(prediction)
        dt = dict(df[df['cluster_8'] == prediction]["label"].value_counts())
        return render_template('index.html',dt = dt)
    
    
                     

if __name__ == '__main__':
    app.run(debug=True)
