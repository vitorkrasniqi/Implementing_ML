from flask import Flask, render_template, request

@app.route('/')
def index_view():
    return render_template('index.html')


@app.route('/predict/',methods=['GET','POST'])
def predict():
	response = "For ML Prediction"
return response	

if __name__ == '__main__':
    app.run(debug=True, port=8000)

    