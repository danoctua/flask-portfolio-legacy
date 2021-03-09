import os

from app import app, media_version, google_client
from flask import render_template, flash, redirect, url_for, request, jsonify, abort
from werkzeug.urls import url_parse
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
# from app.email import *
# from app.bot import *
from flask_babel import _
import requests, json
import hashlib
import hmac
import base64

# import telegram


def get_google_provider_cfg():
    return requests.get(app.config["GOOGLE_DISCOVERY_URL"]).json()


@app.route("/login")
def login_page():
    if current_user.is_authenticated:
        flash("You already has been authenticated")
        return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/login-google")
def login_google_midpoint():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = google_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url.replace("http://", 'https://') + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login-google/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = google_client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url.replace("http://", "https://", 1) if request.url.startswith(
            "http://") else request.url,
        redirect_url=request.base_url.replace("http://", "https://", 1) if request.base_url.startswith(
            "http://") else request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(app.config["GOOGLE_CLIENT_ID"], app.config["GOOGLE_CLIENT_SECRET"]),
    )
    # Parse the tokens!
    google_client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = google_client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        # unique_id.data = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        # picture = userinfo_response.json()["picture"]
        # users_name = userinfo_response.json()["given_name"]
    else:
        flash(_('User email not available or not verified by Google'), "error")
        return redirect(url_for('login'))
    user = User.query.filter_by(email=users_email).first()
    if not user:
        flash(_('Invalid email. You should log in to existing account'), "error")
        return redirect(url_for('home'))
    # if not user.approved:
    #     flash(_("User has not been approved yet"), "error")
    #     return redirect(url_for('home'))
    login_user(user, remember=True)
    flash(f"You has been logged in as {user.name}", "success")
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for("home")
    return redirect(next_page)


pages = {'/': 'About me', 'studies': 'Studies', 'projects': 'Projects', 'contact': 'Contact'}


# FIXME: replace by login required
# @app.before_request
# def before_request_callback():
#     is_logged_in()


@app.context_processor
def inject_vars():
    return dict(PAGES=pages, media_version=media_version)


@app.route('/')
def home():
    return render_template('about.html', current_function='about')


@app.route('/init', methods=["POST", "GET"])
def init_page():
    form = UserForm()
    if form.validate_on_submit():
        success, message = add_user(form)
        if success:
            flash(message, "success")
            return redirect(url_for("home"))
        else:
            flash(message, "danger")
            return redirect(url_for("init_page"))
    return render_template("init.html", form=form)


@app.route('/studies', methods=['POST', 'GET'])
def studies_page():
    # if request.method == 'POST':
    #     if not is_logged_in():
    #         addNotification('danger', 'You have no access', session)
    #     else:
    #         req = request.values.to_dict()
    #         if 'new-subject' in req.keys():
    #             addSubject(name=req['name'], short_name=req['short'],
    #                        exam=req['exam'], teacher=req['new-subject-teacher-id'], app_session=session)
    #         elif 'edit-subject' in req.keys():
    #             editSubject(subject_id=req['edit-subject'], name=req['name'], short_name=req['short'], exam=req['exam'],
    #                         teacher=req['edit-subject-teacher-id'], app_session=session)
    #         elif 'remove-subject' in req.keys():
    #             removeSubject(req['remove-subject'], app_session=session)
    #         elif 'new-teacher' in req.keys():
    #             addTeacher(name=req['name'], surname=req['surname'], title=req['title'], email=req['email'],
    #                        faculty_info=req['faculty_info'], webpage=req['webpage'], consultations=req['consultations'],
    #                        room=req['room'], app_session=session)
    #         elif 'remove-teacher' in req.keys():
    #             removeTeacher(req['remove-teacher'], app_session=session)
    # notification = checkNotification(session)
    TITLES = ['mgr', 'inż.', 'prof. zw. dr hab. inż.', 'dr inż.', 'dr hab. inż.', 'mgr inż.', 'dr', 'prof. dr hab.',
              'prof. dr hab. inż.']
    FACULTIES = ['FC', 'FA', 'FCEE', 'FMEM', 'FET', 'FET', 'FTP', 'FTE', 'FEM', 'FCT', 'CJiK']
    teachers = []
    subjects = []
    return render_template('studies.html', current_function='studies', current='studies', teachers=teachers,
                           subjects=subjects, TITLES=TITLES, FACULTIES=FACULTIES)


