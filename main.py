from os import path

from flask import Flask
from flask_login import LoginManager

from models import db, create_database, DB_NAME, User


def create_app():
    app = Flask(__name__)
    # The secret key to encrypt session message,keys
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    # Data base Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    create_database(app)

    from auth import auth
    from views import views

    # Register Blueprint to app
    app.register_blueprint(auth)
    app.register_blueprint(views)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
