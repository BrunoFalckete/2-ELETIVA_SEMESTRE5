# Importando os módulos necessários do Flask e outras bibliotecas
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, render_template

# Criando uma instância da aplicação Flask
app = Flask(__name__)

# Configurando o banco de dados SQLite e a chave secreta para proteção CSRF
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contas.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Substitua por uma chave secreta forte

# Criando uma instância do SQLAlchemy para interação com o banco de dados
db = SQLAlchemy(app)

# Definindo o modelo de dados para a tabela 'Usuario'
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

    # Método para definir a senha usando hash
    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    # Método para verificar a senha usando hash
    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)

    # Método de representação para depuração
    def __repr__(self):
        return f'<Usuario {self.username}>'

# Definindo o modelo de dados para a tabela 'Conta'
class Conta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    descricao = db.Column(db.String(120), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False)

    # Método de representação para depuração
    def __repr__(self):
        return f'<Conta {self.descricao}>'

# Rota para o cadastro de usuários
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Obtendo dados do formulário
        username = request.form['username']
        senha = request.form['senha']
        
        # Verificando se o nome de usuário já está em uso
        if Usuario.query.filter_by(username=username).first():
            flash('Nome de usuário já em uso. Escolha outro.')
        else:
            # Criando um novo usuário e adicionando ao banco de dados
            user = Usuario(username=username)
            user.set_senha(senha)
            db.session.add(user)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça o login.')
            return redirect(url_for('login'))
    return render_template('cadastro.html')

# Rota para o login de usuários
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtendo dados do formulário
        username = request.form['username']
        senha = request.form['senha']
        
        # Procurando o usuário no banco de dados
        user = Usuario.query.filter_by(username=username).first()

        # Verificando a senha
        if user and user.verificar_senha(senha):
            session['username'] = username
            return redirect(url_for('dashboard'))
        flash('Login inválido. Verifique seu nome de usuário e senha.')
    return render_template('login.html')

# Rota para adicionar uma nova conta
@app.route('/inserir_conta', methods=['GET', 'POST'])
def adicionar_conta():
    if request.method == 'POST':
        # Obtendo dados do formulário
        descricao = request.form['descricao']
        valor = request.form['valor']
        data = request.form['data']
        
        # Criando uma nova conta e adicionando ao banco de dados
        conta = Conta(descricao=descricao, valor=valor, data=data, usuario_id=1)
        db.session.add(conta)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('inserir_conta.html')

# Rota para mostrar o gráfico por ano
@app.route('/mostrar_grafico')
def mostrar_grafico():
    return 'Gráfico mostrado' 

# Rota principal para o dashboard
@app.route('/dashboard')
def dashboard():
    # Recupera a lista de contas do banco de dados e a passa para o template
    if not 'username' in session:
            return redirect(url_for('login'))
        
    contas = Conta.query.all()
    return render_template('dashboard.html', contas=contas)

# Rota para excluir uma conta
@app.route('/excluir_conta/<int:conta_id>')
def excluir_conta(conta_id):
    # Obtém a conta pelo ID e a remove do banco de dados
    conta = Conta.query.get_or_404(conta_id)
    db.session.delete(conta)
    db.session.commit()

    return redirect(url_for('dashboard')) # Ou redirecione para uma página específica

# Função para criar as tabelas no banco de dados
def create_tables():
    with app.app_context():
        print('Criando as tabelas')
        db.create_all()

# Verificando se o script está sendo executado diretamente
if __name__ == '__main__':
    # Criando as tabelas no banco de dados
    create_tables()
    # Iniciando a aplicação em modo de depuração
    app.run(debug=True)
