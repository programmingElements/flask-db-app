# Flask Application With MySQL DB

  Flask Installation Guide and Docs : https://flask.palletsprojects.com/en/3.0.x/installation/#python-version

  
  Flask Documentation : https://flask.palletsprojects.com/en/3.0.x/

  flask run --help [ To take help from the flask run commands ]

  flask run -h 0.0.0.0 -p 5001 --debug [ To run the flask app with host , port , debug on mode ]

         (or)

  python app.py

  pip3 freeze [ To see list of softwares and dependencies ]

  pip3 freeze > requirements.txt [ To store the list of softwares into the requirements.txt ]

  pip3 install -r requirements.txt [ To install all softwares and dependencies require for application using requirements file ]

  curl <website-url>

  curl http://127.0.0.1:5001/hello

  curl -I <website-url>

  curl -I http://127.0.0.1:5001/hello

 

### Code of Url & Routes in Flask

  from flask import Flask, request, make_response

  app = Flask(__name__)

  @app.route('/')
  def index():
    return "<h1>Welcome to the Python Flask Application</h1>"

  '''
  @app.route('/hello', methods=["GET","POST"])
  def hello():
    if (request.method == "GET"):
      return "You made a GET request\n"
    elif (request.method == "POST"):
      return "You made a POST request\n"
    else:
      return "You will never see this message\n"
  '''

  @app.route('/hello')
  def hello():
    response = make_response('Hello World\n')
    response.status_code = 202
    response.headers['content-type'] = 'application/octet-stream'
    return response

  # url params
  @app.route('/greet/<name>')
  def greet(name):
    return f"<h1>Hello {name}</h1>"

  # url params
  @app.route('/add/<int:num1>/<int:num2>')
  def add(num1,num2):
    return f"<h2>{num1} + {num2} = {num1 + num2}</h2>"

  # url query params
  @app.route('/handle_url_params')
  def handle_params():
    if ('greeting' in request.args.keys() and 'name' in request.args.keys()):
      greeting = request.args['greeting']
      name = request.args.get('name')
      return f'{greeting}, {name}'
    else:
      return 'Some parameters are missing'

  if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)


## Code for templates rendering & filters, custom filters

  from flask import Flask, render_template, redirect, url_for

  app = Flask(__name__, template_folder='templates')

  @app.route('/')
  def index():
    mylist = [10, 20, 30, 40, 50]
    return render_template('index.html', mylist=mylist)

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





## MYSQL DB CLI Commands to Connect Client

   mysql --host=localhost --user=myname --password=password mydb
   mysql -h localhost -u myname -ppassword mydb

## MYSQL DB Commands

create database flaskdbapp;
use flaskdbapp;
create table employees (
  emp_id int NOT NULL AUTO_INCREMENT,
  emp_name varchar(255),
  emp_mail varchar(255) NOT NULL,
  emp_sal int,
  emp_city varchar(255),
  PRIMARY KEY (emp_id)
);
select * from employees;

