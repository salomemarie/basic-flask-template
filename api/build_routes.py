from flask import Blueprint, render_template

build_bp = Blueprint('build_bp', __name__)


@build_bp.route("/build")
def build():
    return render_template("build.html")