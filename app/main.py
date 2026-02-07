from . import create_app

app = create_app()

if __name__ == "__main__":
    # host="0.0.0.0" makes it accessible on localhost
    # port=8000 changes from 5000 to 8000
    app.run(host="0.0.0.0", port=8000, debug=True)

