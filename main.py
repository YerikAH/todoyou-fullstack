from flask import Flask, request, render_template, make_response, redirect, session,url_for, abort, flash
from flask_login import login_required
import unittest
from app import create_app
from app.forms import LoginForm
from app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm
from flask_login import login_user, current_user, login_required, logout_user
from app.firestore_service import get_users,get_todos,get_user, user_put, put_todo, delete_todo,update_todo
from app.models import UserModel , UserData
from werkzeug.security import generate_password_hash


app = create_app()


task = [
  'Compar un delicioso café.',
  'Estudiar 24 horas haciendo ayuno de dopamina.',
  'Cocinar una taza de chocolate caliente.'
]

# Test
@app.cli.command()
def test():
  tests = unittest.TestLoader().discover('tests')
  unittest.TextTestRunner().run(tests)


# Error

@app.errorhandler(404)
def error_not_found(error):
  return render_template('404.html',error=error)

@app.errorhandler(500)
def error_server(error):
  return render_template('500.html',error=error)

@app.route('/')
def index():
  ip_get = request.remote_addr
  redirect_center = make_response(redirect('/center'))
  session['ip_get'] = ip_get

  return redirect_center

@app.route('/center',methods = ['GET','POST'])
@login_required
def center():
  ip_get = session.get('ip_get')
  fullname = current_user.id
  todo_form = TodoForm()
  delete_form = DeleteTodoForm()
  update_form = UpdateTodoForm()
  context = {
    'ip_get' : ip_get,
    'task':get_todos(user_id=fullname),
    'fullname':fullname,
    'todo_form':todo_form,
    'delete_form':delete_form,
    'update_form':update_form
  }
  if todo_form.validate_on_submit():
    put_todo(user_id=fullname, description=todo_form.description.data)
    return redirect(url_for('center'))

  return render_template('app.html',**context)

@app.route('/login',methods = ['GET','POST'])
def login():
  login_form = LoginForm()
  context = {
    'login_form' : login_form
  }
  if login_form.validate_on_submit():
    fullname = login_form.fullname.data
    password = login_form.password.data
    user_doc = get_user(fullname)

    if user_doc.to_dict() is not None:
      password_from_db = user_doc.to_dict()['password']
      if password == password_from_db:
        user_data = UserData(fullname,password)
        user = UserModel(user_data)

        login_user(user)
        flash("Welcome again")
        
        redirect(url_for('center'))
      else:
        flash("The password that you enter is incorrect")

    else:
      flash("Username don't exists")

    return redirect(url_for('index'))
    
  return render_template('login.html',**context)


@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash("Come back soon")
  return redirect(url_for('login'))

@app.route('/signup',methods = ['GET','POST'])
def signup():
  signup_form = LoginForm()
  context = {
    'signup_form' : signup_form
  }
  if signup_form.validate_on_submit():
    fullname = signup_form.fullname.data
    password = signup_form.password.data

    user_doc = get_user(fullname)

    if user_doc.to_dict() is None:
      password_hash = generate_password_hash(password)
      user_data = UserData(fullname, password_hash)
      user_put(user_data)
      user = UserModel(user_data)

      login_user(user)

      flash('Welcome!')

      return redirect(url_for('center'))


    else:
      flash('Sorry the user already exists')


  return render_template('signup.html', **context)

@app.route('/todos/delete/<todo_id>',methods = ['POST'])
def delete(todo_id):
  user_id =  current_user.id
  delete_todo(user_id=user_id, todo_id=todo_id)

  return redirect(url_for('center'))

@app.route('/todos/update/<todo_id>/<int:done>',methods = ['POST'])
def update(todo_id,done):
  user_id =  current_user.id
  update_todo(user_id=user_id, todo_id=todo_id, done=done)

  return redirect(url_for('center'))