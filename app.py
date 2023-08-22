from server.manage import app, sio

if __name__ == "__main__":
    sio.run(app, host='192.168.1.118', port=5000)
