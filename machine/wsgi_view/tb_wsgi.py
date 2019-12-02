import os
from shutil import copyfile

from django.shortcuts import get_object_or_404

from machine.models import Machine


def tb_wsgi_app(environ, start_response, Machine_ID, Resource):
    from tensorboard import default
    from tensorboard import program
    from tensorboard.backend import application
    from django.conf import settings

    BASE_DIR = settings.BASE_DIR

    # Getting Machine
    machine = get_object_or_404( Machine, pk=Machine_ID )

    # Init TB
    plugins = default.get_plugins()
    assets_zip_provider = None

    tensorboard = program.TensorBoard(plugins, assets_zip_provider)

    # Create log dir
    log_dir = f"/tmp/tf-logs/{Machine_ID}"
    # log_dir = f"/{BASE_DIR}/media/tf-logs/{Machine_ID}"
    os.makedirs( log_dir, exist_ok=True )

    # Copy log
    timestamp = "1565787567"
    station = "DESKTOP-8045KQ7"

    with open( f"{log_dir}/events.{timestamp}.{station}", 'wb' ) as f:
        f.write( machine.Training_FileTensorBoardLog )

    # Prepare TB args
    argv = [__file__,
        f'--logdir={log_dir}',
        f'--path_prefix=/Machine/{Machine_ID}/NN/'
    ]
    tensorboard.configure(argv=argv)

    # Run TB WSGI app
    app = application.standard_tensorboard_wsgi(tensorboard.flags,
                                                tensorboard.plugin_loaders,
                                                tensorboard.assets_zip_provider)

    return app(environ, start_response)

