from sqlalchemy.orm import backref
from gkcsystems import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    # funcao query.get automaticamente retorna a chave primaria, que no caso é o campo ID na classe Usuarios
    return Usuarios.query.get(int(id_usuario))

class Usuarios(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    cv = database.Column(database.String, nullable=False, default='Não informado')
    linkedin = database.Column(database.String, nullable=False, default='Não informado')
    phone = database.Column(database.String, nullable=False)
    endereco = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, nullable=False, default='default-user.png')
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now())

    # aqui o parametro backref serve para referenciar a tabela Projetos com Usuario
    # Ou seja, quando quiser ver o email da pessoa que criou o projeto
    # só escrever Projetos.dev.nome
    projetos = database.relationship('Projetos', backref='dev', lazy=True)


class Projetos(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    descricao = database.Column(database.Text)
    link_video = database.Column(database.String, nullable=False)
    # ferramentas_usadas será armazenadas todas as ferrasmentas utilizadas no projeto
    # Ex: Python, Jquery, Bootstrap
    ferramentas_usadas = database.Column(database.String, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuarios.id'), nullable=False)

