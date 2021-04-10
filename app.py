from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secKey'
Bootstrap(app)


class SearchForm(FlaskForm):
    search = StringField('Search for', [InputRequired()])


@app.route("/search/<query>")
def unsafe_query(query):
    print(query)
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
