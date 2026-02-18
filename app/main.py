from . import create_app

app = create_app()

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(host="127.0.0.1", port=8081, debug=True, use_reloader=False, use_debugger=False)
