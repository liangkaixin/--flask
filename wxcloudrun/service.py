import os
import io
from PIL import Image
from flask import Flask, request, jsonify
import torch

from run import app

# 加载最轻 YOLOv5n 模型
model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
model.eval()

@app.route("/detect", methods=["POST"])
def detect_object():
    if 'file' not in request.files:
        return jsonify({"message": "未上传文件"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "文件名为空"}), 400

    try:
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        # 推理
        results = model(img)
        detections = results.pandas().xyxy[0].to_dict(orient="records")

        if not detections:
            return jsonify({'message': '未检测到物体'})

        # 返回第一个检测对象名称
        return jsonify({'message': f"检测到: {detections[0].get('name')}"})

    except Exception as e:
        return jsonify({"message": f"识别失败: {str(e)}"}), 500
