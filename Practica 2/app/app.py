#./app/app.py

from pymongo import MongoClient
from flask import Flask, Response, request, jsonify, render_template
from flask_restful import Resource, Api, reqparse

from bson import ObjectId

app = Flask(__name__)

# Conectar al servicio (docker) "mongo" en su puerto estandar
client = MongoClient("mongo", 27017)

# Base de datos
db = client.cockteles

@app.route('/')
def root():
    return render_template('base.html')


# para devolver una lista (GET), o añadir (POST)
@app.route('/api/recipes', methods=['GET', 'POST'])
def api_1():
    if request.method == 'GET':
        #Si se introduce por parámetros
        if request.args:
            if request.args.get('con'):
                ingrediente = request.args.get('con')
                lista = []
                recetas = db.recipes.find( {"ingredients.name":str(ingrediente)}) # devuelve un cursor(*), no una lista ni un iterador
                for recipe in recetas:
                    recipe['_id'] = str(recipe['_id']) # paso a string
                    lista.append(recipe)
                return jsonify(lista)

            elif request.args.get('de'):
                ingrediente = request.args.get('de')
                lista = []
                recetas = db.recipes.find({"slug":str(ingrediente)}) # devuelve un cursor(*), no una lista ni un iterador
                for recipe in recetas:
                    recipe['_id'] = str(recipe['_id']) # paso a string
                    lista.append(recipe)
                return jsonify(lista)
            else:
                return jsonify({'error':'Not found'}), 404

        elif request.get_json(silent=True) is not None:
            # Si se han introducido por JSON
            request_data = request.get_json()
            if request_data:
                if request_data['con']:
                    ingrediente = request_data['con']
                    lista = []
                    recetas = db.recipes.find( {"ingredients.name":str(ingrediente)}) # devuelve un cursor(*), no una lista ni un iterador
                    for recipe in recetas:
                        recipe['_id'] = str(recipe['_id']) # paso a string
                        lista.append(recipe)
                    return jsonify(lista)

                elif request_data['de']:
                    ingrediente = request_data['de']
                    lista = []
                    recetas = db.recipes.find({"slug":str(ingrediente)}) # devuelve un cursor(*), no una lista ni un iterador
                    for recipe in recetas:
                        recipe['_id'] = str(recipe['_id']) # paso a string
                        lista.append(recipe)
                    return jsonify(lista)
                else:
                    return jsonify({'error':'No valid values introduced'}), 404
        else:
            lista = []
            buscados = db.recipes.find().sort('name')
            for recipe in buscados:
                recipe['_id'] = str(recipe['_id']) # paso a string
                lista.append(recipe)
            return jsonify(lista)

    if request.method == 'POST':

        # Si se han introducido parámetros
        request_data = request.get_json()
        name = None
        instructions = None
        ingredients = None
        slug = None
        if request_data:
            if 'name' in request_data:
                name = request_data['name']
            if 'instructions' in request_data:
                instructions = request_data['instructions']
            if 'ingredients' in request_data:
                ingredients = request_data['ingredients']
            if 'slug' in request_data:
                slug = request_data['slug']

            receta = {"name": name, "instructions":instructions, "ingredients":ingredients, "slug": slug}

            db.recipes.insert_one(receta)

            lista = []
            buscados = db.recipes.find({"name":str(name), "instructions":instructions, "ingredients":ingredients, "slug": slug})

            for recipe in buscados:
                recipe['_id'] = str(recipe['_id']) # paso a string
                lista.append(recipe)
            return jsonify(lista)
        else:
            return jsonify({'error':'No values introduced'}), 404
    else:
        return jsonify({'error':'Not valid method'}), 404


# para devolver una, modificar o borrar
@app.route('/api/recipes/<id>', methods=['GET', 'PUT', 'DELETE'])
def api_2(id):

    if request.method == 'GET':
        buscado = db.recipes.find_one({'_id':ObjectId(id)})
        if buscado:
            buscado['_id'] = str(buscado['_id']) # casting a string (es un ObjectId)
            return jsonify(buscado)
        else:
            return jsonify({'error':'Not found'}), 404

    if request.method == 'PUT':

        request_data = request.get_json()
        name = None
        instructions = None
        ingredients = None
        slug = None

        buscado = db.recipes.find_one({'_id':ObjectId(id)})
        if buscado:

            if 'name' in request_data:
                name = request_data['name']
            if 'instructions' in request_data:
                instructions = request_data['instructions']
            if 'ingredients' in request_data:
                ingredients = request_data['ingredients']
            if 'slug' in request_data:
                slug = request_data['slug']

            filter = {'_id' : ObjectId(id)}
            newvalues = { "$set": { 'name': name, 'instructions': instructions , 'ingredients': ingredients ,'slug': slug }}
            db.recipes.update_one(filter, newvalues)

            buscado = db.recipes.find_one({'_id':ObjectId(id)})
            buscado['_id'] = str(buscado['_id']) # casting a string (es un ObjectId)
            return jsonify(buscado)
        else:
            return jsonify({'error':'Not found'}), 404

    if request.method == 'DELETE':
        buscado = db.recipes.find_one({'_id':ObjectId(id)})
        if buscado:
            db.recipes.delete_one({'_id':ObjectId(id)})
            buscado_eliminado = db.recipes.find_one({'_id':ObjectId(id)})
            if buscado_eliminado is None:
                return jsonify(str(buscado['_id']))
        else:
            return jsonify({'error':'Not found'}), 404
    else:
        return jsonify({'error':'Not valid method'}), 404




