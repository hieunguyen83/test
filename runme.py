from flask import abort, Flask, flash, jsonify, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import json
import os


app = Flask(__name__)
app.secret_key = 'ffdddddd34lkdf0882sxxc'

@app.route("/")
def home():
    return render_template("home.html", codes=session.keys())


@app.route("/about")
def about():
    pass


@app.route("/your_url", methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as f:
                urls = json.load(f)
        if request.form['code'] in urls.keys():
            flash('Code is existed!')
            return redirect(url_for('home'))
        
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('C:\\Users\\Gia Hieu\\Desktop\\hocflask\\static\\user_files\\'+full_name)
            urls[request.form['code']] = {'file':full_name}

        with open('urls.json','w') as f:
            session[request.form['code']] = True
            json.dump(urls, f)
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))

@app.route("/<string:code>")
def your_code(code):
    urls = {}
    if os.path.exists('urls.json'):
            with open('urls.json') as f:
                urls = json.load(f)
                if code in urls.keys():
                    if 'url' in urls[code].keys():
                        return redirect(urls[code]['url'])
                    else:
                        return redirect(url_for('static', filename='user_files/'+urls[code]['file']))


    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"),404


@app.route("/api")
def api():
    return jsonify(list(session.keys()))