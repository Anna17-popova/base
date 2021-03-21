from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from data.login import LoginForm
from data import db_session
from data.users import User
from data.jobs import Jobs
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort


app = Flask(__name__)
db_session.global_init("db/mars_explorer.db")
app.config['SECRET_KEY'] = 'my_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    mylist = []
    db_sess = db_session.create_session()
    text = 'Журнал работ'
    for job in db_sess.query(Jobs).all():
        a = [job.id, job.job, db_sess.query(User).filter(User.id == job.team_leader).first(), job.work_size, job.collaborators, 'Is finished'
        if job.is_finished == 1 else 'Is not finished']
        mylist.append(a)
    print(mylist)
    return render_template('table_jobs.html', title=text, mylist=mylist)


@app.route('/training/<prof>')
def training(prof):
    return render_template('professions.html', prof=prof)


@app.route('/list_prof/<type>')
def list_prof(type):
    if type not in 'olul':
        print('WRONG PARAMS')
        return
    return render_template('list_professions.html', type=type)


@app.route('/answer')
@app.route('/auto_answer')
def auto_answer():
    title, surname, name, education, profession, sex, motivation, ready =\
        'Анкета', 'Popova', 'Anna', '-', '-',\
        'female', 'Всегда мечтал застрять на Марсе!', 'True'
    return render_template('auto_answer.html', title=title, surname = surname, name=name, education=education,
                           profession=profession, sex=sex, motivation=motivation, ready=ready)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('log.html',
                                message="Неправильное имя или пароль",
                                form=form)
    return render_template('log.html', title='Авторизация', form=form)


@app.route('/distribution')
def distribution():
    mylist = ['Ридли Скотт', 'Энди Уир', 'Марк Уотни', 'Венката Капур', 'Тедди Сандерс']
    return render_template('distribution.html', mylist=mylist)


@app.route('/table/<sex>/<int:age>')
def table(sex, age):
    return render_template('table.html', sex=sex, age=age)


if __name__ == '__main__':
    app.run(port=8070, host='127.0.0.1')
