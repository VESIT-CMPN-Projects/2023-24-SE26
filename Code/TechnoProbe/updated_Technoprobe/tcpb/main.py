import os
import json
import requests
from flask import *
from bson.objectid import ObjectId
from Backend.config import *
from flask import Flask, flash, redirect, render_template, request, url_for
from flask import session
from operator import itemgetter
from werkzeug.utils import secure_filename
import time

from Backend.config import recruiter_post_collection, qna_collection, profile_collection, \
    java_collection, machine_learning_collection, webdev_collection, python_collection, cybersecurity_collection, \
    community_collection, signup_collection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Frontend', 'templates')
app.template_folder = template_folder
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Frontend', 'static')
app.static_folder = static_folder
app.static_url_path = '/static'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/about-us")
def about():
    return render_template('about-us.html')


def update_database(data):
    with open('Backend/data/qna.json', 'w') as f:
        json.dump(data, f, indent=2)


@app.route("/qna", methods=['GET', 'POST'])
def qna():
    if 'username' in session:
        if request.method == 'POST':
            if 'title' in request.form:
                new_question = {
                    "id": qna_collection.count_documents({}) + 1,
                    "title": request.form.get('title'),
                    "content": request.form.get('question'),
                    "account": session['username'],
                    "replies": []
                }
                qna_collection.insert_one(new_question)

            if 'form-type' in request.form:
                question_id = int(request.form.get('question_id', -1))
                reply_content = request.form.get('replyContent')
                if question_id != -1:
                    question = qna_collection.find_one({'id': question_id})
                    if question:
                        qna_collection.update_one(
                            {'id': question_id},
                            {'$push': {'replies': {"content": reply_content, "reply_account": session['username']}}}
                        )
                        return redirect(url_for('qna'))
        data = list(qna_collection.find({}))
        for d in data:
            print(d)
        return render_template('qna.html', questions=data, author_name=session['username'])

    return redirect('signup')


# @app.route("/posts", methods=['GET', 'POST'])
# def posts():
#     with open('./Backend/data/jobs.json', encoding='utf-8') as f:
#         # data = json.load(f)
#
#
#
#     if 'username' in session:
#         personalised = []
#         # for i in data['jobs']:
#         #     if session['username'] == i['account']:
#         #         personalised.append(i)
#         if request.method == 'POST':
#
#             if 'title' in request.form:
#                 content = request.form.get('question')
#                 recruiter = session['username']  # Get the current user's username
#                 # Get the next job ID for the current user
#                 next_job_id = max((job['id'] for job in data['jobs'] if job['account'] == recruiter), default=0) + 1
#                 post = {
#                     "id": next_job_id,
#                     "title": request.form.get('title'),
#                     "content": content,
#                     "account": session['username'],
#                     "company_name": request.form.get('company_name'),
#                     "description": request.form.get('description'),
#                     "link": request.form.get('company_url'),
#                     "contact_number": request.form.get('contact_number'),
#                     "email": request.form.get('email'),
#                     "location": request.form.get('location'),
#                     "country": request.form.get('country'),
#                     "category": [item.strip() for item in content.split(',')],
#                     "recruiter": recruiter  # Associate the recruiter's username with the job posting
#                 }
#                 data['jobs'].append(post)
#                 # recruiter_post_collection.insert_one(post)
#
#                 # Save the updated data to the JSON file
#                 with open('./Backend/data/jobs.json', 'w', encoding='utf-8') as f:
#                     json.dump(data, f, indent=2)
#
#             if 'form-type' in request.form:
#                 question_id = int(request.form.get('question_id', -1))
#                 reply_content = request.form.get('replyContent')
#                 question = next((item for item in data['jobs'] if item["id"] == question_id), None)
#
#                 if question:
#                     question['replies'].append({"content": reply_content, "reply_account": session['username']})
#
#             if 'candidates' in request.form:
#                 print('cand')
#                 return render_template(url_for('dash'))
#
#             if 'delete' in request.form:
#                 print('delete')
#                 question_id = int(request.form['post_id'])
#                 print(int(question_id))
#                 # with open('./Backend/data/jobs.json', 'r', encoding='utf-8') as f:
#                 #     info = json.load(f)
#                 for i in data['jobs']:
#                     if i['id'] == int(question_id):
#                         data['jobs'].pop(data['jobs'].index(i))
#                         break
#                 # with open('./Backend/data/jobs.json', 'w', encoding='utf-8') as f:
#                 #     json.dump(info,f,indent=2)
#
#             with open('./Backend/data/jobs.json', 'w', encoding='utf-8') as f:
#                 json.dump(data, f, indent=2)
#             recruiter_post_collection.insert_one(post)
#             return redirect(url_for('posts'))
#
#         for i in data['jobs']:
#             try:
#                 if session['username'] == i['account']:
#                     personalised.append(i)
#             except:
#                 continue
#
#         return render_template('posts.html', questions=personalised, author_name=session.get('username'))
#     return redirect('signup')

