"""
GET /pets - Returns a list all of the Pets
GET /pets/{id} - Returns the Pet with a given id number
POST /pets - creates a new Pet record in the database
PUT /pets/{id} - updates a Pet record in the database
DELETE /pets/{id} - deletes a Pet record in the database
"""

from flask import jsonify, request, url_for, make_response, abort
from werkzeug.exceptions import NotFound
from . import status  # HTTP Status Codes
from . import app  # Import Flask application

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import RecommendationModel, DataValidationError

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Recommendation Demo REST API Service",
            version="1.0",
            paths=url_for("list_recs", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    RecommendationModel.init_db(app)


    ######################################################################
# LIST ALL RECOMMENDATIONS
######################################################################
@app.route("/recs", methods=["GET"])
def list_recs():
    """Returns all of the Recommendations"""
    app.logger.info("Request for recommendation list")
    recs = []
    prod_A_id = request.args.get("prod_A_id")
    prod_B_id = request.args.get("prod_B_id")
    prod_B_name = request.args.get("prod_B_name")
    name = request.args.get("name")
    if prod_A_id:
        recs = RecommendationModel.find_by_prod_A_id(prod_A_id)
    elif name:
        recs = RecommendationModel.find_by_name(name)
    elif prod_B_id:
        recs = RecommendationModel.find_by_prod_B_id(prod_B_id)
    elif prod_B_name:
        recs = RecommendationModel.find_by_prod_B_name(prod_B_name)
    else:
        recs = RecommendationModel.all()

    results = [rec.serialize() for rec in recs]
    app.logger.info("Returning %d recommendation", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)