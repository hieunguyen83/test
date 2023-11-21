from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os


app = Flask(__name__)
app.secret_key = 'ffdddddd34lkdf0882sxxc'

@app.route("/")
def home():
    return render_template("home.html")


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
        
        urls[request.form['code']] = {'url':request.form['url']}
        with open('urls.json','w') as f:
            json.dump(urls, f)
        return render_template('your_url.html', code=request.form['code'], url=request.form['url'])
    else:
        return redirect(url_for('home'))
