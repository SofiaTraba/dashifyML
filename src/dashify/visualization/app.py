import dash
from dashify.visualization.controllers.data_controllers import ExperimentController, MetricsController, ConfigController, GridSearchController
from dashify.visualization.controllers import data_controllers
from flask import request
from dashify.metrics.processor import MetricDataProcessor

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
from flask import jsonify


@app.server.route('/download_experiments_data')
def download_experiments_data():

    # get session id and filters
    session_id = request.args.get("session_id")
    filters = request.args.get("filters")

    # get experiments data
    ExperimentController.set_experiment_filters(session_id, filters.split(" && "))
    df_experiments = ExperimentController.get_experiments_df(session_id)
    csv_string = df_experiments.to_csv(index=False, encoding='utf-8')

    return csv_string


@app.server.route("/download_graph_data")
def download_graph_data():

    # get session id and metric id
    session_id = request.args.get("session_id")
    metric_tag = request.args.get("metric_tag")
    to_aggregate = request.args.get("aggregate")

    if to_aggregate == "True":
        json_data = jsonify(MetricDataProcessor.get_aggregated_data(session_id, metric_tag))
    else:
        json_data = jsonify(MetricDataProcessor.get_data(session_id, metric_tag))

    return json_data

@app.server.route("/download_settings_data")
def download_settings_data():

    session_id = request.args.get("session_id")
    grid_search_id = GridSearchController.get_activated_grid_search_id(session_id)

    settings_dict = {}
    settings_dict["config_settings"] = ConfigController.get_selected_configs_settings(session_id)
    settings_dict["metric_settings"] = MetricsController.get_metrics_settings(session_id).to_dict()
    settings_dict["filter_settings"] = data_controllers.cache_controller.get_experiment_filters(grid_search_id, session_id)
    return jsonify(settings_dict)