from app import db
from flask import jsonify, make_response, abort
from werkzeug.exceptions import HTTPException

class API():

	def response(data, status=200):
		json_dict = {
				'data': data
		}

		if(isinstance(data, list)):
			json_dict['total'] = len(data)

		return make_response(jsonify(json_dict), status)

	def abort(status, message=""):
		abort(status)

	def success():
		return make_response({'status':'success'})

	def error(e):
		code = 500
		
		if isinstance(e, HTTPException):
			code = e.code

		return make_response(jsonify(
			error=str(e)
		), code)

	def update_obj(obj,data):
		for key, value in data.items():
			setattr(obj, key, value)

		return obj

	def save_changes(obj):
		try:
			db.session.add(obj)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			API.abort(500, "DB Integrity Error")

	def delete(obj):
		try:
			db.session.delete(obj)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			API.abort(500, "DB Integrity Error")