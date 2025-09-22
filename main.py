from http.client import responses
from locale import currency

import json

import flask
from flask import Flask
from flask import url_for, redirect
from flask import render_template, request
# import requests
# import json
from sqlalchemy import Table, Column ,create_engine , String, ForeignKey
# from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase , sessionmaker, Mapped, mapped_column, relationship

app = Flask(__name__)

engine = create_engine("sqlite:///films.db",echo=True)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    def create_db(self):
        Base.metadata.create_all(engine)
    def drop_db(self):
        Base.metadata.drop_all(engine)

class Films(Base):
    __tablename__ = "reviews"
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(50))
    director: Mapped[str] = mapped_column(String(50))
    year : Mapped[int] = mapped_column()
    url : Mapped[str] = mapped_column(String(100))

# base = Base()
# base.create_db()


@app.route('/searched_film', methods=['POST'])
def search():
    if request.method == "POST":
        name = request.form['s_name']
        return redirect(url_for("searched_film", searched_name=name))
@app.route("/film", methods=["GET","POST"])
def film_site():
    if request.method == "GET":
        return render_template("get_film.html")
    else:
        name = request.form["name"]
        director = request.form["director"]
        year = int(request.form["year"])
        url = request.form["url"]

        with Session() as sess:
            new_film = Films(name=name,director=director,year=year,url=url)
            sess.add(new_film)
            sess.commit()

        return redirect(url_for("all_films"))

@app.route("/all_films")
def all_films():
    with Session() as sess:
        data = sess.query(Films).all()
        return render_template('film_list.html', data=data)

@app.route('/searched_film')
def searched_film():
    name = request.args.get("searched_name")
    with Session() as sess:
        s_name = sess.query(Films).filter_by(name=name).all()
        return render_template('film_list.html', data=s_name)





if __name__ == '__main__':
    app.run(debug=True, port = 8000)

