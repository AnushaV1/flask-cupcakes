"""Flask app for Cupcakes"""
from flask import Flask, request, render_template,redirect, flash, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = "Spiderman567"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
connect_db(app)

@app.route("/")
def homepage():
    """Render homepage."""

    return render_template("index.html")

@app.route('/api/cupcakes')
def list_cupcakes():
    """ Return JSON {'cupcakes': [{id, flavor, size,rating,image}, ...]} """
    cupcakes = [cupcake.serialize_cake() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes/<cupcake_id>")
def list_single_cupcake(cupcake_id):
    """Return JSON {'cupcake': {id, flavor, size,rating,image}}"""

    cake = Cupcake.query.get(cupcake_id)
    return jsonify(cupcake=cake.serialize_cake())


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcakes():
    """Create dessert from form data & return it.

    Returns JSON {'cupcake': {id, flavor, size,rating,image}}"""
    
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"] or None

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize_cake()

    # Return w/status code 201 --- return tuple (json, status)
    return ( jsonify(cupcake=serialized), 201 )


@app.route("/api/cupcakes/<cupcake_id>", methods=["PATCH"])
def update_cupcakes(cupcake_id):
    """Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request"""
    
    cake = Cupcake.query.get_or_404(cupcake_id)
    # db.session.query(Cupcake).filter_by(id= cupcake_id).update(request.json)
    cake.flavor = request.json.get('flavor',cake.flavor)
    cake.size = request.json.get('size',cake.size)
    cake.rating = request.json.get('rating', cake.rating)
    cake.image = request.json.get('image', cake.image)

    db.session.commit()
    return jsonify(cupcake=cake.serialize_cake())


@app.route("/api/cupcakes/<cupcake_id>", methods=["DELETE"])
def delete_cupake(cupcake_id):
    """ Deleted requested cupcake given id """
    cake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cake)
    db.session.commit()
    return jsonify(message = "Deleted")

