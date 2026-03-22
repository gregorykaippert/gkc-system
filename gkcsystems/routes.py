from sqlalchemy import DateTime

from gkcsystems import app, database, bcrypt, login_manager
from flask import render_template, url_for, flash, redirect, request, abort
from gkcsystems.forms import LoginForm, CriarContaForm, EditarPerfilForm, CadastrarProjeto
from gkcsystems.models import Usuarios, Projetos
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from datetime import datetime
import time, os, secrets
from PIL import Image

@app.route('/')
def index():
    ano = datetime.today().year
    projetos = Projetos.query.all()
    return render_template('index.html', ano=ano, projetos=projetos)

@app.route('/projetos/<id_projeto>/excluir')
@login_required
def excluir_projeto(id_projeto):
    if current_user.is_authenticated:
        projeto = Projetos.query.get(id_projeto)
        database.session.delete(projeto)
        database.session.commit()
        flash(f'Projeto {id_projeto} excluído com sucesso!', 'alert-warning')
        return redirect(url_for('index'))
    else:
        abort(code=403)

@app.route('/contact')
def contato():
    ano = datetime.today().year
    return render_template('contact.html', ano=ano)

@app.route('/usuarios')
@login_required
def conta():
    ano = datetime.today().year
    return render_template(template_name_or_list='conta.html', ano=ano)

@app.route('/youtube')
def youtube():
    ano = datetime.today().year
    return render_template('youtube.html', ano=ano)

@app.route('/login', methods=['GET', 'POST'])
def login():
    ano = datetime.today().year
    login_form = LoginForm()
    criar_conta_form = CriarContaForm()
    if login_form.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuarios.query.filter_by(email=login_form.email_login.data).first()
        #print(usuario)
        if usuario == None: # verifica se existe o usuario
            flash('Usuário não cadastrado. Cadastra-se ao lado.', 'alert-warning')
        elif usuario and bcrypt.check_password_hash(usuario.senha, login_form.password_login.data):
            # verifica se a senha esta ok
            login_user(usuario, remember=login_form.manter_conectado.data)
            flash(f'Seja bem vindo {login_form.email_login.data}, login realizado com sucesso!', 'alert-success')
            parametro_next = request.args.get('next')
            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for('index'))
        else:
            # usuario existe porem senha errada
            flash('Dados informados incorretos.', 'alert-danger')

    if criar_conta_form.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        #criar a conta
        senha_cript = bcrypt.generate_password_hash(criar_conta_form.password.data)
        usuario = Usuarios(nome=criar_conta_form.username.data, email=criar_conta_form.email.data, senha=senha_cript, phone=criar_conta_form.phone.data, endereco=criar_conta_form.endereco.data)
        # adicionar dados a sessao
        database.session.add(usuario)
        # commit com os dados
        database.session.commit()

        flash(f'Seja bem vindo {criar_conta_form.username.data}, sua conta foi criada com sucesso!', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', login_form=login_form, criar_conta_form=criar_conta_form, ano=ano)

@app.route('/login-gregory')
def login_gregory():
    ano = datetime.today().year
    login_form = LoginForm()
    criar_conta_form = CriarContaForm()
    return render_template('login2.html', login_form=login_form, criar_conta_form=criar_conta_form, ano=ano)

@app.route('/sair')
def sair():
    logout_user()
    flash('Logout com sucesso!', 'alert-success')
    return redirect(url_for('index'))

@app.route('/perfil')
def perfil():
    ano = datetime.today().year
    dados = Usuarios.query.first()
    return render_template('perfil.html', ano=ano, dados=dados)

def salvar_arquivo(arquivo):
    # gerar nome aleatorio do arquivo
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(arquivo.filename)
    nome_arquivo = nome + codigo + extensao

    if extensao == '.jpg' or extensao == '.png':
        caminho_completo = os.path.join(app.root_path, 'static/foto_perfil/', nome_arquivo)
        # reduzir tamanho da imagem
        tamanho = (400,400)
        arquivo = Image.open(arquivo)
        arquivo.thumbnail(tamanho)
        # salvar na pasta
        arquivo.save(caminho_completo)

    elif extensao == '.pdf' or extensao == '.docx':
        # salvar na pasta
        caminho_completo = os.path.join(app.root_path, 'static/curriculo/', nome_arquivo)
        arquivo.save(caminho_completo)
    else:
        caminho_completo = os.path.join(app.root_path, 'static/videos/', nome_arquivo)
        arquivo.save(caminho_completo)

    return nome_arquivo

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def perfil_editar():
    ano = datetime.today().year
    form = EditarPerfilForm()
    if request.method == 'GET':
        form.username.data = current_user.nome
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.endereco.data = current_user.endereco
        form.linkedin.data = current_user.linkedin

    elif request.method == 'POST' and form.validate_on_submit() and 'botao_submit_editar_perfil' in list(request.form.to_dict().keys()):

        current_user.nome = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.endereco = form.endereco.data
        if form.linkedin.data:
            current_user.linkedin = form.linkedin.data
        else:
            current_user.linkedin = 'Não informado'

        if form.cv.data:
            current_user.cv = salvar_arquivo(form.cv.data)

        database.session.commit()
        flash('{}, seu perfil foi atualizado com sucesso!'. format(current_user.nome), 'alert-success')
        return redirect(url_for('perfil'))

    elif 'botao_editar_foto' in list(request.form.to_dict().keys()):

        # print(form.errors)
        # print(form.foto_perfil.data)
        if form.foto_perfil.data and 'foto_perfil' not in form.errors:
            current_user.foto_perfil = salvar_arquivo(form.foto_perfil.data)
            database.session.commit()
            flash('{}, sua foto foi atualizada com sucesso!'. format(current_user.nome), 'alert-success')
        elif form.foto_perfil.data and 'foto_perfil' in form.errors:
            flash('{}'.format(form.errors['foto_perfil'][0]), 'alert-warning')
        else:
            flash('{}, você deve escolher pelo menos uma foto de perfil!'. format(current_user.nome), 'alert-warning')

        return redirect(url_for('perfil_editar'))

    elif 'botao_excluir_foto' in list(request.form.to_dict().keys()):
        os.remove(os.path.join(app.root_path, 'static/foto_perfil/', current_user.foto_perfil))
        current_user.foto_perfil = 'default-user.png'
        database.session.commit()
        flash('{}, sua foto foi excluída com sucesso!'. format(current_user.nome), 'alert-warning')
        return redirect(url_for('perfil'))

    return render_template('perfil_editar.html', form=form, ano=ano)

@app.route('/projetos/criar', methods=['GET', 'POST'])
@login_required
def create_projetos():
    ano = datetime.today().year
    form = CadastrarProjeto()
    if form.validate_on_submit():
        projeto = Projetos(
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            ferramentas_usadas=form.ferramentas_usadas.data,
            link_video=salvar_arquivo(form.upload_video.data),
            id_usuario=current_user.id
        )
        database.session.add(projeto)
        database.session.commit()
        flash('Projeto cadastrado com sucesso!', 'alert-success')
        return redirect(url_for('index'))
    return render_template('projetos.html', ano=ano, form=form)

@app.route('/projetos/listar')
def listar_projetos():
    ano = datetime.today().year
    projetos = Projetos.query.all()
    return render_template('projetos.html', ano=ano, projetos=projetos)