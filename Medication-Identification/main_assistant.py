# main_assistant.py
# main_assistant.py
from baidu_helper import BaiduHelper
import cv2
import json
import speech_recognition as sr

class MedicineAssistant:
    def __init__(self):
        self.helper = BaiduHelper()
        self.medicine_db = self.load_db()
        self.current_medicine = None

    def load_db(self):
        try:
            with open('medicine_db.json', 'r', encoding='utf-8') as f:
                return json.load(f)['User']
        except Exception as e:
            print(f"加载数据库失败: {str(e)}")
            return []

    def match_medicine(self, ocr_text):
        ocr_text = ocr_text.lower()
        for med in self.medicine_db:
            if med['name'].lower() in ocr_text:
                return med
        return None

    def process_command(self, command):
        response = None
        try:
            if "拍照" in command:
                self.current_medicine = None
                print("请对准药品拍照...")
                #image_path = self.helper.capture_prescription()
                image_path = 'test.jpg'
                if image_path:
                    ocr_result = self.helper.ocr_recognition(image_path)
                    ocr_text = '\n'.join([item['words'] for item in ocr_result.get('words_result', [])])
                    self.current_medicine = self.match_medicine(ocr_text)
                    response = "拍照成功，已识别药品信息"
                else:
                    response = "拍照失败，请重试"
                
            elif "是什么" in command:
                if self.current_medicine:
                    response = f"这是{self.current_medicine['name']}"
                else:
                    response = "请先拍照识别药品"
                
            elif "怎么吃" in command:
                if self.current_medicine:
                    response = f"{self.current_medicine['name']}的用法：{self.current_medicine['usage']}，用量：{self.current_medicine['dosage']}"
                else:
                    response = "请先拍照识别药品"
                
            elif "退出" in command:
                exit()
                
            else:
                response = "未识别的指令"

            # 直接调用实时语音接口
            if response:
                self.helper.tts_realtime(response)  # 关键修改点

        except Exception as e:
            print(f"指令处理异常: {str(e)}")
            self.helper.tts_realtime("系统出现错误，请重试")

    def run(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("助手已启动，等待指令...")
            recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    audio = recognizer.listen(source, timeout=5)
                    wav_data = audio.get_wav_data(convert_rate=16000)
                    text = self.helper.speech_to_text(wav_data)
                    if text:
                        print("识别到指令:", text)
                        self.process_command(text)
                        
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    print(f"运行时错误: {str(e)}")
                    self.helper.tts_realtime("系统异常，正在恢复")

if __name__ == "__main__":
    assistant = MedicineAssistant()
    assistant.run()