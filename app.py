"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)

@app.route("/api/cupcakes")
def list_cupcakes():
    """get data about all cupcakes"""
    cupcakes = [cupcake.serialize_cupcake() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    data = request.json

    cupcake = Cupcake(flavor=data['flavor'], 
                      rating=data['rating'], 
                      size=data["size"], 
                      image=data["image"])
    
    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize_cupcake()), 201)


@app.route("/api/cupcakes/<int:id>")
def show_cupcake_info(id):
    """get data about a specific cupcake"""
    cupcake = Cupcake.query.get_or_404(id)

    return jsonify(cupcake=cupcake.serlialize_cupcake())

