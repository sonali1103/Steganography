from flask import Flask



app = Flask(__name__)
app.config['SECRET_KEY'] = 'BHSIDJHG lhjdgfytewv'


def create_app(): 
   
    from .home import home
    from .auth import auth
    from .encode import encode
    from .decode import decode
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(encode, url_prefix='/')
    app.register_blueprint(decode, url_prefix='/')

    return app