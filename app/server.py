import random
import time
import pandas as pd
from flask import Flask, render_template
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode="threading")


df = pd.DataFrame(columns=["transaction_id", "customer_id", "amount"])
transaction_id = 1


@app.route("/")
def index():
    return render_template("dashboard.html")


def generate_transaction():
    global transaction_id, df

    t = {
        "transaction_id": transaction_id,
        "customer_id": random.randint(100, 200),
        "amount": round(random.uniform(1, 100), 2)
    }

    df.loc[len(df)] = t
    transaction_id += 1

    return t


def stream_data():
    while True:
        new_tx = generate_transaction()
        socketio.emit("new_transaction", new_tx)
        time.sleep(1)


def start_server():
    socketio.start_background_task(target=stream_data)
    socketio.run(app, host="0.0.0.0", port=5000)
