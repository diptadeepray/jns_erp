from flask import Flask, render_template, request, redirect
import sqlite3, os



def create_app():
    app = Flask(__name__)


    # Database path
    app.config['DATABASE'] = os.path.join(app.root_path, 'database.db')




    # ---------- INDIAN NUMBER FORMATTER ----------
    def indian_format(value):
        if value is None:
            return ""

        try:
            value = float(value)
        except:
            return value

        integer_part, _, decimal_part = f"{value:.2f}".partition(".")

        if len(integer_part) <= 3:
            formatted = integer_part
        else:
            last3 = integer_part[-3:]
            rest = integer_part[:-3]
            parts = []
            while len(rest) > 2:
                parts.insert(0, rest[-2:])
                rest = rest[:-2]
            if rest:
                parts.insert(0, rest)
            formatted = ",".join(parts) + "," + last3

        return formatted if decimal_part == "00" else f"{formatted}.{decimal_part}"
    

    
    # 🔥 REGISTER FILTER HERE
    app.jinja_env.filters["indian"] = indian_format
    # --------------------------------------------







    # Register Blueprints
    from onboarding.routes import onboarding_bp
    from inbound_payments.routes import inbound_payments_bp
    from outbound_payments.routes import outbound_payments_bp
    from dashboard.routes import dashboard_bp
    from all_data.routes import all_data_bp
    from delete_data.routes import delete_data_bp

    app.register_blueprint(onboarding_bp, url_prefix='/onboarding')
    app.register_blueprint(inbound_payments_bp, url_prefix='/inbound_payments')
    app.register_blueprint(outbound_payments_bp, url_prefix='/outbound_payments')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(all_data_bp, url_prefix='/all_data')
    app.register_blueprint(delete_data_bp, url_prefix='/delete_data')

    # Home route
    @app.route('/')
    def home():
        return render_template('home.html')
    
    
    
    return app


if __name__ == "__main__":
    app = create_app()
    #app.run()
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5005, debug=True)










# Whenever user clicks on a button which has href="/onboarding"
# This block of code runs
# @app.route("/onboarding", methods=["GET", "POST"])
# def red_page():
#     if request.method == "POST":

#         data = request.form.get("info")

#         conn = sqlite3.connect("database.db")

#         c = conn.cursor()
#         c.execute("INSERT INTO red_data(info) VALUES (?)", (data,))
        
#         conn.commit()
#         conn.close()
#         return redirect("/onboarding")
    
#     return render_template("onboarding.html")


# Whenever user clicks on a button which has href="/inbound_process"
# This block of code runs
# @app.route("/inbound_payments", methods=["GET", "POST"])
# def inbound_payments():
#     if request.method == "POST":

#         a_number = request.form["a_number"]
#         first_text = request.form["first_text"]
#         second_text = request.form["second_text"]

#         conn = sqlite3.connect("database.db")
#         c = conn.cursor()
#         c.execute("INSERT INTO demo (a_number, first_text, second_text) VALUES (?, ?, ?)",
#                   (a_number, first_text, second_text))
#         conn.commit()
#         conn.close()

#         return redirect("/inbound_payments")
    
#     return render_template("inbound_payments.html")

# @app.route("/outbound_payments")
# def outbound_payments():
#     conn = sqlite3.connect("database.db")
#     c = conn.cursor()
#     c.execute("SELECT * FROM demo")
#     rows = c.fetchall()
#     conn.close()
#     return render_template("outbound_payments.html", rows=rows)