@app.route('/projects')
def projects_page():
    projects_private, projects_work, projects_study = get_projects(current_user.is_authenticated)
    return render_template('projects.html', projects_private=projects_private, projects_work=projects_work,
                           projects_study=projects_study)


@app.route('/projects/<category>/add', methods=["GET", "POST"])
@login_required
def add_project_page(category):
    form = NewProjectForm()
    # flash("Some message, longer then you might expect", "success")
    if form.validate_on_submit():
        success, message = add_project(
            category=category,
            form=form
        )
        if success:
            flash(message, "success")
            return redirect(url_for("projects_page"))
        else:
            flash(message, "danger")
            return redirect(url_for("add_project_page", category=category))
    return render_template("project/add.html", category=category, form=form)


@app.route('/projects/<int:project_id>')
def project_page(project_id):
    project = Project.query.filter(Project.project_id == project_id).first_or_404()
    return render_template('project/index.html', project=project)


@app.route('/projects/<int:project_id>/edit', methods=["GET", "POST"])
@login_required
def edit_project_page(project_id):
    project = Project.query.filter(Project.project_id == project_id).first_or_404()
    form = NewProjectForm()
    form.submit.label.text = "Update"
    if form.validate_on_submit():
        success, message = modify_project(
            project_id=project_id,
            form=form
        )
        if success:
            flash(message, "success")
            return redirect(url_for("project_page", project_id=project_id))
        else:
            flash(message, "danger")
            return redirect(url_for("edit_project_page", project_id=project_id))
    else:
        form.title.data = project.title or ""
        form.background_image.data = project.background_url or ""
        form.github_url.data = project.github_url or ""
        form.website_url.data = project.website_url or ""
        form.description.data = project.description or ""
    return render_template('project/edit.html', project=project, form=form)


@app.route('/projects/<int:project_id>/update', methods=["POST"])
@login_required
def update_project_api_page(project_id):
    req = request.values.to_dict()
    result = update_project_settings(project_id=project_id, req=req)
    return jsonify(result)


@app.route('/projects/<int:project_id>/remove', methods=["POST"])
@login_required
def remove_project_page(project_id):
    success, message = remove_project(project_id)
    if success:
        flash(message, "success")
        return redirect(url_for("projects_page"))
    else:
        flash(message, "danger")
        return redirect(url_for("edit_project_page", project_id=project_id))


@app.route('/contact', methods=["GET", "POST"])
def contact_page():
    form = ContactForm()
    if form.validate_on_submit():
        flash("Oops... Not working yet", "danger")
        return redirect(url_for("contact_page"))
    return render_template('contact.html', form=form)


@app.route('/wedding', methods=['GET'])
def wedding_page():
    name = request.values.get("name")
    wedding_data = Wedding()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    wedding_file_location = os.path.join(dir_path, os.getenv("WEDDING_SETUP_PATH"))
    wedding_data.load(wedding_file_location)
    wedding_data.parse_to_json()
    if not name or not any(x.people == name for x in wedding_data.invitees):
        abort(404)
    return render_template('wedding.html', name=name, wedding_data=wedding_data, datetime=datetime)


@app.route('/wedding-setup', methods=['GET', 'POST'])
# @login_required
def wedding_setup_page():
    wedding_data = Wedding()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    wedding_file_location = os.path.join(dir_path, os.getenv("WEDDING_SETUP_PATH"))
    wedding_data.load(wedding_file_location)
    wedding_data.parse_to_json()
    form = WeddingSetupForm(data=wedding_data.output)

    if form.validate_on_submit():
        success = wedding_data.update(wedding_file_location, form)
        if success:
            flash("Wedding data has been updated", "success")
        else:
            flash("Oops. Something went wrong", "danger")
        return redirect(url_for("wedding_setup_page"))
    else:
        print(form.errors)
    return render_template('wedding-setup.html', form=form, wedding_data=wedding_data)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("You has been logged out", "success")
    return redirect(url_for('home'))
