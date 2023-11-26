from server.manage import app, sio

if __name__ == "__main__":
    sio.run(app, app.config['APP_HOST'], port=app.config['APP_PORT'])
