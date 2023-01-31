from app import app

if __name__ == "__main__":
    app.run(debug=True, port=5001) # run locally
    # app.run(host="0.0.0.0", port=8080, debug=True) # run as a docker container
