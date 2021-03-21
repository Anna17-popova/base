from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('id астронавта', validators=[DataRequired()])
    password = PasswordField('Пароль астронавта', validators=[DataRequired()])
    username2 = StringField('id капитана', validators=[DataRequired()])
    password2 = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'


@app.route('/')
@app.route('/index')
def index():
    text = 'Заготовка'
    return render_template('base.html', title=text)


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
        return redirect('/success')
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
