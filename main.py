from math import ceil, floor

from flask import Flask, render_template, request, json, abort
from flask_socketio import SocketIO

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate/", methods=["POST", "GET"])
def calculate():

    if request.method == "GET":
        return abort(405)

    try:
        data = json.loads(request.data)

        if not data.get("credit"):
            socketio.emit("error", data={"msg": "Please fill out the boxes above"}, to=data.get("socket_id"))
            return '', 204


        creditFee = 5525 if data.get("oldBatch") else 6500
        credits = int(data.get("credit"))
        waiver = int(data.get("scholarship")) / 100
        transportFee = 4000 if data.get("transport") else 0

        total = credits*creditFee
        total -= total * waiver
        total += 6500

        resp = {
            "total": total + transportFee,
            "first": total * 0.4 + transportFee,
            "second": ceil(total * 0.3),
            "third": floor(total * 0.3)
        }

        socketio.emit("result", data=resp, to=data.get("socket_id"))
    except Exception:
        socketio.emit("error", data={"msg": "An Error occurred!!! Please try again later."}, to=data.get("socket_id"))
    finally:
        return '', 204

@app.errorhandler(405)
def notAllowed(_):
    return render_template(
        f"error.html",
        home=True,
        errorCode=405,
        msgs=[
            "You are not supposed to enter that link manually!",
            "Click the button below to go home and then click on the calculate button to calculate your installment."
        ]
    )

@app.errorhandler(404)
def notFound(_):

    return render_template(
        f"error.html",
        home=True,
        errorCode=404,
        msgs=["Oops! Seems we are lost.", "Let's click the button below and go home :)"]
    )

@app.errorhandler(500)
def somethingWrong(_):
    return render_template("error.html", errorCode=500, msgs=["Something went wrong!", "Let's go home by clicking the button below"])

if __name__ == "__main__":
    socketio = SocketIO(app)
    socketio.run(app, host="0.0.0.0", port=80, debug=False)