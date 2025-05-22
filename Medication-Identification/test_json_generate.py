# 测试代码（可另存为test.py）
from baidu_helper import BaiduHelper
from main_assistant import MedicineAssistant
def test_system():
    # 测试数据库生成
    helper = BaiduHelper()
    test_image = "demo.jpg"  # 你的测试处方图片路径
    
    # OCR识别测试
    ocr_result = helper.ocr_recognition(test_image)
    print("OCR测试结果:", ocr_result)
    
    # 数据库生成测试
    processed_data = helper.ernie_process(ocr_result)
    print("AI处理结果:", processed_data)
    
    # 助手功能测试
    assistant = MedicineAssistant()
    assistant.current_medicine = assistant.match_medicine("头孢克颗粒 50mg")
    print(assistant.process_command("这是什么药？"))
    print(assistant.process_command("怎么吃？"))

if __name__ == "__main__":
    test_system()