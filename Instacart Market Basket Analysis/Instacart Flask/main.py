import pickle
from flask import Flask, request, render_template
from predict_reorder import predict_reorder
app = Flask(__name__)

#from sklearn.externals import joblib
#predict_function = joblib.load('Predict_funtion.p')


@app.route('/')
def entry_page():
    return render_template('index.html')

@app.route('/predict_reorder/', methods=['GET', 'POST'])
def render_message():
    user_id = request.form['user_id']
    try:
        user_id_int = int(user_id)
    except:
        message = "Please enter a number for the user_id"
        return render_template('index.html',
                               message=message)

    product_id = request.form['product_id']
    try:
        product_id_int = int(product_id)
    except:
        message = "Please enter a number for the product_id"
        return render_template('index.html',
                               message=message)

    message = predict_reorder(user_id, product_id)

    return render_template('index.html',
                           message=message)


if __name__ == '__main__':
    app.run(debug=True)
