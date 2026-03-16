from flask import Flask, render_template, redirect, url_for, flash
from forms import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisshouldbeasecretkey'

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Here you can save the data to a database
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('success'))
    return render_template('register.html', form=form)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)