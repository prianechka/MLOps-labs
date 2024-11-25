import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from heart_diseases_detector.db import get_db

bp = Blueprint('predict', __name__, url_prefix='/')

@bp.route('/predict', methods=['POST'])
def predict():
    return render_template('heart/result.html')
