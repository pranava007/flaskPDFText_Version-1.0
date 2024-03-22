from flask import Flask, render_template, request
import fitz  # PyMuPDF
import tempfile
import os



app = Flask(__name__)

def pdf_to_text(pdf_file):
    temp_pdf_file = tempfile.NamedTemporaryFile(delete=False)
    temp_pdf_file.write(pdf_file.read())
    temp_pdf_file.close()

    text = ""
    with fitz.open(temp_pdf_file.name) as doc:
        for page in doc:
            text += page.get_text()
    
    # Clean up temporary file
    os.unlink(temp_pdf_file.name)
    
    return text


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.pdf'):
            text = pdf_to_text(file)
            return render_template('result.html', text=text)
        else:
            return render_template('index.html', error='Please upload a valid PDF file.')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
