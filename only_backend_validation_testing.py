from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():






######################################################### IMPORTANT  #########################################################


    # Whether user is hits this URL the entire method will run-for the first time/submitting correctly/submitting with error
    message = ""

    # If it is a GET request, just render the form with empty fields(defined above)

    if request.method == "POST":
        name = request.form.get("name")
        value = request.form.get("value")

        
        if value == "No":
            message = "Previous entry submitted successfully!"
            
            # If it is a good POST request, render the form with empty fields again(defined above)

        else:
            message = "Error: Value must be 'No'. Please correct."



    # This rendering the template, will always be done for for all requests--GET/Good POST/Bad POST
    return render_template("only_backend_validation_testing.html", message=message)



######################################################### IMPORTANT  #########################################################





if __name__ == "__main__":
    app.run(debug=True)
