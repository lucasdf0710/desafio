from flask import Flask, render_template, request
from flask_restful import Api
from resources.colab import Colab, Colabs
from models.colab import ColabModel
from models.forms import ColabForm, Colab_Form

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'abcd1234'

api = Api(app)

@app.before_first_request
def cria_banco():
    banco.create_all()

api.add_resource(Colabs, '/colabs')
api.add_resource(Colab, '/colabs/<string:colab_id>')

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/search", methods=["GET","POST"])
def get():
    form = Colab_Form()
    if form.validate_on_submit():
        colab = ColabModel.find_colab(form.colab_id.data)
        if colab:
            return render_template("get.html", form=form, colab=colab, aux=None)
        else:
            return render_template("get.html", form=form, colab=colab, aux=True)
    return render_template("get.html", form=form)

@app.route("/add", methods=["GET", "POST"])
def post():
    form = ColabForm()
    if form.validate_on_submit():
        objeto = ColabModel(form.colab_id.data, form.nome.data, form.idade.data, form.cargo.data)
        colab = ColabModel.find_colab(objeto.colab_id)
        if colab:
            return render_template("post.html", form=form, colab_encontrado=colab, colab_novo=None)
        else:
            objeto.save_colab()
            return render_template("post.html", form=form, colab_novo=objeto, colab_encontrado=None)
    return render_template("post.html", form=form)

@app.route("/update", methods=["GET", "POST"])
def put():
    form = ColabForm()
    if form.validate_on_submit():
        objeto = ColabModel(form.colab_id.data, form.nome.data, form.idade.data, form.cargo.data)
        colab_encontrado = ColabModel.find_colab(objeto.colab_id)
        if colab_encontrado:
            colab_encontrado.update_colab(form.nome.data, form.idade.data, form.cargo.data)
            colab_encontrado.save_colab()
            return render_template("put.html", form=form, colab_encontrado=colab_encontrado, colab_novo=None)
        else:
            objeto.save_colab()
            return render_template("put.html", form=form, colab_novo=objeto, colab_encontrado=None)
    return render_template("put.html", form=form)
@app.route("/delete", methods=["GET", "POST"])
def delete():
    form = Colab_Form()
    if form.validate_on_submit():
        colab = ColabModel.find_colab(form.colab_id.data)
        Colab.delete(Colab, form.colab_id.data)
        if colab:
            return render_template("delete.html", form=form, colab=colab)
        else:
            return render_template("delete.html", form=form, colab=colab, aux=True)
    return render_template("delete.html", form=form)

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
