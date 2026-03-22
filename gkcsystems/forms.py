from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from pyexpat.errors import messages
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from gkcsystems.models import Usuarios


class CriarContaForm(FlaskForm):
    username = StringField('Nome completo', validators=[DataRequired(message='Campo nome de usuário obrigatório o preenchimento.')])
    email = StringField('Email', validators=[DataRequired(message='Campo email obrigatório o preenchimento.'), Email()])
    password = PasswordField('Senha', validators=[DataRequired(message='Campo senha obrigatório o preenchimento.'), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirmar senha', validators=[DataRequired(message='Campo confirmar senha obrigatório o preenchimento.'), EqualTo('password', message='Campo senha e confirmar senha devem ser iguais!')])
    phone = StringField('Telemóvel', validators=[DataRequired(message='Campo telemóvel obrigatório o preenchimento.')])
    endereco = StringField('Endereço', validators=[DataRequired(message='Campo endereco obrigatório o preenchimento.')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuarios.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado, escolha outro ou faça login.')


class LoginForm(FlaskForm):
    email_login = StringField('Email', validators=[DataRequired(message='Campo email obrigatório o preenchimento.'), Email('Campo email inválido.')])
    password_login = PasswordField('Senha', validators=[DataRequired(message='Campo senha obrigatório o preenchimento.'), Length(min=6, max=20, message='Campo senha deve conter entre 6 e 20 caracteres.')])
    manter_conectado = BooleanField('Deseja continuar conectado ?')
    botao_submit_login = SubmitField('Login')


class EditarPerfilForm(FlaskForm):
    username = StringField('Nome', validators=[DataRequired(message='Campo nome de usuário obrigatório o preenchimento.')])
    email = StringField('Email', validators=[DataRequired(message='Campo email obrigatório o preenchimento.'), Email('Campo email inválido.')])
    phone = StringField('Telemóvel', validators=[DataRequired(message='Campo telemóvel obrigatório o preenchimento.')])
    endereco = StringField('Endereço', validators=[DataRequired(message='Campo endereço obrigatório o preenchimento.')])
    linkedin = StringField('Linkedin')
    cv = FileField('Currículo', validators=[FileAllowed(['pdf', 'docx'], message='Apenas extensão de arquivos: (PDF ou DOCX) permitidos.')])
    foto_perfil = FileField('Selecionar foto', validators=[FileAllowed(['png', 'jpg'], message='Apenas extensão de imagem: (PNG ou JPG) permitidos.')])
    botao_editar_foto = SubmitField('Enviar foto')
    botao_excluir_foto = SubmitField('Excluir foto')
    botao_submit_editar_perfil = SubmitField('Editar Perfil')


class CadastrarProjeto(FlaskForm):
    titulo = StringField('Título do projeto', validators=[DataRequired('Campo título obrigatório o preenchimento!')])
    descricao = TextAreaField('Descrição do projeto', validators=[DataRequired('Campo descrição obrigatório o preenchimento!')])
    ferramentas_usadas = StringField('Ferramentas utilizadas', validators=[DataRequired('Campo ferramentas obrigatório o preenchimento!')])
    link_video = StringField('Link do vídeo')
    upload_video = FileField('Carregar vídeo do projeto', validators=[DataRequired('Obrigatório o envio de uma demonstração do projeto.')])
    botao_submit_projetos = SubmitField('Cadastrar projetos')

