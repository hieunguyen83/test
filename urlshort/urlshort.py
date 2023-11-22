from flask import abort, Blueprint, flash, jsonify, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import json
import os


bp = Blueprint('urlshort',__name__)

@bp.route("/")
def home():
    return render_template("home.html", codes=session.keys())


@bp.route("/about")
def about():
    pass


@bp.route("/your_url", methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as f:
                urls = json.load(f)
        if request.form['code'] in urls.keys():
            flash('Code is existed!')
            return redirect(url_for('urlshort.home'))
        
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('C:\\Users\\Gia Hieu\\Desktop\\hocflask\\urlshort\\static\\user_files\\'+full_name)
            urls[request.form['code']] = {'file':full_name}

        with open('urls.json','w') as f:
            session[request.form['code']] = True
            json.dump(urls, f)
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home'))

@bp.route("/<string:code>")
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

@bp.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"),404


@bp.route("/api")
def api():
    return jsonify(list(session.keys()))