from server import app, bind_port
if __name__ == '__main__':
    app.secret_key = 'secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True, host='0.0.0.0', port=bind_port)
