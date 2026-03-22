from gkcsystems import app, database
from forms import CriarContaForm, LoginForm
from gkcsystems.models import Usuarios, Projetos


# o codigo abaixo é apenas para criar o banco de dados, pode deixar comentado
with app.app_context():
    database.drop_all()
    database.create_all()

# with app.app_context():
#     usuario = Usuarios(nome='Greg', email='greg_kaippert@hotmail.com', senha='123456')
#     usuario2 = Usuarios(nome='Tati', email='taty@hotmail.com', senha='123456')
#     usuario3 = Usuarios(nome='Tina', email='tina@hotmail.com', senha='123456')
#
#     database.session.add(usuario)
#     database.session.add(usuario2)
#     database.session.add(usuario3)
#
#     database.session.commit()

# with app.app_context():
#     usuario = Usuarios.query.filter_by(id=3)
#     print(usuario)

# with app.app_context():
#     projeto1 = Projetos(id_usuario=1, titulo='Automação', descricao='Feito com Pyautogui e Scelenium', link_video='https://www.google.com')
#     projeto2 = Projetos(id_usuario=2, titulo='Desenvolvimento web', descricao='Feito com Flask e Django', link_video='https://www.google.com')
#     database.session.add(projeto1)
#     database.session.add(projeto2)
#
#     database.session.commit()

# with app.app_context():
#     projetos = Projetos.query.all()
#     print(projetos[0].desenvolvedor.nome)
#     print(projetos[1].desenvolvedor.email)
#     print(projetos[0].link_video)
