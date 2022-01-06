from application.entry import app 

def run_app(host='127.0.0.1', port=2525, debug=False, ssl_context=None): 
    app.run(host=host, port=port, debug=debug)
    