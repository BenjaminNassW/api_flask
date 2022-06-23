"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Fav_people, Fav_planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def getUser():
    all_user = User.query.all()
    arreglo_user = list(map(lambda x: x.serialize(), all_user))
    return jsonify({"Resultado": arreglo_user})


@app.route('/people', methods=['GET'])
def getPeople():
    all_people = People.query.all()
    arreglo_people = list(map(lambda x: x.serialize(), all_people))
    return jsonify({"Resultado": arreglo_people})


@app.route('/people/<int:people_id>', methods=['GET'])
def getPeopleID(people_id):
    one_people = People.query.get(people_id)
    return jsonify({"personaje": one_people.serialize()})


@app.route('/planet', methods=['GET'])
def getPlanet():
    all_planet = Planet.query.all()
    arreglo_planet = list(map(lambda x: x.serialize(), all_planet))
    return jsonify({"Resultado": arreglo_planet})


@app.route('/planet/<int:planet_id>', methods=['GET'])
def getPlanetID(planet_id):
    one_planet = Planet.query.get(planet_id)
    return jsonify({"planeta": one_planet.serialize()})


@app.route('/favPeople', methods=['GET'])
def getFavPoeple():
    all_favPeople = Fav_people.query.all()
    arreglo_favPeople = list(map(lambda x: x.serialize(), all_favPeople))
    return jsonify({"Resultado": arreglo_favPeople})

@app.route('/favPlanet', methods=['GET'])
def getFavPlanet():
    all_favPlanet = Fav_planet.query.all()
    arreglo_favPlanet = list(map(lambda x: x.serialize(), all_favPlanet))
    return jsonify({"Resultado": arreglo_favPlanet})

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def addFavPeople(people_id):
    user = request.get_json()
    newFav = Fav_people()
    newFav.id_user = user['id']
    newFav.uid_people = people_id

    db.session.add(newFav)
    db.session.commit()
    return("todo salio bien :D")


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def deleteFavPeople(people_id):
    user = request.get_json()
    allFavs = Fav_people.query.filter_by(
        id_user=user['id'], uid_people=people_id).all()
    for i in allFavs:
        db.session.delete(i)
    db.session.commit()
    return("se elimino todo")

@app.route('/favorite/planet/<int:planet_uid>', methods=['POST'])
def addFavPlanet(planet_uid):
    user = request.get_json()
    newFav = Fav_planet()
    newFav.id_user = user['id']
    newFav.uid_planet = planet_uid

    db.session.add(newFav)
    db.session.commit()
    return("todo salio bien :D")


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def deleteFavPlanet(planet_id):
    user = request.get_json()
    allFavs = Fav_planet.query.filter_by(
        id_user=user['id'], uid_planet=planet_id).all()
    for i in allFavs:
        db.session.delete(i)
    db.session.commit()
    return("se elimino todo")

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
