from genesis_api import create_app
from genesis_api import socketio
from werkzeug.exceptions import HTTPException
import traceback

app = create_app()


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e
    print("Error:", traceback.print_exc(), flush=True)
    # now you're handling non-HTTP exceptions only
    return {"error": True, "message": str(e)}, 500

# Main app


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5555, debug=True)
