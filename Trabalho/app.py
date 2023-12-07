from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from collections import defaultdict
from datetime import datetime

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
            session['id'] = user.id
            return redirect(url_for('dashboard'))
        flash('Login inválido. Verifique seu nome de usuário e senha.')
    return render_template('login.html')

# Rotas relacionadas à gestão de contas
@app.route('/inserir_conta', methods=['GET', 'POST'])
def inserir_conta():
    if request.method == 'POST' and 'id' in session:
        descricao = request.form.get('descricao')
        valor = request.form.get('valor')
        data_str = request.form.get('data')

        # Convert string to datetime
        data = datetime.strptime(data_str, '%Y-%m-%d')

        # Verifica se todos os campos obrigatórios estão preenchidos
        if descricao is not None and valor is not None and data is not None:
            # Cria uma nova conta e a adiciona ao banco de dados
            conta = Conta(descricao=descricao, valor=valor, data=data, usuario_id=session['id'])
            db.session.add(conta)
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            flash('Todos os campos devem ser preenchidos.')

    return render_template('inserir_conta.html')

@app.route('/mostrar_grafico/<ano>')
def mostrar_grafico(ano):
    ano = int(ano)

    if 'id' not in session:
        return redirect(url_for('login'))

    contas = Conta.query.filter_by(usuario_id=session['id']).all()
    contas_por_mes = {}

    # Adicionando lógica para obter anos distintos do banco de dados
    anos_do_banco_de_dados = set(conta.data.year for conta in contas)

    print("Anos do Banco de Dados:", anos_do_banco_de_dados)
    print("Ano Fornecido na Rota:", ano)

    for conta in contas:
        if conta.data.year != ano:
            continue

        mes = conta.data.month
        if mes not in contas_por_mes:
            contas_por_mes[mes] = {'total': 0, 'contas': []}

        contas_por_mes[mes]['total'] += conta.valor
        contas_por_mes[mes]['contas'].append(conta)

    return render_template('graficos.html', contas_por_mes=contas_por_mes, ano=int(ano), anos_do_banco_de_dados=anos_do_banco_de_dados, ano_selecionado=ano)

@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        return redirect(url_for('login'))
    
    contas = Conta.query.filter_by(usuario_id=session['id']).all()
    return render_template('dashboard.html', contas=contas)

@app.route('/excluir_conta/<int:conta_id>')
def excluir_conta(conta_id):
    conta = Conta.query.get_or_404(conta_id)
    db.session.delete(conta)
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Limpe a sessão ou qualquer lógica de logout necessário
    session.clear()

    # Redirecione para a página de login após o logout
    return redirect(url_for('login'))

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
