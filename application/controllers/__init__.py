USER_LOGIN = {}
USER = []

def init_controllers(app): 
    prefix = "/api/v1"
    
    import application.controllers.identity as identity
    app.register_blueprint(identity.bp_app, url_prefix=prefix)
    
    import application.controllers.oauth2 as oauth2
    app.register_blueprint(oauth2.bp, url_prefix=prefix)
    
    import application.controllers.auth as auth
    app.register_blueprint(auth.bp, url_prefix=prefix)
    
    import application.controllers.client as client
    app.register_blueprint(client.bp, url_prefix=prefix)
    
    