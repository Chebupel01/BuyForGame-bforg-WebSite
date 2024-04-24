from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('nickname', required=True)
parser.add_argument('email', required=True)
parser.add_argument('hashed_password', required=True)
