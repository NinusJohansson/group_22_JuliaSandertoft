# pylint: disable=cyclic-import
"""
File that contains all the routes of the application.
This is equivalent to the "controller" part in a model-view-controller architecture.
In the final project, you will need to modify this file to implement your project.
"""
# built-in imports
import io

# external imports
from flask import Blueprint, jsonify, render_template
from flask.wrappers import Response as FlaskResponse
from matplotlib.figure import Figure
from werkzeug.wrappers.response import Response as WerkzeugResponse

# internal imports
from codeapp.models import Jobs
from codeapp.utils import calculate_statistics, get_data_list, prepare_figure

# define the response type
Response = str | FlaskResponse | WerkzeugResponse

bp = Blueprint("bp", __name__, url_prefix="/")


################################### web page routes ####################################


@bp.get("/")  # root route
def home() -> Response:
    # gets dataset
    dataset: list[Jobs] = get_data_list()

    # get the statistics that is supposed to be shown
    counter: dict[int, int] = calculate_statistics(dataset)

    # render the page
    return render_template("home.html", counter=counter)


@bp.get("/image")
def image() -> Response:
    # gets dataset
    dataset: list[Jobs] = get_data_list()

    # get the statistics that is supposed to be shown
    counter: dict[int, int] = calculate_statistics(dataset)

    # creating the plot

    fig = Figure()
    fig.gca().grid(ls=":")
    fig.gca().hist(
        list(sorted(counter.keys())),
        bins=10,
    )
    fig.gca().set_xlabel("Spending Score (1-100)")
    fig.tight_layout()
    ################ START -  THIS PART MUST NOT BE CHANGED BY STUDENTS ################
    # create a string buffer to hold the final code for the plot
    output = io.StringIO()
    fig.savefig(output, format="svg")
    # output.seek(0)
    final_figure = prepare_figure(output.getvalue())
    return FlaskResponse(final_figure, mimetype="image/svg+xml")


@bp.get("/data")  # data route
def data() -> Response:
    # TODO: create here the route that renders the data.html file
    pass


@bp.get("/about")
def about() -> Response:
    return render_template("about.html")


################################## web service routes ##################################


@bp.get("/json-dataset")  # root route
def get_json_dataset() -> Response:
    # gets dataset
    dataset: list[Jobs] = get_data_list()

    # render the page
    return jsonify(dataset)


@bp.get("/json-stats")  # root route
def get_json_stats() -> Response:
    # gets dataset
    dataset: list[Jobs] = get_data_list()

    # get the statistics that is supposed to be shown
    counter: dict[int, int] = calculate_statistics(dataset)

    # render the page
    return jsonify(counter)
