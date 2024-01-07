stats server
if __name__ == "__main__":
    print("running on http://127.0.0.1:5000/ ")
    print()
    socketio.run(app, debug=True)