import threading
import sys
import time
import cv2
import speech_recognition as sr
from aip import AipSpeech, AipOcr
import erniebot

class BaiduHelper:
    def __init__(self, app_id, api_key, secret_key, access_token):
        self.client_Speech = AipSpeech(app_id, api_key, secret_key)
        self.client_Ocr = AipOcr(app_id, api_key, secret_key)
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
        self.cap = cv2.VideoCapture(0)
        self.audio_text = None
        self.stop_threads = False
        self.audio_thread = threading.Thread(target=self.audio_processing)
        erniebot.api_type = 'aistudio'
        erniebot.access_token = access_token

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def tts(self, text):
        result = self.client_Speech.synthesis(text, 'zh', 1, {'vol': 5})
        if not isinstance(result, dict):
            filename = 'audio.mp3'
            with open(filename, 'wb') as f:
                f.write(result)
            return filename
        print('tts failed')
        return None

    def get_text(self, wav_bytes):
        result = self.client_Speech.asr(wav_bytes, 'wav', 16000, {
            'dev_pid': 1537
        })
        return result['result'][0]

    def audio_processing(self):
        while not self.stop_threads:
            try:
                with self.mic as source:
                    self.r.adjust_for_ambient_noise(source)
                    audio = self.r.listen(source)
                audio_data = audio.get_wav_data(convert_rate=16000)
                print("Recognizing...")
                self.audio_text = self.get_text(audio_data)
            except Exception as e:
                print(f"Audio processing error: {e}")

    def start_audio_thread(self):
        self.audio_thread.start()

    def start_camera(self):
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            sys.exit(1)

        print("Camera opened successfully.")

        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Can't receive frame.")
                    break
                cv2.imshow('Camera Feed', frame)

                if '退出' in self.audio_text:
                    print("Quitting camera...")
                    break
                elif '拍照' in self.audio_text:
                    filename = f"capture_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
                    cv2.imwrite(filename, frame)
                    self.audio_text = None
                    break
        finally:
            self.stop_threads = True
            self.cap.release()
            cv2.destroyAllWindows()
            return filename

    def ernie_response(self, message, history):
        # model选用ernie-bot-4，定义输入的messages文本。
        model = 'ernie-4.0'
        messages = [{'role': 'user', 'content': message}]
        # 主函数 (model, messages)，实现根据传入的model名称和messages文本获取模型生成的内容结果。
        response = erniebot.ChatCompletion.create(
            model = model,
            messages = messages,
            top_p = 0.95) # top_p影响生成文本的多样性，取值越大，生成文本的多样性越强,取值范围为[0, 1.0]
        reply = response.get_result()
        return reply