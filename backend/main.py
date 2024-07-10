import dateutil.parser
from flask import Flask, request
from markupsafe import escape
import urllib
import dateutil
from datetime import datetime
import os

PORT = 5000
DATABASE = "db"


app = Flask("Intellinodes")


@app.route("/api/search")
def search():
    from_date = request.values.get("fromDate", None)
    to_date = request.values.get("toDate", None)
    sort: str = request.values.get("sort")

    pass


if __name__ == "__main__":
    # flask --app main run --debug
    app.run(
        port=PORT,
        debug=True
    )