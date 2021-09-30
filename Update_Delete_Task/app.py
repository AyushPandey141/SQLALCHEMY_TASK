# TASK:To print the data before and after updation and deletion
# Program By:Ayush Pandey
# Email Id:1805290@kiit.ac.in
# DATE:24-Sept-2021
# Python Version:3.7
# CAVEATS:None
# LICENSE:None


from flask import Flask
from flask import render_template
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ayush14@localhost/GUVI'
app.config['SECRET_KEY'] = 'ayush@lucknow'

db = SQLAlchemy(app)

# create a table inside our database


class APIUserModel(db.Model):
    __tablename__ = 'guvi_data_sciences'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(20))


# insert data into mysql server


@app.route('/write', methods=['POST'])
def write():
    name = request.get_json()["name"]
    email = request.get_json()["email"]
    api_user_model = APIUserModel(name=name, email=email)
    save_to_database = db.session()
    try:
        save_to_database.add(api_user_model)
        save_to_database.commit()
    except:
        save_to_database.rollback()
        save_to_database.flush()

    return jsonify({"message": "success"})


# fetch data from server
@app.route('/', methods=['GET'])
def fetch_all():
    data = APIUserModel.query.all()
    data_all = []
    for data in data:
        data_all.append(
            {"id": data.id, "name": data.name, "email": data.email})
    return jsonify(data_all)

# fetch data based on ID


@app.route('/display/<int:id>', methods=['GET'])
def fetch_by_id(id):
    try:
        data = APIUserModel.query.filter_by(id=id).first()
        return jsonify({"id": data.id, "name": data.name, "email": data.email})
    except:
        return jsonify({"message": "error"})


# update data
@app.route('/update/<int:id>', methods=['PATCH'])
def update(id):
    # update = insert + fetch by id
    see = APIUserModel.query.filter_by(id=id).first()
    q = see.name
    w = see.email
    first = see.id

    name = request.get_json()["name"]
    email = request.get_json()["email"]
    save_to_database = db.session
    try:
        api_user_model = APIUserModel.query.filter_by(id=id).first()
        api_user_model.name = name
        api_user_model.email = email
        first = api_user_model.id
        save_to_database.commit()

    except:
        return jsonify({"message": "error in updating data"})
        save_to_database.rollback()
        save_to_database.flush()
    id = api_user_model.id
    data = APIUserModel.query.filter_by(id=id).first()
    return jsonify({"id": first, "name": q, "email": w}, {"id": data.id, "name": data.name, "email": data.email})

# delete data


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    see = APIUserModel.query.filter_by(id=id).first()
    q = see.name
    w = see.email
    first = see.id
    try:
        save_to_database = db.session
        APIUserModel.query.filter_by(id=id).delete()
        save_to_database.commit()
        return jsonify({"id": first, "name": q, "email": w})
    except:
        return jsonify({"message": "error in deleting data"})


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5000)