# @app.route("/posts", methods=['GET', 'POST'])
# def posts():
#     # with open('./Backend/data/jobs.json', encoding='utf-8') as f:
#     #     data = json.load(f)
#     mongo_data = recruiter_post_collection
#     if 'username' in session:
#         personalised = []
#
#         if request.method == 'POST':
#
#             if 'title' in request.form:
#                 content = request.form.get('question')
#                 recruiter = session['username']  # Get the current user's username
#                 # Get the next job ID for the current user
#                 next_job_id = max((job['id'] for job in mongo_data if job['account'] == recruiter), default=0) + 1
#                 post = {
#                     "id": next_job_id,
#                     "title": request.form.get('title'),
#                     "content": content,
#                     "account": session['username'],
#                     "company_name": request.form.get('company_name'),
#                     "description": request.form.get('description'),
#                     "link": request.form.get('company_url'),
#                     "contact_number": request.form.get('contact_number'),
#                     "email": request.form.get('email'),
#                     "location": request.form.get('location'),
#                     "country": request.form.get('country'),
#                     "category": [item.strip() for item in content.split(',')],
#                     "recruiter": recruiter
#                 }
#                 # data['jobs'].append(post)
#                 recruiter_post_collection.insert_one(post)
#
#             if 'form-type' in request.form:
#                 question_id = int(request.form.get('question_id', -1))
#                 reply_content = request.form.get('replyContent')
#                 question = next((item for item in mongo_data if item["id"] == question_id), None)
#
#                 if question:
#                     question['replies'].append({"content": reply_content, "reply_account": session['username']})
#
#             if 'candidates' in request.form:
#                 print('cand')
#                 return render_template(url_for('dash'))
#
#             if 'delete' in request.form:
#                 print('delete')
#                 question_id = int(request.form['post_id'])
#                 print(int(question_id))
#
#                 mongo_data.delete_one({"id": int(question_id)})
#
#                 for i in mongo_data.find({}):
#                     if i['id'] == int(question_id):
#                         mongo_data.pop(mongo_data.index(i))
#                         break
#
#             # with open('./Backend/data/jobs.json', 'w', encoding='utf-8') as f:
#             #     json.dump(data, f, indent=2)
#             # recruiter_post_collection.insert_one(post)
#
#             # with open('./Backend/data/jobs.json', 'w', encoding='utf-8') as f:
#             #     json.dump(data, f, indent=2)
#             return redirect(url_for('posts'))
#
#         for i in mongo_data.find({}):
#             try:
#                 if session['username'] == i['account']:
#                     personalised.append(i)
#             except:
#                 continue
#
#         return render_template('posts.html', questions=personalised, author_name=session.get('username'))
#     return redirect('signup')

@app.route("/posts", methods=['GET', 'POST'])
def posts():
    mongo_data = recruiter_post_collection
    if 'username' in session:
        personalised = []

        if request.method == 'POST':

            if 'title' in request.form:
                content = request.form.get('question')
                recruiter = session['username']  # Get the current user's username
                # Get the next job ID for the current user
                next_job = mongo_data.find_one({"account": recruiter}, sort=[("id", -1)])
                next_job_id = next_job["id"] + 1 if next_job else 1
                post = {
                    "id": next_job_id,
                    "title": request.form.get('title'),
                    "content": content,
                    "account": session['username'],
                    "company_name": request.form.get('company_name'),
                    "description": request.form.get('description'),
                    "link": request.form.get('company_url'),
                    "contact_number": request.form.get('contact_number'),
                    "email": request.form.get('email'),
                    "location": request.form.get('location'),
                    "country": request.form.get('country'),
                    "category": [item.strip() for item in content.split(',')],
                    "recruiter": recruiter
                }
                recruiter_post_collection.insert_one(post)

            if 'form-type' in request.form:
                question_id = int(request.form.get('question_id', -1))
                reply_content = request.form.get('replyContent')
                question = next((item for item in mongo_data.find({}) if item["id"] == question_id), None)

                if question:
                    question['replies'].append({"content": reply_content, "reply_account": session['username']})

            if 'candidates' in request.form:
                print('cand')
                return render_template(url_for('dash'))

            if 'delete' in request.form:
                print('delete')
                question_id = int(request.form['post_id'])
                print(int(question_id))

                mongo_data.delete_one({"id": int(question_id)})

            return redirect(url_for('posts'))

        for i in mongo_data.find({}):
            try:
                if session['username'] == i['account']:
                    personalised.append(i)
            except:
                continue

        return render_template('posts.html', questions=personalised, author_name=session.get('username'))
    return redirect('signup')



