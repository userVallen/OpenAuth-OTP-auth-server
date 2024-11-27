from flask import Flask
from otp.routes import otp_blueprint

app = Flask(__name__)
app.register_blueprint(otp_blueprint, url_prefix='/otp')

if __name__ == '__main__':
    app.run(debug=True)
