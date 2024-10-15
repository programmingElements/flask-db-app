import os
import uuid
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, Response, send_from_directory, jsonify, session, make_response, flash
from flask_mysqldb import MySQL


app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
app.secret_key = 'SOMECONTENTKEY'

database_host = os.environ.get('DATABASE_HOST')
database_user = os.environ.get('DATABASE_USER')
database_password = os.environ.get('DATABASE_PASSWORD')
database_db = os.environ.get('DATABASE_DB')

# Database Connectivity
# app.config['MYSQL_HOST'] = 'database-1.c1asso82qaoo.ap-south-1.rds.amazonaws.com'
# app.config['MYSQL_USER'] = 'admin'
# app.config['MYSQL_PASSWORD'] = 'Mkrishna*672'
# app.config['MYSQL_DB'] = 'flaskdbapp'

app.config['MYSQL_HOST'] = database_host
app.config['MYSQL_USER'] = database_user
app.config['MYSQL_PASSWORD'] = database_password
app.config['MYSQL_DB'] = database_db


mysql = MySQL(app)

background_color = os.environ.get('BACKGROUND_COLOR');

@app.route('/', methods=['GET', 'POST'])
def index():
  if (request.method == "GET"):
    return render_template('index.html', color=background_color)
  elif (request.method == "POST"):
    username = request.form.get('username')
    password = request.form.get('password')
    if username == "neuralnine" and password == "123456":
      return "Success"
    else:
      return "Failure"

@app.route('/employees')
def employees():
  # employees=[{'emp_name': "CHAKRAVARTHI", 'emp_mail': "CHAKRI@GMAIL.COM", 'emp_sal': 30000, 'emp_city': "SRIKAKULAM"}]
  cur = mysql.connection.cursor()
  cur.execute('''select * from employees''')
  data = cur.fetchall()
  cur.close()
  return render_template('employees.html',employees=data)

@app.route('/add-employee', methods=['GET','POST'])
def add_employee():
  if (request.method == 'GET'):
    return render_template('addEmployee.html')
  elif (request.method == 'POST'):
    emp_name = request.form.get('emp_name')
    emp_mail = request.form.get('emp_mail')
    emp_sal = request.form.get('emp_sal')
    emp_city = request.form.get('emp_city')

    cur = mysql.connection.cursor()
    cur.execute('''insert into employees (emp_name, emp_mail, emp_sal, emp_city) values (%s, %s, %s, %s)''', (emp_name, emp_mail, emp_sal, emp_city))
    mysql.connection.commit()
    flash("Employee Data Inserted Successfully!")
    return redirect(url_for('employees'))

@app.route('/update-employee/<int:emp_id>', methods=['GET','POST'])
def update_employee(emp_id):
  if request.method == 'GET':
    cur = mysql.connection.cursor()
    cur.execute("select * from employees where emp_id="+str(emp_id))
    data = cur.fetchall()
    print(data[0])
    cur.close()
    return render_template('updateEmployee.html', emp_id=emp_id, employee=data[0])
  elif request.method == 'POST':
    id_data = request.form.get('id')
    name = request.form.get('emp_name')
    email = request.form.get('emp_mail')
    salary = request.form.get('emp_sal')
    city = request.form.get('emp_city')

    cur = mysql.connection.cursor()
    cur.execute("""
    update employees set emp_name=%s, 
    emp_mail=%s, emp_sal=%s, emp_city=%s
    where emp_id=%s
    """, (name, email, salary, city, id_data))
    mysql.connection.commit()
    flash("Employee Data Updated Successfully!")
    return redirect(url_for('employees'))

@app.route('/delete-employee/<int:emp_id>', methods=['GET', 'POST'])
def delete_employee(emp_id):
  if (request.method == 'GET'):
    return render_template('deleteEmployee.html', emp_id=emp_id)
  elif request.method == 'POST':
    id_data = request.form.get('id')
    cur = mysql.connection.cursor()
    cur.execute("""
    delete from employees where emp_id=%s
    """, (id_data))
    mysql.connection.commit()
    flash("Employee Data Deleted Successfully!")
    return redirect(url_for('employees'))
    



@app.route('/dashboard')
def dashboard():
  return render_template('dashboard.html', message="Dashboard")

@app.route('/set_data')
def set_data():
  session['name'] = 'Mike'
  session['other'] = 'Hello World'
  return render_template('dashboard.html', message="Session data set.")  

@app.route('/get_data')
def get_data():
  if "name" in session.keys() and "other" in session.keys():
    name = session['name']
    other = session['other']
    return render_template('dashboard.html', message=f'Name: {name}, Other: {other}')
  else:
    return render_template('dashboard.html', message=f'No session found.')

@app.route('/clear_session')
def clear_session():
  session.clear()
  return render_template('dashboard.html', message='Session Cleared.')

@app.route('/set_cookie')
def set_cookie():
  response = make_response(render_template('dashboard.html', message='Cookie set.'))
  response.set_cookie('cookie_name', 'cookie_value')
  return response

@app.route('/get_cookie')
def get_cookie():
  if "cookie_name" in request.cookies.keys():
    cookie_value = request.cookies['cookie_name']
    return render_template('dashboard.html', message=f'Cookie Value: {cookie_value}')
  else:
    return render_template('dashboard.html', message=f'No cookie found.')

@app.route('/remove_cookie')
def remove_cookie():
  if "cookie_name" in request.cookies.keys():
    response = make_response(render_template('dashboard.html', message='Cookie Removed.'))
    response.set_cookie('cookie_name', expires=0)
    return response
  else:
    return render_template('dashboard.html', message=f'No cookie found.')

@app.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  elif request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'neuralnine' and password == '123456':
      flash('Successful Login!')
      return render_template('dashboard.html', message=f'')
    else:
      flash('Login Failed!')
      return render_template('dashboard.html', message=f'')

@app.route('/file_upload', methods=["POST"])
def file_upload():
  file = request.files['file']

  if file.content_type == 'text/plain':
    return file.read().decode()
  elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or file.content_type == 'application/vnd.ms-excel':
    df = pd.read_excel(file)
    return df.to_html()

@app.route('/convert_csv', methods=['POST'])
def convert_csv():
  file = request.files['file']
  df = pd.read_excel(file)
  response = Response(
    df.to_csv(),
    mimetype='text/csv',
    headers={
      'Content-Disposition': 'attachment; filename=result.csv'
    }
  )
  return response

@app.route('/convert_csv_two', methods=['POST'])
def convert_csv_two():
  file = request.files['file']

  df = pd.read_excel(file)

  if not os.path.exists('downloads'):
    os.makedirs('downloads')

  filename = f'{uuid.uuid4()}.csv'
  df.to_csv(os.path.join('downloads', filename))

  return render_template('download.html', filename=filename)

@app.route('/download/<filename>')
def download(filename):
  return send_from_directory('downloads', filename, download_name='result.csv')


@app.route('/handle_post', methods=['POST'])
def handle_post():
  greeting = request.json['greeting']
  name = request.json['name']

  with open('file.txt', 'w') as f:
    f.write(f'{greeting}, {name}')
  
  return jsonify({'message': 'Successfully written!'})

@app.route('/home')
def home():
  some_text = "Hello World!"
  return render_template('home.html', some_text=some_text)

@app.template_filter('reverse_string')
def reverse_string(s):
  return s[::-1]

@app.template_filter('repeat')
def repeat(s,times=2):
  return s * times

@app.template_filter('alternate_case')
def alternate_case(s):
  return ''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(s)])

@app.route('/redirect_endpoint')
def redirect_endpoint():
  return redirect(url_for('home'))



if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5001, debug=True)