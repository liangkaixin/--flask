# 设置保存目录
import os
from flask import request, jsonify
from run import app
from datetime import datetime

SAVE_DIR = "uploaded_images"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route("/face_recognition", methods=["POST"])
def recognize_face():
    if 'file' not in request.files:
        return jsonify({"message": "未上传文件"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "文件名为空"}), 400

    try:
        # 生成文件名（使用时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        save_path = os.path.join(SAVE_DIR, filename)

        # 保存照片到本地
        file.save(save_path)
        return jsonify({"message": "上传成功"}), 200

    except Exception as e:
        return jsonify({"message": f"识别失败: {str(e)}"}), 500