# from application.controllers.auth import bp_oauth2
# from application.controllers.identity import bp_app

# from repo.application.controllers.auth_api import USER_LOGIN

USER_LOGIN = {}
USER = []

def init_controllers(app): 
    # import application.controllers.auth as auth
    # app.register_blueprint(auth.bp_oauth2, url_prefix="/oauth2")
    prefix = "/api/v1"
    
    import application.controllers.identity as identity
    app.register_blueprint(identity.bp_app, url_prefix=prefix)
    
    # import application.controllers.home as home
    # app.register_blueprint(home.bp_home, url_prefix="")
    
    import application.controllers.auth_api as auth
    app.register_blueprint(auth.bp, url_prefix=prefix)
    
    import application.controllers.client as client
    app.register_blueprint(client.bp, url_prefix=prefix)
    
    