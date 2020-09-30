from app import app
from flask import render_template, flash, redirect, url_for, request, abort, g, make_response, jsonify
from werkzeug.urls import url_parse
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
# from app.email import *
# from app.bot import *
from flask_babel import _, Locale
from flask_babel import lazy_gettext as _l
from flask_babel import get_locale, force_locale
from urllib.parse import urlencode
import requests, json
import hashlib
import hmac
import base64
# import telegram

#
# # login with google account
# @app.route('/google/login')
# def google_login(start=None):
#     req = request.values.to_dict()
#     if 'start' in req:
#         session['before-redirect'] = req['start']
#     if is_logged_in():
#         return True
#     cur_session = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope=AUTHORIZATION_SCOPE,
#                                 redirect_uri=url_for('google_auth_redirect', _external=True))
#     uri, state = cur_session.create_authorization_url(AUTHORIZATION_URL)
#     session.permanent = True
#     return redirect(uri, code=302)
#
#
# @app.route('/google/auth')
# @no_cache
# def google_auth_redirect():
#     state = request.args.get('state', default=None, type=None)
#     cur_session = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope=AUTHORIZATION_SCOPE, state=state,
#                                 redirect_uri=url_for('google_auth_redirect', _external=True))
#     oauth2_tokens = cur_session.fetch_access_token(ACCESS_TOKEN_URI, authorization_response=request.url)
#     session[AUTH_TOKEN_KEY] = oauth2_tokens
#     user_info = get_user_info()
#     # enter user data into the session
#     if user_info:
#         if 'before-redirect' in session.keys():
#             resp = make_response(redirect(url_for(session['before-redirect'])))
#         else:
#             resp = make_response(redirect(url_for('index')))
#         expired_time = datetime.datetime.now() + datetime.timedelta(days=365)
#         resp.set_cookie('token', user_info, expires=expired_time)
#         addNotification('success', 'You were logged in', session)
#         return resp
#     else:
#         # if user is not in database - raise error
#         addNotification('danger', 'You have no access', session)
#     if 'before-redirect' in session.keys():
#         return redirect(url_for(session['before-redirect']))
#     return redirect(url_for('index'))
#
#
# def build_credentials():
#
#     oauth2_tokens = session[AUTH_TOKEN_KEY]
#     return google.oauth2.credentials.Credentials(
#         oauth2_tokens['access_token'],
#         refresh_token=oauth2_tokens['refresh_token'],
#         client_id=CLIENT_ID,
#         client_secret=CLIENT_SECRET,
#         token_uri=ACCESS_TOKEN_URI)
#
#
# # get email and check in database
# def get_user_info():
#     credentials = build_credentials()
#     oauth2_client = build('oauth2', 'v2', credentials=credentials)
#     data = oauth2_client.userinfo().get().execute()
#     session.pop(AUTH_TOKEN_KEY, None)
#     session.pop(AUTH_STATE_KEY, None)
#     if data['email'] in getUsers(data='email'):
#         return getUsers(data='token', email=data['email'])[0]
#     else:
#         return False


pages = {'/': 'About me', 'studies': 'Studies', 'projects': 'Projects', 'contact': 'Contact'}

# FIXME: replace by login required
# @app.before_request
# def before_request_callback():
#     is_logged_in()


@app.context_processor
def inject_vars():
    return dict(PAGES=pages)


@app.route('/')
def home():
    # notification = checkNotification(session)
    return render_template('about.html', current_function='about')
    # return render_template('index.html', current_function='index', current='', home=True)


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
    TITLES = ['mgr', 'inż.', 'prof. zw. dr hab. inż.', 'dr inż.', 'dr hab. inż.', 'mgr inż.', 'dr', 'prof. dr hab.', 'prof. dr hab. inż.']
    FACULTIES = ['FC','FA', 'FCEE', 'FMEM', 'FET', 'FET', 'FTP', 'FTE', 'FEM', 'FCT', 'CJiK']
    teachers = []
    subjects = []
    return render_template('studies.html', current_function='studies', current='studies', teachers=teachers, subjects=subjects, TITLES=TITLES, FACULTIES=FACULTIES)


@app.route('/projects')
def projects_page():
    return render_template('projects.html', current_function='projects')


@app.route('/projects/<int:project_id>')
def project_page(project_id):
    return render_template('project/index.html')


@app.route('/contact')
def contact_page():
    return render_template('contact.html', current_function='contact')


@app.route('/logout')
def logout_page(start=None):
    req = request.values.to_dict()
    # if g.is_logged_in:
    #     if 'start' in req:
    #         resp = make_response(redirect(url_for(req['start'])))
    #     else:
    #         resp = make_response(redirect(url_for('index')))
    #     resp.set_cookie('token', '', expires=0)
    #     session['notification'] = 'success'
    #     session['message'] = 'You were logged out'
    #     return resp
    # session['notification'] = 'danger'
    # session['message'] = 'Something went wrong'
    if 'start' in req:
        return redirect(url_for(req['start']))
    else:
        return redirect(url_for('index'))

