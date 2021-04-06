from flask import *
import os, random, json
app = Flask(__name__)

with open("codes.json") as f:
  data = json.load(f) 

@app.route('/')###
def index():
    return render_template('index.html')

@app.route('/new-link', methods=['POST', 'GET'])###
def new_link():
  global data
  link = request.form['link']
  if not link.startswith("http"):
    return render_template("index.html", stat="A URL Should Start With http or https!")
  else:
    with open('codes.json', 'r') as r:
      read = r.read()
      while True:
        code = str(random.randint(1000, 9999))
        if code in read:
          pass
        else:
          os.system(f"echo Ip:  > clients/{code}")
          data[code] = link
          with open('codes.json', 'w+') as fp:
            # f.write(code + "\n")
            json.dump(data, fp, sort_keys=True, indent=int(4))
            stat = f"Created Your Code Is: {code}, Send this link to the victim: http://127.0.0.1:8000/link/{code}"
            break
    return render_template("index.html", good=stat)

@app.route('/a/add-one', methods=['POST', 'GET'])###
def add_one_to_link():
  global data
  code = request.form['code']
  ip = request.form['ip']
  with open(f"clients/{code}", 'r') as read:
    read = read.read()
    if ip in read:
      pass
    else:
      with open(f"clients/{code}", 'a') as f:
        f.write(f"Ip: {ip}\n")
    return redirect(data[code])

@app.route("/link/<code>")###
def goto(code):
  with open("codes.json", "r") as f:
    if code in f.read():
      return render_template("model.html", code=code)
    return f"'{code}' Not Found!"

@app.route("/statics", methods=['POST', 'GET'])
def statics():
  code = request.form['code']
  try:
    with open(f"clients/{code}", 'r') as f:
      read = f.read()
    return render_template("statics.html", read=read, code=code)
  except:
    return render_template("index.html", stat="Code Not Found!")



app.run(port=8000, debug=True)