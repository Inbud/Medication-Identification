from baidu_helper import BaiduHelper
import json

def generate_medicine_db():
    helper = BaiduHelper()
    
    # 拍摄处方照片
    print("请对准处方单，按空格键拍照...")
    #image_path = helper.capture_prescription()
    image_path = "demo.jpg"
    if not image_path:
        return
    
    # OCR识别
    ocr_result = helper.ocr_recognition(image_path)
    print("OCR识别结果:", ocr_result)
    
    # 调用文心处理
    processed_data = helper.ernie_process(ocr_result)
    
    # 清理响应格式
    if processed_data.startswith("```json"):
        processed_data = processed_data[7:-3].strip()
    
    # 保存数据库
    with open('medicine_db.json', 'w', encoding='utf-8') as f:
        f.write(processed_data)
    print("数据库已更新！")

if __name__ == "__main__":
    generate_medicine_db()