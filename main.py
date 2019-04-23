from server import app, bind_port

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=bind_port)