@app.route("/internship", methods=['GET', 'POST'])
def internship():
    data = list(recruiter_post_collection.find({}))
    # print(data)
    if request.method == 'POST':
        if 'search' in request.form:
            target = request.form.get('search').lower()
            jobloc = [d for d in data if target in d['location'].lower()]
            return render_template('internship.html', jobs=jobloc)

        if 'skills' in request.form or 'interests' in request.form:
            jobskill = []
            skill = request.form.get('skills')
            interest = request.form.get('interests')

            for d in data:
                if skill and skill.lower() in d['category']:
                    jobskill.append(d)

                if interest and interest.lower() in d['title'].lower():
                    jobskill.append(d)

            return render_template('internship.html', jobs=jobskill)

    return render_template('internship.html', jobs=data)


# @app.route('/find-candidates', methods=['GET', 'POST'])
# def dash():
#     if request.method == 'POST':
#         post_id = request.form.get('post_id')
#         required_skills, matching_profiles = set(), []
#
#         data = list(recruiter_post_collection.find({}))
#         required_skills = {skill.strip().lower() for skill in data[int(post_id) - 1]['content'].split(',')}
#
#         # Iterate over student profiles
#         student_data = list(profile_collection.find({}))
#         for student_profile in student_data:
#             student_skills = set(student_profile['skill_list'])
#
#             # Calculate the percentage of matching skills
#             common_skills = student_skills.intersection(required_skills)
#             matching_percentage = (len(common_skills) / len(required_skills)) * 100
#
#             # If the matching percentage meets the threshold, add the profile to the list of matching profiles
#             if matching_percentage >= 10:
#                 matching_profiles.append((student_profile, matching_percentage))
#                 # matching_profiles.append({"profile": student_profile, "matching_percentage": matching_percentage})
#
#         # If no matching profiles found, display a message
#         if not matching_profiles:
#             # flash('No candidates matched')
#             return render_template('home.html', name=session.get('username'))
#
#         # Sort the matching profiles based on matching percentage
#         sorted_profiles = sorted(matching_profiles, key=lambda x: x[1], reverse=True)
#
#         # Extract only the profiles from the sorted list
#         sorted_profiles = [profile[0] for profile in sorted_profiles]
#
#         # # Sort the matching profiles based on matching percentage (in descending order)
#         # matching_profiles = sorted(matching_profiles, key=itemgetter('matching_percentage'), reverse=True)
#         #
#         # # Extract the sorted candidate profiles
#         # sorted_profiles = [profile["profile"] for profile in matching_profiles]
#
#         # Display the sorted matching profiles
#         return render_template('base.html', post=sorted_profiles)
#
#     # If the request method is not POST, render the recruiter dashboard
#     return render_template('rec_dashboard.html', name=session.get('username'))
# @app.route('/find-candidates', methods=['GET', 'POST'])
# def dash():
#     if request.method == 'POST':
#         post_id = request.form.get('post_id')
#         required_skills, matching_profiles = set(), []
#
#         data = recruiter_post_collection.find({})
#         required_skills = {skill.strip().lower() for skill in data[int(post_id) - 1]['content'].split(',')}
#         print(required_skills)
#         student_data = profile_collection.find({})
#         for student_profile in student_data:
#             student_skills = set(skill.lower() for skill in student_profile['skill_list'])
#             # student_skills = set(student_profile['skill_list'])
#             print(student_skills)
#             common_skills = student_skills.intersection(required_skills)
#             print(common_skills)
#             matching_percentage = (len(common_skills) / len(required_skills)) * 100
#
#             if matching_percentage >= 10:
#                 matching_profiles.append((student_profile, matching_percentage))
#                 # print(student_profile)
#
#         if not matching_profiles:
#             # flash('No candidates matched')
#             return render_template('home.html', name=session.get('username'))
#
#         sorted_profiles = sorted(matching_profiles, key=lambda x: x[1], reverse=True)
#
#         sorted_profiles = [profile[0] for profile in sorted_profiles]
#         return render_template('base.html', post=sorted_profiles)
#
#     return render_template('rec_dashboard.html', name=session.get('username'))

