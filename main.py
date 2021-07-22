from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy

# -------------------- App and Database -------------------- #

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)

db = SQLAlchemy(app)


# -------------------- Cafe Table Configuration -------------------- #

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


# -------------------- Cafe Form Configuration -------------------- #

class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    img_url = StringField('Cafe Image (URL)', validators=[DataRequired(), URL()])
    loc = StringField('Cafe Location', validators=[DataRequired()])
    sockets = SelectField('Has Power Sockets', choices=["Yes", "No"], validators=[DataRequired()])
    toilet = SelectField('Has Toilets', choices=["Yes", "No"], validators=[DataRequired()])
    wifi = SelectField('Has WiFi', choices=["Yes", "No"], validators=[DataRequired()])
    calls = SelectField('Can Take Calls', choices=["Yes", "No"], validators=[DataRequired()])
    seats = SelectField('How Many Seats', choices=["0-10", "10-20", "20-30", "30-40", "40-50", "50+"],
                        validators=[DataRequired()])
    coffee_price = StringField('Coffe Price eg. £2.50', validators=[DataRequired()])
    submit = SubmitField('Submit')


# -------------------- Flask Routes -------------------- #

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('get_cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def get_cafes():
    cafes = Cafe.query.all()
    return render_template("cafes.html", all_cafes=cafes)


@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('get_cafes'))


if __name__ == '__main__':
    app.run(debug=True)
