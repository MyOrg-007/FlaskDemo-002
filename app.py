# Another example chaining Bokeh's to Flask.

from bokeh.embed import components
from flask import Flask, render_template
import bokeh
import pandas as pd
from util import make_plot
from waitress import serve

df = pd.read_csv(
    "https://data.boston.gov/dataset/c8b8ef8c-dd31-4e4e-bf19-af7e4e0d7f36/resource/29e74884-a777-4242-9fcc-c30aaaf3fb10/download/economic-indicators.csv",
    parse_dates=[["Year", "Month"]],
)
length = len(df)
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html.j2")

@app.route("/test")
def test():
    return render_template("testbill.html.j2")

@app.route("/bokehplot")
def bokehplot():
    figure = make_plot()
    fig_script, fig_div = components(figure)
    return render_template(
        "bokeh.html.j2",
        fig_script=fig_script,
        fig_div=fig_div,
        bkversion=bokeh.__version__,
    )


@app.route("/df")
def dataframe():
    return render_template("df.html.j2", length=length, dataframe=df.to_html())


@app.route("/dfcustom")
def dfcustom():
    data = df.to_dict(orient="records")
    headers = df.columns
    print(headers)
    return render_template("dfcustom.html.j2", data=data, headers=headers)


if __name__ == "__main__":
    app.run(debug=False, port=5000)
    serve(app, host='0.0.0.0', port=5000)
    #serve(app, host='0.0.0.0', port=8080, url_scheme='https')

  
