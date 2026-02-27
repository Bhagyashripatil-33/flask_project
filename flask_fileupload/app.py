from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if file.filename == '':
        return "No file selected"

    # Save file directly in project folder (NO upload folder)
    file.save(file.filename)

    return render_template('success.html', filename=file.filename)

if __name__ == '__main__':
    app.run(debug=True)