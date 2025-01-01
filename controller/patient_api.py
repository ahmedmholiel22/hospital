import json
from urllib.parse import parse_qs
from logging import exception
from odoo import http
from odoo.http import request
import math


def valid_response(data, status, pagination_info):
    response_body = {
        'message': 'successful',
        'data': data,
    }
    if pagination_info:
        response_body['pagination_info'] = pagination_info
    return request.make_json_response(response_body, status=status)


def invalid_response(error, status):
    response_body = {
        'error': error,
    }
    return request.make_json_response(response_body, status=status)


class PatientApi(http.Controller):

    @http.route("/v1/hospital_patient", methods=["POST"], type='http', auth="none", csrf=False)
    def post_patient(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get('name'):
            return request.make_json_response({
                'error': 'Name is required',
            }, status=400)
        try:
            res = request.env['hospital.patient'].sudo().create(vals)
            if res:
                return request.make_json_response({
                    'message': 'patient record has been created successfully',
                    'id': res.id,
                    'name': res.name,
                }, status=201)
        except Exception as error:
            return request.make_json_response({
                'error': error,
            }, status=400)

    @http.route("/v1/hospital_patient/json", methods=["POST"], type='json',auth="none", csrf=False)
    def post_patient_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['hospital.patient'].sudo().create(vals)
        if res:
            return({
                'message': 'patient record has been created successfully'
            })

    @http.route("/v1/hospital_patient/<int:patient_id>", methods=["PUT"], type='http',auth="none", csrf=False)
    def update_patient(self,patient_id):
        try:
            patient_id = request.env['hospital.patient'].sudo().search([('id', '=', patient_id)])
            if not patient_id:
                return request.make_json_response({
                    'error': 'ID does not exist',
                }, status=400)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            patient_id.write(vals)
            return request.make_json_response({
                'message': 'patient record has been updated successfully',
                'id': patient_id.id,
                'name': patient_id.name,
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                'error': error,
            }, status=400)

    @http.route("/v1/hospital_patient/<int:patient_id>", methods=["GET"],type='http', auth="none", csrf=False)
    def get_patient(self, patient_id):
        try:
            patient_id = request.env['hospital.patient'].sudo().search(
                [('id', '=', patient_id)])
            if not patient_id:
                return invalid_response('ID does not exist', status=400)
            return valid_response({
                'id': patient_id.id,
                'name': patient_id.name,
                'date_of_birth': patient_id.date_of_birth,
                'age': patient_id.age,
                'gender': patient_id.gender,
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                'error': error,
            }, status=400)

    @http.route("/v1/hospital_patient/<int:patient_id>", methods=["DELETE"],type='http', auth="none", csrf=False)
    def delete_patient(self, patient_id):
        try:
            patient_id = request.env['hospital.patient'].sudo().search(
                [('id', '=', patient_id)])
            if not patient_id:
                return request.make_json_response({
                    'error': 'ID does not exist',
                }, status=400)
            patient_id.unlink()
            return request.make_json_response({
                'message': 'patient record has been deleted successfully',
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                'error': error,
            }, status=400)

    @http.route("/v1/hospital_patients", methods=["GET"],type='http', auth="none", csrf=False)
    def get_patients_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            patient_domain =[]
            page = offset = None
            limit = 0
            if params:
                if params.get('limit'):
                    limit = int(params.get('limit')[0])
                if params.get('page'):
                    page = int(params.get('page')[0])
            if page:
                offset = (page * limit) - limit
            if params.get('state'):
                patient_domain += [('state','in', params.get('state'))]
            patient_ids = request.env['hospital.patient'].sudo().search(patient_domain, offset=offset, limit=limit, order='id desc')
            patients_count = request.env['hospital.patient'].sudo().search_count(patient_domain)
            if not patient_ids:
                return invalid_response('There Are no records!', status=400)
            return valid_response([{
                'id': patient_id.id,
                'name': patient_id.name,
                'date_of_birth': patient_id.date_of_birth,
                'age': patient_id.age,
                'gender': patient_id.gender,
                'state': patient_id.state,
            } for patient_id in patient_ids], pagination_info={
                'page': page if page else 1,
                'limit': limit,
                'pages': math.ceil(patients_count / limit) if limit else 1,
                'count': patients_count
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                'error': error,
            }, status=400)