@app.route('/find-candidates', methods=['GET', 'POST'])
def dash():
    if request.method == 'POST':
        post_id = request.form.get('post_id')
        required_skills, matching_profiles = set(), []

        # Retrieve the required skills for the job posting
        job_data = recruiter_post_collection.find_one({"id": int(post_id), "account": session.get('username')})
        if job_data:
            required_skills = set(skill.strip().lower() for skill in job_data['content'].split(','))

            # Retrieve candidate profiles
            candidate_data = profile_collection.find({})
            for candidate_profile in candidate_data:
                candidate_skills = set(skill.strip().lower() for skill in candidate_profile['skill_list'])

                # Calculate matching percentage and common skills
                common_skills = candidate_skills.intersection(required_skills)
                matching_percentage = (len(common_skills) / len(required_skills)) * 100

                # Print matching percentage and common skills
                print(f"Candidate: {candidate_profile['name']}")
                print(f"Matching Percentage: {matching_percentage}%")
                print("Matching Skills:", ', '.join(common_skills))

                # If matching percentage meets the threshold, add the candidate to the list
                if matching_percentage >= 10:
                    matching_profiles.append((candidate_profile, matching_percentage))

            # If no matching candidates found, display a message
            if not matching_profiles:
                # flash('No candidates matched')
                return render_template('home.html', name=session.get('username'))

            # Sort the matching profiles based on matching percentage
            sorted_profiles = sorted(matching_profiles, key=lambda x: x[1], reverse=True)

            # Extract only the candidate profiles from the sorted list
            sorted_profiles = [profile[0] for profile in sorted_profiles]

            return render_template('base.html', post=sorted_profiles)

    # If the request method is not POST or if there was an error, render the recruiter dashboard
    return render_template('rec_dashboard.html', name=session.get('username'))





@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if session:
        if request.method == 'POST':
            profile_data = {
                'name': request.form.get('Name'),
                'email': request.form.get('email'),
                'contact': request.form.get('contact'),
                'headline': request.form.get('headline'),
                'location': request.form.get('location'),
                'industry': request.form.get('industry'),
                'skills': request.form.get('skills'),
                'skill_list': [skill.strip() for skill in request.form.get('skills').split(',')],
                'experience': request.form.get('experience'),
                'education': request.form.get('education'),
                'account': session['username']
            }
            profile_collection.insert_one(profile_data)
            return render_template('final-prof.html', profile_data=profile_data)
        all_coll = profile_collection.find({})
        for i in all_coll:
            if i['account'] == session['username']:
                return render_template('final-prof.html', profile_data=i)
        return render_template('profile.html')
    return redirect(url_for('signup'))


@app.route('/java', methods=['GET', 'POST'])
def java():
    if 'username' in session:
        if request.method == 'POST':
            if 'title' in request.form:
                new_question = {
                    "id": java_collection.count_documents({}) + 1,
                    "title": request.form.get('title'),
                    "content": request.form.get('question'),
                    "account": session['username'],
                    "replies": []
                }
                java_collection.insert_one(new_question)
            if 'form-type' in request.form:
                question_id = int(request.form.get('question_id', -1))
                reply_content = request.form.get('replyContent')
                question = java_collection.find_one({'id': question_id})

                if question:
                    java_collection.update_one(
                        {'id': question_id},
                        {'$push': {'replies': {"content": reply_content, "reply_account": session['username']}}}
                    )
            return redirect(url_for('java'))
        author_name = session.get('username')
        data = list(java_collection.find({}))
        return render_template('java.html', questions=data, author_name=author_name)
    return redirect('signup')


