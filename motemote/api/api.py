#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, abort, make_response, jsonify
import mote

api = Flask(__name__)


@api.route("/evaluation/<string:screenname>", methods=["GET"])
def mote_eval(screenname):
    try:
        print(screenname)
    except:
        abort(404)

    result = mote.calc_mote(screenname)
    return make_response(jsonify(result))


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    api.run(host='0.0.0.0', port=3000)
