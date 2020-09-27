from apis.initialization import configure_app, register_blueprint


app = configure_app()
register_blueprint(app)

