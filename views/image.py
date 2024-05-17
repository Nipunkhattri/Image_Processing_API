from flask_restx import Namespace,Resource
from flask import request,jsonify
from PIL import Image
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch

image_api = Namespace('image')

processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")

@image_api.route('/object-detection/')
class DetectImages(Resource):
    def post(self):
        """
        Detection the objects in the images
        """
        image_data = request.files.get('image')

        if not image_data:
            return jsonify({'error':'No image provided'})
        
        image = Image.open(image_data.stream)

        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        target_sizes = torch.tensor([image.size[::-1]])
        results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

        detected_objects = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            detected_objects.append({
                "label": model.config.id2label[label.item()],
                "confidence": round(score.item(), 3),
                "bounding_box": box
            })

        return jsonify({'objects': detected_objects})
