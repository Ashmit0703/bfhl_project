from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for Flask-WTF

class DataForm(FlaskForm):
    json_input = TextAreaField('JSON Input', validators=[DataRequired()])
    options = SelectMultipleField(
        'Options',
        choices=[
            ('alphabets', 'Alphabets'),
            ('numbers', 'Numbers'),
            ('highest_lowercase', 'Highest lowercase alphabet')
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')

@app.route('/bfhl', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return {"operation_code": 1}
        # return render_template('get_page.html', operation_code=1)

    if (request.method == "POST"):
        data = request.json.get('data', {}).get("array", [])
        if (len(data) == 0):
            return jsonify(is_success=False, error="No data was given")

        numbers_list = []
        alphabets = []
        highest_lower_case_alphabet = []

        for i in data:
            try:
                _ = int(i)
                numbers_list.append(i)
            except:
                if i.isalpha()  and (len(i) > 1):
                    print(i)
                    return jsonify(is_success=False, error="alphabet with length > 1 given")

                alphabets.append(i)
                if (i.islower()):
                    highest_lower_case_alphabet = [i]

        return jsonify(
            is_success=True,
            user_id="ashmit_sangtani_07032003",
            email="ashmit.sangtani2021@vitstudent.in",
            roll_number="21BAI1539",
            numbers=numbers_list,
            alphabets=alphabets,
            highest_lowercase_alphabet=highest_lower_case_alphabet
        )


@app.route('/', methods=['GET', 'POST'])
def index():
    form = DataForm()
    response = None
    error = None

    if form.validate_on_submit():
        try:
            data = json.loads(form.json_input.data)
            options = form.options
            result = {
                'alphabets': [x for x in data if x.isalpha()],
                'numbers': [x for x in data if x.isdigit()],
                'highest_lowercase': max((x for x in data if x.islower()), default=None),
                'is_success': True,
                'user_id': "ashmit_sangtani_07032003",
                'email': "ashmit.sangtani2021@vitstudent.in",
                'roll_number': "21BAI1539"
            }
            response = result
        except json.JSONDecodeError:
            error = 'Invalid JSON format'
        except Exception as e:
            error = str(e)

    return render_template('index.html', form=form, response=response, error=error)

if __name__ == '__main__':
    app.run(debug=True)
