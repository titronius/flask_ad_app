from flask import Flask, request, jsonify
from flask.views import MethodView

from models import BdInstruments, Ad

app = Flask(__name__)

@app.before_request
def before_requests():
    session = BdInstruments.get_session()
    request.session = session


@app.after_request
def after_request(http_response):
    request.session.close()
    return http_response

class UserView(MethodView):
    def get(self, ad_id):
        ad = Ad.ad_get_by_id(request.session, ad_id)
        return jsonify(ad.dict)

    def post(self):
        json_data = request.json
        ad = Ad.ad_insert(request.session, json_data['title'], json_data['description'], json_data['user_id'])
        return jsonify(ad.dict)

    def delete(self, ad_id):
        Ad.ad_delete(request.session, ad_id)
        return jsonify({"status": "deleted"})

ad_view = UserView.as_view('ad')

app.add_url_rule('/ad/<int:ad_id>', view_func=ad_view, methods=['GET','DELETE'])
app.add_url_rule('/ad', view_func=ad_view, methods=['POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443)