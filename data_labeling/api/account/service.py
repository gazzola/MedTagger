"""Module responsible for defining endpoints for user management"""
from typing import Any

from flask import request
from flask_login import login_required
from flask_restplus import Resource

from data_labeling.api import api
from data_labeling.api.account import serializers
from data_labeling.api.account.business import create_user, sign_in_user, sign_out_user, get_current_user_info

account_ns = api.namespace('account', 'User account management')


@account_ns.route('/register')
class Register(Resource):
    """Register user endpoint"""

    @staticmethod
    @api.expect(serializers.new_user)
    @api.doc(responses={201: 'User created', 400: 'Invalid arguments'})
    def post() -> Any:
        """Register the user"""
        user = request.json
        user_id = create_user(user['email'], user['password'], user['firstName'], user['lastName'])
        return {'id': user_id}, 201


@account_ns.route('/sign-in')
class SignIn(Resource):
    """Sign in endpoint"""

    @staticmethod
    @api.expect(serializers.sign_in)
    @api.doc(responses={204: 'Signed in', 400: 'User does not exist or wrong password'})
    def post() -> Any:
        """Sign in the user"""
        sign_in = request.json
        sign_in_user(sign_in['email'], sign_in['password'])
        return {}, 204


@account_ns.route('/sign-out')
class SignOut(Resource):
    """Sign out endpoint"""

    @staticmethod
    @login_required
    @api.doc(responses={204: 'Signed out'})
    def post() -> Any:
        """Sign out the user"""
        sign_out_user()
        return {}, 204


@account_ns.route('/get-user-info')
class GetUserInfo(Resource):
    """Get user info endpoint"""

    @staticmethod
    @login_required
    @api.marshal_with(serializers.user_info)
    @api.doc(responses={200: 'Successfully retrieved data.'})
    def get() -> Any:
        """Get user info"""
        user_info = get_current_user_info()
        return user_info._asdict(), 200