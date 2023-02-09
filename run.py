from server import create_app
from config import DevConfig
from routes.example_routes import example

app = create_app(DevConfig, example)

if __name__ == "__main__":
    app.run()

