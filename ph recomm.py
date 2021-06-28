from flask import Flask, request, render_template
import os

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=TEMPLATE_DIR)

import pickle
import pandas as pd


import warnings
warnings.filterwarnings("ignore")

from IPython.core.display import display, HTML
display(HTML("<style>.container { width:90% !important; }</style>"))


@app.route("/")
def hello():
    return TEMPLATE_DIR


print("building recommendation engine")
print("reading data")
with open('rec_list.pkl','rb') as file:
    reco = pickle.load(file)


@app.route("/rec", methods=['GET', 'POST'])
def rec():
    query = ''
    if (request.method == "POST"):
        print("inside post")
        print(str(request.form.get('query')))
        query = request.form.get('query')
        recommendations = reco[query]
        recommendations = pd.DataFrame(recommendations).set_index(0)
        return render_template('rec.html', query=query, recommendations=recommendations)
    else:
        return render_template('rec.html', query="", recommendations="<<unknown>>")


if __name__ == "__main__":
    app.run(debug=True)


