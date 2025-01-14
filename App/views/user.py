from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from.index import index_views

from App.controllers import (
    create_user,
    create_admin,
    get_user,
    check_competitions,
    jwt_authenticate, 
    get_all_users,
    get_all_users_json,
    jwt_required
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_user(data['username'], data['password'])
    return jsonify({'message': f"user {data['username']} created"})

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')

@user_views.route('/normal', methods=['POST'])
def create_normal_user_action():
    data = request.json
    result = create_user(username=data['username'], password=data['password'], email=data['email'])
    if result:
        return jsonify({"message": f"User created with id {result.id}"}), 201
    return jsonify({"error": f"Username {data['username']} already exists "}), 500

@user_views.route('/admin', methods=['POST'])
def create_admin_user_action():
    data = request.json
    result = create_admin(username=data['username'], password=data['password'], email=data['email'])
    if result:
        return jsonify({"message": f"Admin created with id {result.id}"}), 201
    return jsonify({"error": f"Admin Username {data['username']} already exists "}), 500

@user_views.route('/myprofile', methods=['GET'])
@jwt_required()
def view_profile_action():
    user = get_user(jwt_current_user.id)
    competitions = check_competitions(user.id)
    return jsonify(user.get_json(), competitions)