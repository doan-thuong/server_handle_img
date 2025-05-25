from flask import Flask, request, jsonify
import easyocr
from PIL import Image
import io

app = Flask(__name__)
reader = easyocr.Reader(['en', 'vi'])

@app.route('/ocr', methods=['POST'])
def ocr_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image'].read()
    img = Image.open(io.BytesIO(image))
    results = reader.readtext(img)
    texts = [text for _, text, _ in results]
    return jsonify({'texts': texts})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
