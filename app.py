from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify
from werkzeug.exceptions import abort
from models import app
from models import Aluno
from flask_restful import Resource, Api

from views.anamnese import ViewsAnamnese
from views.alunos import ViewsAluno
from views.site import ViewsSite
ViewsSite(app)
ViewsAluno(app, Aluno)
ViewsAnamnese(app)

# ROTAS RELATIVAS A AUTENTICAÇÃO ===========================================#


# ROTA PARA AUTENTICAÇÃO NA ÁREA LOGADA
@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if 'master' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(request.form['usuario'] + 'logou com sucesso!')
        return redirect('/menu_area_logada.html')
    else:
        flash('Não logado. Tente novamente!')
        return redirect('login')


# ROTA PARA LOGOUT
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect('/')


# ROTA DIRETA PARA O MENU ÁREA LOGADA
@app.route('/menu_area_logada.html')
def menu_area_logada():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Login Obrigatório!')
        return redirect('Site/login')
    return render_template('Site/menu_area_logada.html', titulo='Menu Área Logada')


api = Api(app)


class Dados(Resource):
    def get(self, ra):
        dados_aluno = Aluno.query.filter_by(ra=ra).first()
        if dados_aluno is None:
            abort(484)
        retorno = {}
        retorno['nome'] = dados_aluno.nome_aluno
        retorno['ra'] = dados_aluno.ra
        retorno['nascimento'] = dados_aluno.nascimento
        retorno['serie'] = dados_aluno.num_ser
        retorno['turma'] = dados_aluno.turma
        retorno['nome_mae'] = dados_aluno.nome_mae
        retorno['nome_pai'] = dados_aluno.nome_pai
        return retorno


api.add_resource(Dados, '/dados_aluno/<int:ra>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
