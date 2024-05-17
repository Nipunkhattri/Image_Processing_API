from flask_model import Flask, request, jsonify
import torch
from PIL import Image
import requests
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image
import requests

app = Flask(__name__)

processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")

@app.route('/detect', methods=['POST'])
def detect_objects():
    # Retrieve image data from request
    image_data = request.files.get('image')

    # Error handling: Check if image is present
    if not image_data:
        return jsonify({'error': 'No image provided'}), 400

    # Load image from request data
    image = Image.open(image_data.stream)

    # Preprocess, detect objects, and post-process as in the original code
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

    # Prepare response data (list of detected objects with details)
    detected_objects = []
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        detected_objects.append({
            "label": model.config.id2label[label.item()],
            "confidence": round(score.item(), 3),
            "bounding_box": box
        })

    return jsonify({'objects': detected_objects})

if __name__ == '__main__':
    app.run(debug=True)
