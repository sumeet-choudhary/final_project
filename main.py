from application.register_login.views import register_login_blueprint
from application import app

app.register_blueprint(register_login_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