@app.route('/machine-learning', methods=['GET', 'POST'])
def machine_learning():
    if 'username' in session:

        if request.method == 'POST':
            if 'title' in request.form:
                new_question = {
                    "id": machine_learning_collection.count_documents({}) + 1,
                    "title": request.form.get('title'),
                    "content": request.form.get('question'),
                    "account": session['username'],
                    "replies": []
                }
                machine_learning_collection.insert_one(new_question)
            if 'form-type' in request.form:
                question_id = int(request.form.get('question_id', -1))
                reply_content = request.form.get('replyContent')
                question = machine_learning_collection.find_one({'id': question_id})

                if question:
                    machine_learning_collection.update_one(
                        {'id': question_id},
                        {'$push': {'replies': {"content": reply_content, "reply_account": session['username']}}}
                    )
            return redirect(url_for('machine_learning'))
        author_name = session.get('username')
        data = list(machine_learning_collection.find({}))
        return render_template('ml.html', questions=data, author_name=author_name)
    return redirect('signup')


@app.route('/webdev', methods=['GET', 'POST'])
def webdev():
    if 'username' in session:
        if request.method == 'POST':

            if 'title' in request.form:
                new_question = {
                    "id": webdev_collection.count_documents({}) + 1,
                    "title": request.form.get('title'),
                    "content": request.form.get('question'),
                    "account": session['username'],
                    "replies": []
                }
                webdev_collection.insert_one(new_question)

            if 'form-type' in request.form:
                question_id = int(request.form.get('question_id', -1))
                reply_content = request.form.get('replyContent')
                question = webdev_collection.find_one({'id': question_id})

                if question:
                    webdev_collection.update_one(
                        {'id': question_id},
                        {'$push': {'replies': {"content": reply_content, "reply_account": session['username']}}}
                    )
            return redirect(url_for('webdev'))
        author_name = session.get('username')
        data = list(webdev_collection.find({}))
        return render_template('webdev.html', questions=data, author_name=author_name)
    return redirect('signup')


@app.route('/python', methods=['GET', 'POST'])
def python():
    if 'username' in session:
        if request.method == 'POST':
            if 'title' in request.form:
                new_question = {
                    "id": python_collection.count_documents({}) + 1,
                    "title": request.form.get('title'),
                    "content": request.form.get('question'),
                    "account": session['username'],
                    "replies": []
                }
                python_collection.insert_one(new_question)
            if 'form-type' in request.form:
                question_id = int(request.form.get('question_id', -1))
                reply_content = request.form.get('replyContent')
                question = python_collection.find_one({'id': question_id})
                if question:
                    python_collection.update_one(
                        {'id': question_id},
                        {'$push': {'replies': {"content": reply_content, "reply_account": session['username']}}}
                    )
            return redirect(url_for('python'))
        author_name = session.get('username')
        data = list(python_collection.find({}))
        for i in data:
            print(i)
        return render_template('python.html', questions=data, author_name=author_name)
    return redirect('signup')


@app.route('/cybersecurity', methods=['GET', 'POST'])
def cybersecurity():
    if 'username' in session:
        # with open('data/cybersecurity.json') as f:
        #     data = json.load(f)
        data = cybersecurity_collection.find({})

        if request.method == 'POST':

            if 'title' in request.form:
                new_question = {
                    "id": cybersecurity_collection.count_documents({}) + 1,
                    "title": request.form.get('title'),
                    "content": request.form.get('question'),
                    "account": session['username'],
                    "replies": []
                }
                cybersecurity_collection.insert_one(new_question)

            if 'form-type' in request.form:
                question_id = int(request.form.get('question_id', -1))
                reply_content = request.form.get('replyContent')
                question = cybersecurity_collection.find_one({'id': question_id})

                if question:
                    cybersecurity_collection.update_one(
                        {'id': question_id},
                        {'$push': {'replies': {"content": reply_content, "reply_account": session['username']}}}
                    )

            # with open('data/cybersecurity.json', 'w') as f:
            #     json.dump(data, f, indent=2)
            # cybersecurity_collection.insert_one(data)
            # cybersecurity_collection.insert_one(new_question)

            return redirect(url_for('cybersecurity'))
        author_name = session.get('username')

        return render_template('cybersecurity.html', questions=data, author_name=author_name)
    return redirect('signup')


