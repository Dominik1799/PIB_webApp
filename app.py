from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField
from wtforms.validators import InputRequired
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secKey'
Bootstrap(app)


class SearchForm(FlaskForm):
    search = StringField('Search for', [InputRequired()])


@app.route("/unsafe_search/<query>")
def unsafe_query(query):
    conn = psycopg2.connect(database="postgres", user="postgres",
                            password="postgres", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT name, description, price FROM products WHERE name LIKE '%" + query + "%'")
    items = cur.fetchall()
    return render_template("search.html", items=items)


@app.route("/safe_search/<query>")
def safe_query(query):
    conn = psycopg2.connect(database="postgres", user="postgres",
                            password="postgres", host="127.0.0.1", port="5432")
    q = sql.SQL("SELECT name, description, price FROM products WHERE name LIKE %s")
    cur = conn.cursor()
    cur.execute(q, ("%" + query + "%",))
    items = cur.fetchall()
    return render_template("search.html", items=items)


@app.route('/', methods=["GET", "POST"])
def hello_world():
    unsafe_form = SearchForm()
    safe_form = SearchForm()
    conn = psycopg2.connect(database="postgres", user="postgres",
                            password="postgres", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    if "unsafe" in request.form and unsafe_form.is_submitted():
        return redirect(url_for("unsafe_query", query=request.form["search"]))
    if "safe" in request.form and safe_form.is_submitted():
        return redirect(url_for("safe_query", query=request.form["search"]))
    return render_template("index.html", unsafeForm=unsafe_form, safeForm=safe_form)


if __name__ == '__main__':
    app.run()
