from flask_restful import Resource, reqparse
from models.colab import ColabModel
from flask import render_template

class Colabs(Resource):
    def get(self):
        #return render_template('index.html')
        return {'colabs':[colab.json() for colab in ColabModel.query.all()]} 

class Colab(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left empty")
    argumentos.add_argument('idade', type=int, required=True, help="The field 'idade' cannot be left empty")
    argumentos.add_argument('cargo', type=str, required=True, help="The field 'cargo' cannot be left empty")

    def get(self, colab_id):
        colab = ColabModel.find_colab(colab_id)
        if colab:
            return colab.json()
        return {'message':'Colab not found'}, 404

    def post(self, colab_id):
        if ColabModel.find_colab(colab_id):
            return {'message':'Colab id "{}" already exists.'.format(colab_id)}, 400

        dados = Colab.argumentos.parse_args()
        colab = ColabModel(colab_id, **dados)
        try:
            colab.save_colab()
        except:
            return {'message':'An internal error ocurred trying to save colab.'}, 500
        return colab.json()

    def put(self, colab_id):

        dados = Colab.argumentos.parse_args()
        colab_encontrado = ColabModel.find_colab(colab_id)
        if colab_encontrado:
            colab_encontrado.update_colab(**dados)
            colab_encontrado.save_colab()
            return colab_encontrado.json(), 200
        colab = ColabModel(colab_id, **dados)
        try:
            colab.save_colab()
        except:
            return {'message':'An internal error ocurred trying to save colab.'}, 500
        return colab.json(), 201

    def delete(self, colab_id):
        colab = ColabModel.find_colab(colab_id)
        if colab:
            try:
                colab.delete_colab()
            except:
                return {'message':'An error ocurred trying to delete colab'}, 500
            return {'message':'Colab deleted.'}, 200
        return {'message':'Colab not found.'}, 404

    def hello():
        return render_template('index.html')
