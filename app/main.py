from flask import Flask

from app.routes.phone_route import phone_blueprint
from app.routes.statistics_route import statistics_blueprint

app = Flask(__name__)


app.register_blueprint(phone_blueprint, url_prefix='/api')
app.register_blueprint(statistics_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
