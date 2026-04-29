from flask import Flask, render_template, request, jsonify
import logging
from datetime import datetime

from views import main_page, events_page

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/main")
def api_main():
    date_str = request.args.get("date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info(f"API main: date={date_str}")
    try:
        result = main_page(date_str)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in api_main: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/events")
def api_events():
    date_str = request.args.get("date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    period = request.args.get("period", "M")
    logger.info(f"API events: date={date_str}, period={period}")
    try:
        result = events_page(date_str, period)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in api_events: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/search")
def api_search():
    query = request.args.get("q", "")
    logger.info(f"API search: query={query}")
    
    from modules.search import search_transactions
    from data_loader import get_transactions
    
    transactions = get_transactions()
    results = search_transactions(transactions, query)
    
    return jsonify(results[:100])


if __name__ == "__main__":
    app.run(debug=True)
