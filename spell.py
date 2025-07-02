from flask import Flask, render_template, request
from markupsafe import Markup
from textblob import TextBlob

app = Flask(__name__)

def highlight_corrections(original, corrected):
    orig_words = original.split()
    corr_words = corrected.split()
    highlighted = []
    for o, c in zip(orig_words, corr_words):
        if o != c:
            highlighted.append(f'<span style="background: #ffff99">{c}</span>')
        else:
            highlighted.append(c)
    # Add any extra words (if corrected text is longer)
    if len(corr_words) > len(orig_words):
        for c in corr_words[len(orig_words):]:
            highlighted.append(f'<span style="background: #ffff99">{c}</span>')
    return ' '.join(highlighted)

@app.route('/', methods=['GET', 'POST'])
def index():
    corrected = ''
    original = ''
    highlighted = ''
    if request.method == 'POST':
        # Check if a file is uploaded and has a filename
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            if file and file.filename.endswith('.txt'):
                original = file.read().decode('utf-8')
            else:
                original = ''
        else:
            original = request.form.get('text', '')
        if original.strip():
            corrected = str(TextBlob(original).correct())
            highlighted = Markup(highlight_corrections(original, corrected))
    return render_template('index.html', corrected=corrected, original=original, highlighted=highlighted)

if __name__ == '__main__':
    app.run(debug=True)
