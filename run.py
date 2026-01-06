from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port=5004)


# To run the application using Flask's built-in server, use the command:

"""
// Command to run the Flask application:-
// Start the virtual environment and run the Flask app on port 5004:

# Activate the virtual environment
.\venv\Scripts\activate  


$env:FLASK_APP = "run.py"


# Confirm by running:
echo $env:FLASK_APP



# Run the Flask app on port 5004
flask run --port 5004 



"""


