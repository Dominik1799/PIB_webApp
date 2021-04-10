from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField
from wtforms.validators import InputRequired
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secKey'
Bootstrap(app)


class SearchForm(FlaskForm):
    search = StringField('Search for', [InputRequired()])


@app.route("/search/<query>")
def unsafe_query(query):
    conn = psycopg2.connect(database="postgres", user="postgres",
                           password="postgres", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT * FROM test")
    print(cur.fetchall())

    return render_template("search.html")


@app.route('/', methods=["GET", "POST"])
def hello_world():
    form = SearchForm()
    if form.is_submitted():
        func = "unsafe_query"
        return redirect(url_for(func, query=request.form["search"]))
    return render_template("index.html", form=form)


if __name__ == '__main__':
    app.run()
