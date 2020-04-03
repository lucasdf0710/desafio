from sql_alchemy import banco

class ColabModel(banco.Model):
    __tablename__ = 'colabs'

    colab_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    idade = banco.Column(banco.Float)
    cargo = banco.Column(banco.String(80))

    def __init__(self, colab_id, nome, idade, cargo):
        self.colab_id = colab_id
        self.nome = nome
        self.idade = idade
        self.cargo = cargo

    def json(self):
        return {
            'colab_id': self.colab_id,
            'nome': self.nome,
            'idade': self.idade,
            'cargo': self.cargo

        }

    @classmethod
    def find_colab(cls, colab_id):
        colab = cls.query.filter_by(colab_id=colab_id).first()
        if colab:
            return colab
        return None

    def save_colab(self):
        banco.session.add(self)
        banco.session.commit()

    def update_colab(self, nome, idade, cargo):
        self.nome = nome
        self.idade = idade
        self.cargo = cargo

    def delete_colab(self):
        banco.session.delete(self)
        banco.session.commit()