#
# @app.route('/vogue', methods=['GET', 'POST'])
# def vogue():
#     is_logged_in()
#     result = []
#     if request.method == 'POST':
#         req = request.values.to_dict()
#         # print(req)
#         if 'get_schedule' in req:
#
#             if 'days_step' in req: day_step = int(req['days_step'])
#             else: day_step = 1
#             if req['sms'] == 'telegram': telegram_messages = True
#             else: telegram_messages = False
#             if 'schedule' not in req: not_schedule = True
#             else: not_schedule = False
#             change_status('working')
#             pr = Process(target=get_schedule, args=[day_step, telegram_messages, tommorow_notes, schedule, not_schedule])
#             pr.start()
#             return redirect(url_for('vogue'))
#         elif 'ru' in req.keys():
#             ru_text = req['ru']
#             pl_text = req['pl']
#             new1, new2 = backformating(ru_text), backformating(pl_text, 'pl')
#             if new1:
#                 open(os.path.join(dir_path, 'data', 'main_text_ru_backup'), 'w').write(open(os.path.join(dir_path, 'data', 'main_text_ru'), 'r').read())
#                 open(os.path.join(dir_path, 'data', 'main_text_ru'), 'w').write(new1)
#             if new2:
#                 open(os.path.join(dir_path, 'data', 'main_text_pl_backup'), 'w').write(open(os.path.join(dir_path, 'data', 'main_text_pl'), 'r').read())
#                 open(os.path.join(dir_path, 'data', 'main_text_pl'), 'w').write(new2)
#             if new1 and new2:
#                 result = [True, "Текст был обновлён"]
#             else:
#                 result = [False, 'Один или оба текстов не были обновлены. Возможно проблема с форматирование']
#         elif 'backup' in req:
#             open(os.path.join(dir_path, 'data', 'main_text_ru'), 'w').write(
#                 open(os.path.join(dir_path, 'data', 'main_text_ru_backup'), 'r').read())
#             open(os.path.join(dir_path, 'data', 'main_text_pl'), 'w').write(
#                 open(os.path.join(dir_path, 'data', 'main_text_pl_backup'), 'r').read())
#             result = [True, 'Прошлый текст возвращён']
#
#         elif 'start-reset' in req:
#             CONFIG['sp'] = 3
#             io.open(CONFIG_PATH, 'w', encoding='utf-8').write(str(CONFIG))
#             result = [True, 'Начало поиска даты сброшено до 3']
#
#         elif 'android' in req.keys():
#             redirect_sms_url = sendSMS(req)
#             return redirect(redirect_sms_url)
#         elif 'iphone' in req.keys():
#             redirect_sms_url = sendSMS(req)
#             return redirect(redirect_sms_url)
#         elif 'reset-sms' in req.keys():
#             tommorow_notes.clear()
#             # print(ru_text, pl_text)
#     updateConfig()
#     updateMessages()
#     data = eval(open(STATE_VOGUE_PATH, 'r').read())
#     status = data['status']
#     if datetime.datetime.strptime(CONFIG['current_schedule'], '%d.%m.%Y').date() < (datetime.datetime.today()).date() \
#             and status != 'working':
#         change_status('working')
#         pr = Process(target=get_schedule, args=[1, False, tommorow_notes, schedule, True])
#         pr.start()
#     vogue_state = eval(open(STATE_VOGUE_PATH, 'r').read())
#     status = vogue_state['status']
#     # status = 'error'
#     log = vogue_state['log'] if vogue_state['log']!="" else None
#     # log = 'Google API was updated. Please, edit your interaction with a module'
#     last_req_time = vogue_state['time'] if vogue_state['time']!="" else None
#     ru = open(os.path.join(dir_path, 'data', 'main_text_ru'), 'r').read()
#     ru_ls = ru.format('...Добрый день...', "...время визита...", "...хорошего дня...").splitlines()
#     pl = open(os.path.join(dir_path, 'data', 'main_text_pl'), 'r').read()
#     pl_ls = pl.format('...Dzień dobry...', "...czas wizyty...", "...miłęgo dnia...").splitlines()
#     max_layer = max([len(i) for i in schedule.values()]) if len(schedule) > 0 else 0
#     return render_template('vogue.html', status=status, log=log, last_req_time=last_req_time, ru=ru, pl=pl,
#                            result=result, ru_ls=ru_ls, pl_ls=pl_ls, tommorow_notes=messages, schedule=schedule, max_layer=max_layer)
#
#
# @app.route('/web-updates', methods=['GET', 'POST'])
# def web_updates():
#     if request.method == 'POST':
#         if 'bot_change':
#             bot_handle(True)
#             return redirect(url_for('web_updates'))
#     state = get_state_check_bot()
#     db = get_full_db()
#     bot_on = bot_handle()
#     return render_template('check_updates.html', state=state, db=db, bot_on=bot_on)
