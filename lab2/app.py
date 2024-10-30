from flask import Flask, request, jsonify
from models import db, Car
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


# CREATE
@app.route('/cars', methods=['POST'])
def create_car():
    data = request.get_json()
    new_car = Car(
        offer_type=data.get('offer_type'),
        brand=data.get('brand'),
        model=data.get('model'),
        generation=data.get('generation'),
        registration=data.get('registration'),
        condition=data.get('condition'),
        country_origin=data.get('country_origin'),
        manufacturing_year=data.get('manufacturing_year'),
        price=data.get('price'),
        currency=data.get('currency'),
        mileage=data.get('mileage'),
        engine_capacity=data.get('engine_capacity'),
        power_hp=data.get('power_hp'),
        fuel_type=data.get('fuel_type'),
        transmission=data.get('transmission'),
        color=data.get('color')
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify({'message': 'Car created'}), 201


# READ with Pagination
@app.route('/cars', methods=['GET'])
def get_cars():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)
    offset = (page - 1) * limit

    cars = Car.query.offset(offset).limit(limit).all()
    total_cars = Car.query.count()
    total_pages = (total_cars + limit - 1) // limit

    response = {
        'cars': [car.to_dict() for car in cars],
        'page': page,
        'limit': limit,
        'total_pages': total_pages,
        'total_cars': total_cars
    }
    return jsonify(response)


# UPDATE
@app.route('/cars/<int:id>', methods=['PUT'])
def update_car(id):
    data = request.get_json()
    car = Car.query.get(id)
    if not car:
        return jsonify({'message': 'Car not found'}), 404

    car.offer_type = data.get('offer_type', car.offer_type)
    car.brand = data.get('brand', car.brand)
    car.model = data.get('model', car.model)
    car.generation = data.get('generation', car.generation)
    car.registration = data.get('registration', car.registration)
    car.condition = data.get('condition', car.condition)
    car.country_origin = data.get('country_origin', car.country_origin)
    car.manufacturing_year = data.get('manufacturing_year', car.manufacturing_year)
    car.price = data.get('price', car.price)
    car.currency = data.get('currency', car.currency)
    car.mileage = data.get('mileage', car.mileage)
    car.engine_capacity = data.get('engine_capacity', car.engine_capacity)
    car.power_hp = data.get('power_hp', car.power_hp)
    car.fuel_type = data.get('fuel_type', car.fuel_type)
    car.transmission = data.get('transmission', car.transmission)
    car.color = data.get('color', car.color)

    db.session.commit()
    return jsonify({'message': 'Car updated'})


# DELETE
@app.route('/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    car = Car.query.get(id)
    if not car:
        return jsonify({'message': 'Car not found'}), 404

    db.session.delete(car)
    db.session.commit()
    return jsonify({'message': 'Car deleted'})


# UPLOAD FILE
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        file_contents = file.read().decode('utf-8')
        try:
            data = json.loads(file_contents)
            return jsonify({'message': 'File content received', 'contents': data}), 200
        except json.JSONDecodeError:
            return jsonify({'message': 'Invalid JSON file format'}), 400


if __name__ == '__main__':
    app.run(debug=True)
