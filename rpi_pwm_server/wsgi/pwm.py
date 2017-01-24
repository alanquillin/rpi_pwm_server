from flask_restful import reqparse
from flask_restful import Resource

from rpi_pwm_server.pwm import PWMCtl


import logging

LOG = logging.getLogger(__name__)


class PWMResourse(Resource):
    def get(self, *args, **kwargs):
        return self._get_current_state()

    def post(self, *args, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('mode', required=True)
        parser.add_argument('value')
        args = parser.parse_args()

        mode = args.get('mode')
        pwm_value = args.get('value')

        PWMCtl.setmode(mode, pwm_value=pwm_value)

        return self._get_current_state(), 200

    @staticmethod
    def _get_current_state():
        return dict(mode=PWMCtl.get_mode_display_value(),
                    value=PWMCtl.get_pwm_display_value())