api = Api(app)

class Default(Resource):
    def get(self):

        #Si se introduce por parámetros
        if request.args:
            if request.args.get('con'):
                ingrediente = request.args.get('con')
                lista = []
                recetas = db.recipes.find( {"ingredients.name":str(ingrediente)}) # devuelve un cursor(*), no una lista ni un iterador
                for recipe in recetas:
                    recipe['_id'] = str(recipe['_id']) # paso a string
                    lista.append(recipe)
                return jsonify(lista)

            elif request.args.get('de'):
                ingrediente = request.args.get('de')
                lista = []
                recetas = db.recipes.find({"slug":str(ingrediente)}) # devuelve un cursor(*), no una lista ni un iterador
                for recipe in recetas:
                    recipe['_id'] = str(recipe['_id']) # paso a string
                    lista.append(recipe)
                return jsonify(lista)
            else:
                return jsonify({'error':'Not found'}), 404

        else:
            lista = []
            buscados = db.recipes.find().sort('name')
            for recipe in buscados:
                recipe['_id'] = str(recipe['_id']) # paso a string
                lista.append(recipe)
            return jsonify(lista)

    def post(self):
        # Si se han introducido parámetros
        request_data = request.values
        name = None
        instructions = None
        ingredients = None
        slug = None
        if request_data:
            if 'name' in request_data:
                name = request_data['name']
            if 'instructions' in request_data:
                instructions = request_data['instructions']
            if 'ingredients' in request_data:
                ingredients = request_data['ingredients']
            if 'slug' in request_data:
                slug = request_data['slug']

            receta = {"name": name, "instructions":instructions, "ingredients":ingredients, "slug": slug}

            db.recipes.insert_one(receta)

            lista = []
            buscados = db.recipes.find({"name":str(name), "instructions":instructions, "ingredients":ingredients, "slug": slug})

            for recipe in buscados:
                recipe['_id'] = str(recipe['_id']) # paso a string
                lista.append(recipe)
            return jsonify(lista)
        else:
            return jsonify({'error':'No values introduced'}), 404

class Id(Resource):
    def get(self,id):

        buscado = db.recipes.find_one({'_id':ObjectId(id)})
        if buscado:
            buscado['_id'] = str(buscado['_id']) # casting a string (es un ObjectId)
            return jsonify(buscado)
        else:
            return jsonify({'error':'Not found'}), 404
    def put(self,id):

        request_data = request.values
        name = None
        instructions = None
        ingredients = None
        slug = None

        buscado = db.recipes.find_one({'_id':ObjectId(id)})
        if buscado:

            if 'name' in request_data:
                name = request_data['name']
            if 'instructions' in request_data:
                instructions = request_data['instructions']
            if 'ingredients' in request_data:
                ingredients = request_data['ingredients']
            if 'slug' in request_data:
                slug = request_data['slug']

            filter = {'_id' : ObjectId(id)}
            newvalues = { "$set": { 'name': name, 'instructions': instructions , 'ingredients': ingredients ,'slug': slug }}
            db.recipes.update_one(filter, newvalues)

            buscado = db.recipes.find_one({'_id':ObjectId(id)})
            buscado['_id'] = str(buscado['_id']) # casting a string (es un ObjectId)
            return jsonify(buscado)
        else:
            return jsonify({'error':'Not found'}), 404

    def delete(self,id):
        buscado = db.recipes.find_one({'_id':ObjectId(id)})
        if buscado:
            db.recipes.delete_one({'_id':ObjectId(id)})
            buscado_eliminado = db.recipes.find_one({'_id':ObjectId(id)})
            if buscado_eliminado is None:
                return jsonify(str(buscado['_id']))
        else:
            return jsonify({'error':'Not found'}), 404

api.add_resource(Default, '/api2/recipes')
api.add_resource(Id, '/api2/recipes/<id>')

if __name__ == '__main__':
    app.run(debug=True)







