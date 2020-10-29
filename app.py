from flask import Flask, render_template, url_for
import pandas as pd 
app = Flask(__name__)

def generate_fake_news():
    df = pd.read_excel('master.xlsx')
    return(df.loc[1, "full_text"])

@app.route("/")
def index():
    newz = generate_fake_news()
    return render_template("index.html", newz=newz)


if __name__ == "__main__":
    app.run(debug=True)