import argparse
import dashify
from dashify.visualization.app import app
from dashify.visualization.layout_definition import layout

def parse_args():
    parser = argparse.ArgumentParser(description='Visualize grid search experiments')
    parser.add_argument('--logdir', type=str, help='Path tho the grid search root directory')
    args = parser.parse_args()
    log_dir = args.logdir
    if log_dir is None:
        raise Exception("Please speficy the log dir with --logdir <your grid search log dir>")
    else:
        return log_dir


if __name__ == '__main__':
    dashify.visualization.log_dir = parse_args()
    app.layout = layout
    app.run_server(debug=True)