@app.route("/community", methods=['GET', 'POST'])
def community():
    if session:
        if request.method == 'POST':
            if 'join-java' in request.form:
                data = community_collection.find({})
                if community_collection.count_documents({}) != 0:
                    for d in data:
                        if d['username'] == session['username']:
                            d['joined'].append('java')
                            break
                community_collection.insert_one({'username': session['username'], 'joined': ['java']})
                flash('Joined the Java community')
                return redirect('java')

            elif 'join-webdev' in request.form:
                data = community_collection.find({})
                if community_collection.count_documents({}) != 0:
                    for d in data:
                        if d['username'] == session['username']:
                            d['joined'].append('webdev')
                            break
                else:
                    community_collection.insert_one({'username': session['username'], 'joined': ['webdev']})
                flash('Joined the Web development community')
                return redirect('webdev')

            elif 'join-python' in request.form:
                data = community_collection.find({})
                if community_collection.count_documents({}) != 0:
                    for d in data:
                        if d['username'] == session['username']:
                            d['joined'].append('python')
                            break
                else:
                    community_collection.insert_one({'username': session['username'], 'joined': ['python']})
                flash('Joined the Python community')
                return redirect('python')

            elif 'join-machine-learning' in request.form:
                data = community_collection.find({})
                if community_collection.count_documents({}) != 0:
                    for d in data:
                        if d['username'] == session['username']:
                            d['joined'].append('machine learning')
                            break
                else:
                    community_collection.insert_one({'username': session['username'], 'joined': ['machine learning']})
                flash('Joined the Machine learning community')
                return redirect('machine_learning')

            elif 'join-cybersecurity' in request.form:
                data = community_collection.find({})
                if community_collection.count_documents({}) != 0:
                    for d in data:
                        if d['username'] == session['username']:
                            d['joined'].append('cybersecurity')
                            break
                else:
                    community_collection.insert_one({'username': session['username'], 'joined': ['cybersecurity']})
                flash('Joined the Cybersecurity community')
                return redirect('cybersecurity')

        return render_template('community.html')
    return redirect(url_for('signup'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'sign-up-form' in request.form:
            # Sign-up logic
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            account_type = request.form.get('type')
            existing_user = signup_collection.find_one({'username': username})
            if existing_user:
                flash('Username already exists. Please choose a different one.', 'error')
                return redirect(url_for('login'))
            if not (username and email and password):
                flash('Please fill out all fields', 'error')
                return redirect(url_for('login'))
            signup_collection.insert_one(
                {'username': username, 'email': email, 'password': password, 'type': account_type})
            flash('Account created successfully!', 'success')
            time.sleep(3)
            return redirect(url_for('login'))
        else:
            username = request.form.get("username")
            password = request.form.get("password")
            account_type = request.form.get('types')
            data = signup_collection.find({})
            user_exists = False
            for index, user in enumerate(data):
                if user['username'] == username:
                    user_exists = True
                    if user['password'] == password:
                        session['user_id'] = index
                        session['username'] = user['username']
                        session['types'] = user['type']
                        flash('Login successful!', 'success')
                        time.sleep(3)
                        if account_type == 'recruiter':
                            return redirect(url_for('dash', name=session['username']))
                        return redirect(url_for('index', name=username))
                    else:
                        flash('Login unsuccessful. Please check your Password.', 'danger')
                        return redirect(url_for('login'))
            if not user_exists:
                flash('Username does not exist. Please sign up.', 'error')
                return redirect(url_for('signup'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        account_type = request.form.get('type')
        existing_user = signup_collection.find_one({'username': username})
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('signup'))
        if not (username and email and password):
            flash('Please fill out all fields', 'error')
            return redirect(url_for('signup'))
        signup_collection.insert_one({'username': username, 'email': email, 'password': password, 'type': account_type})
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    elif 'sign-in-form' in request.form:
        # Sign-in logic
        username = request.form.get("username")
        password = request.form.get("password")
        account_type = request.form.get('types')
        data = signup_collection.find({})
        for index, user in enumerate(data):
            if user['username'] == username and user['password'] == password:
                if user['types'] == account_type:  # Check if account type matches the requested dashboard
                    session['user_id'] = index
                    session['username'] = user['username']
                    session['types'] = user['type']
                    flash('Login successful!', 'success')
                    if account_type == 'recruiter':
                        return redirect(url_for('dash', name=session['username']))
                    return redirect(url_for('index', name=username))
                else:
                    flash('You do not have access to this dashboard.', 'danger')
                    return redirect(url_for('signup'))
        flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('signup.html')


# Route for login page
@app.route('/login')
def login_redirect():
    return render_template('login.html')


@app.route('/signup')
def signup_redirect():
    return render_template('signup.html')


# Route for handling redirection from login to signup
@app.route('/redirect_to_signup')
def redirect_to_signup():
    return redirect(url_for('signup'))


# Route for handling redirection from signup to login
@app.route('/redirect_to_login')
def redirect_to_login():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
