from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from collections import defaultdict


app = Flask(__name__)

# Configuração do banco de dados SQLite e chave secreta para proteção CSRF
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contas.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Substitua por uma chave secreta forte

# Instância do SQLAlchemy para interação com o banco de dados
db = SQLAlchemy(app)

# Modelo de dados para a tabela 'Usuario'
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)

    def __repr__(self):
        return f'<Usuario {self.username}>'

# Modelo de dados para a tabela 'Conta'
class Conta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    descricao = db.Column(db.String(120), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Conta {self.descricao}>'

# Rotas relacionadas ao cadastro e login de usuários
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

        if Usuario.query.filter_by(username=username).first():
            flash('Nome de usuário já em uso. Escolha outro.')
        else:
            user = Usuario(username=username)
            user.set_senha(senha)
            db.session.add(user)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça o login.')
            return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

        user = Usuario.query.filter_by(username=username).first()

        if user and user.verificar_senha(senha):
            session['username'] = username
            return redirect(url_for('dashboard'))
        flash('Login inválido. Verifique seu nome de usuário e senha.')
    return render_template('login.html')

# Rotas relacionadas à gestão de contas
from datetime import datetime

@app.route('/inserir_conta', methods=['GET', 'POST'])
def inserir_conta():
    if request.method == 'POST':
        descricao = request.form.get('descricao')
        valor = request.form.get('valor')
        data_str = request.form.get('data')

        # Convert string to datetime
        data = datetime.strptime(data_str, '%Y-%m-%d')

        # Verifies if all mandatory fields are filled
        if descricao is not None and valor is not None and data is not None:
            # Creating a new account and adding it to the database
            conta = Conta(descricao=descricao, valor=valor, data=data, usuario_id=1)
            db.session.add(conta)
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            flash('All fields must be filled.')

    return render_template('inserir_conta.html')


@app.route('/mostrar_grafico')
def mostrar_grafico():
    contas = Conta.query.all()
    dados_grafico = defaultdict(lambda: defaultdict(float))

    for conta in contas:
        ano = conta.data.year
        mes = conta.data.month
        dados_grafico[ano][mes] += conta.valor

    return mostrar_grafico

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    contas = Conta.query.all()
    return render_template('dashboard.html', contas=contas)

@app.route('/excluir_conta/<int:conta_id>')
def excluir_conta(conta_id):
    conta = Conta.query.get_or_404(conta_id)
    db.session.delete(conta)
    db.session.commit()

    return redirect(url_for('dashboard'))

# Função para criar as tabelas no banco de dados
def create_tables():
    with app.app_context():
        print('Criando as tabelas')
        db.create_all()

# Verifica se o script está sendo executado diretamente
if __name__ == '__main__':
    # Cria as tabelas no banco de dados
    create_tables()
    # Inicia a aplicação em modo de depuração
    app.run(debug=True)