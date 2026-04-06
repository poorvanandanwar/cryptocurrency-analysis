from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

# -------------------------------
# LOAD DATA
# -------------------------------
BASE = os.getcwd()   # for local
DATA_PATH = os.path.join(BASE, "data/processed")

df = pd.read_csv(os.path.join(DATA_PATH, "all_coins_clean.csv"))

try:
    model_df = pd.read_csv(os.path.join(DATA_PATH, "04_model_summary.csv"))
except:
    model_df = pd.DataFrame()

# -------------------------------
# ROUTES
# -------------------------------

@app.route("/")
def home():
    coins = df['Coin'].unique().tolist()
    return render_template("index.html", coins=coins)

@app.route("/get_coin_data/<coin>")
def get_coin_data(coin):
    coin_df = df[df['Coin'] == coin]

    return jsonify({
        "dates": coin_df['Date'].astype(str).tolist(),
        "prices": coin_df['Close'].tolist(),
        "high": float(coin_df['High'].max()),
        "low": float(coin_df['Low'].min()),
        "latest": float(coin_df['Close'].iloc[-1])
    })

@app.route("/model_summary")
def model_summary():
    return model_df.to_json(orient="records")


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)