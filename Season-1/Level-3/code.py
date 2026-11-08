import os
from flask import Flask, request

app = Flask(__name__)
@app.route("/")
def source():
    TaxPayer('foo', 'bar').get_tax_form_attachment(request.args["input"])
    TaxPayer('foo', 'bar').get_prof_picture(request.args["input"])

class TaxPayer:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.prof_picture = None
        self.tax_form_attachment = None

    def get_prof_picture(self, path=None):
        if not path:
            pass

        base_dir = os.path.dirname(os.path.abspath(__file__))
        prof_picture_path = os.path.normpath(os.path.join(base_dir, path))
        if not prof_picture_path.startswith(base_dir):
            return None

        with open(prof_picture_path, 'rb') as pic:
            picture = bytearray(pic.read())

        return prof_picture_path

    def get_tax_form_attachment(self, path=None):
        tax_data = None

        if not path:
            raise Exception("Error: Tax form is required for all users")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        tax_form_path = os.path.normpath(os.path.join(base_dir, path))
        if not tax_form_path.startswith(base_dir):
            return None

        with open(tax_form_path, 'rb') as form:
            tax_data = bytearray(form.read())

        return tax_form_path
