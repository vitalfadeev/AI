import os
from shutil import copyfile


def tb_wsgi_app(environ, start_response, Machine_ID, Resource):
    from tensorboard import default
    from tensorboard import program
    from tensorboard.backend import application
    from django.conf import settings

    BASE_DIR = settings.BASE_DIR


    plugins = default.get_plugins()
    assets_zip_provider = None

    tensorboard = program.TensorBoard(plugins, assets_zip_provider)

    # Create log dir
    log_dir = f"/tmp/tf-logs/{Machine_ID}"
    # log_dir = f"/{BASE_DIR}/media/tf-logs/{Machine_ID}"
    os.makedirs( log_dir, exist_ok=True )

    # Copy log
    copyfile( f"{BASE_DIR}/tf-logs/6/events.out.tfevents.1565787567.DESKTOP-8045KQ7", f"{log_dir}/events.out.tfevents.1565787567.DESKTOP-8045KQ7" )

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

