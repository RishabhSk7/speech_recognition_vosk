from flask import Flask, redirect, url_for, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def Index():
   return "This is root dir"

@app.route('/admin/')
def hello_admin():
   return '''Hello Admin, how are you
   
<!doctype html>
<html>
  <head>
    <title>File Upload</title>
  </head>
  <body>
    <h1>File Upload</h1>
    <form method="POST" action="" enctype="multipart/form-data">
      <p><input type="file"   name="file"></p>
      <p><input type="submit" value="Submit"></p>
    </form>
  </body>
</html>'''

@app.route('/guest/<guest>/')
def hello_guest(guest):
   return f'Hello {guest} as Guest'

@app.route('/admin/', methods=["POST"])
def admin():
   uploaded_file = request.files['file']
   if uploaded_file.filename != '':
      uploaded_file.save(uploaded_file.filename)
   return redirect(url_for('hello_admin'))


@app.route('/user/<name>')
def hello_user(name):
   if name == 'Sk7':
      return redirect(url_for('hello_admin'))     #function name in url_for
   else:
      print("hi")
      return redirect(url_for('hello_guest', guest=name))


if __name__ == '__main__':
   app.config["MAX_CONTENT_LENGHT"] = 1024*1024
   app.run(host='127.0.0.1', port=2000)
