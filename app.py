from flask import Flask, request, jsonify
import easyocr
from PIL import Image
import io
import re

app = Flask(__name__)
reader = easyocr.Reader(['en', 'vi'])

@app.route('/ocr', methods=['POST'])
def ocr_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image'].read()
    img = Image.open(io.BytesIO(image)).convert('L')
    results = reader.readtext(img)
    
    full_text = ''.join([text.replace(' ', '') for _, text, _ in results])
    
    match = re.search(r'(GPA\.\d{4}-\d{4}-\d{4}-\d{5})', full_text)

    gpa_texts = match.group()

    if not gpa_texts:
        return jsonify({'text:' "Not found GPA..."}), 200

    return jsonify({'text': gpa_texts}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)