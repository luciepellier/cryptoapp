from flask import current_app as app
from flask import render_template

@app.route("/")
def home():
    return render_template(
        "hello.html",
        title="Exemple de templates jinja",
        description="Mon app avec flask et jinja"
    )