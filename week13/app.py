from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def developer_portal():
        return render_template("index.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
