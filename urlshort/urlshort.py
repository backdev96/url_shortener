import json
import os.path

from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
from werkzeug.utils import secure_filename

bp = Blueprint('urlshort',__name__)


@bp.route('/')
def home():
    return render_template('home.html', codes=session.keys())


@bp.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == "POST":
        urls = dict()
        # Check if json file already exists.
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('This short name has already been taken. Please, select another name!')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            file = request.files['file']
            full_name = request.form['code'] + secure_filename(file.filename)
            file.save('/Users/stasefremov/Dev/first_flask_project/static/user_files/' + full_name)
            urls[request.form['code']] = {'file': full_name}

        with open('urls.json', 'w') as urls_file:
            json.dump(urls, urls_file)
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home'))


@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='/user_files/' + urls[code]['file']))

    # Exception
    return abort(404)


@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
