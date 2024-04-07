import flask
import requests
from flask import make_response, jsonify
from flask import request

from . import db_session
from .ads import Ads

blueprint = flask.Blueprint(
    'ads_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/ads/<ads_id>')
def get_ads2(ads_id):
    try:
        ads_id = int(ads_id)
        db_sess = db_session.create_session()
        ads = db_sess.query(Ads).get(ads_id)
        if not ads:
            return make_response(jsonify({'error': 'Not found'}), 404)
        data = {'ads': [{'id': ads.id, 'id_user': ads.id_user, 'id_game': ads.id_game, 'text': ads.text,
                          'product_quantity': ads.product_quantity, 'start_date': ads.start_date, 'end_date': ads.end_date}]}
        return flask.jsonify(data)
    except Exception:
        return make_response(jsonify({'error': 'Not found'}), 404)


@blueprint.route('/api/ads',  methods=['GET', 'POST'])
def get_ads():
    db_sess = db_session.create_session()
    if request.method == 'GET':

        ads = db_sess.query(Ads).all()
        data = {
            'jobs': [{'id': ad.id, 'id_user': ad.id_user, 'id_game': ad.id_game, 'text': ad.text,
                      'product_quantity': ad.product_quantity, 'start_date': ad.start_date, 'end_date': ad.end_date} for ad in
                     ads]}
        return flask.jsonify(data)
    elif request.method == "POST":
        if not request.json:
            return make_response(jsonify({'error': 'Empty request'}), 400)
        elif not all(key in request.json for key in
                     ['id_user', 'id_game', 'text', 'product_quantity']):
            return make_response(jsonify({'error': 'Bad request'}), 400)
        db_sess = db_session.create_session()
        ads = Ads(
            id_user=request.json['id_user'],
            id_game=request.json['id_game'],
            text=request.json['text'],
            product_quantity=request.json['product_quantity'],
        )
        db_sess.add(ads)
        db_sess.commit()
        return jsonify({'id': ads.id})

@blueprint.route('/api/ads/<int:ads_id>', methods=['DELETE'])
def delete_ads(ads_id):
    db_sess = db_session.create_session()
    ads = db_sess.query(Ads).get(ads_id)
    if not ads:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(ads)
    db_sess.commit()
    return jsonify({'success': 'OK'})


