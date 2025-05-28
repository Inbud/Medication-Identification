import threading
import cv2
import speech_recognition as sr
from aip import AipSpeech, AipOcr
import erniebot
from config import *
import pyaudio
import io
from pydub import AudioSegment
from pydub.playback import play


class BaiduHelper:
    def __init__(self):
        # 初始化语音服务
        self.speech_client = AipSpeech(SPEECH_APP_ID, SPEECH_API_KEY, SPEECH_SECRET_KEY)
        
        # 初始化OCR服务
        self.ocr_client = AipOcr(OCR_APP_ID, OCR_API_KEY, OCR_SECRET_KEY)
        
        # 语音识别相关
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
        
        # 文心一言
        erniebot.api_type = 'aistudio'
        erniebot.access_token = ERNIE_ACCESS_TOKEN

        self.pyaudio_instance = pyaudio.PyAudio()

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def tts(self, text):
        result = self.speech_client.synthesis(text, 'zh', 1, {'vol': 5})
        if not isinstance(result, dict):
            return result
        return None

    def speech_to_text(self, audio_data):
        try:
            result = self.speech_client.asr(audio_data, 'wav', 16000, {'dev_pid': 1537})
            if result['err_no'] == 0:
                return result['result'][0]
            return None
        except Exception as e:
            print(f"语音识别错误: {e}")
            return None

    def ocr_recognition(self, image_path):
        image = self.get_file_content(image_path)
        result = self.ocr_client.basicGeneral(image)
        return result

    def capture_prescription(self):
        cap = cv2.VideoCapture(0)
        try:
            while True:
                ret, frame = cap.read()
                cv2.imshow('按空格拍照，ESC退出', frame)
                key = cv2.waitKey(1)
                if key == 32:  # 空格键
                    filename = 'captured_prescription.jpg'
                    cv2.imwrite(filename, frame)
                    return filename
                elif key == 27:  # ESC键
                    return None
        finally:
            cap.release()
            cv2.destroyAllWindows()

    def ernie_process(self, ocr_result):
        with open("demo.json", 'r', encoding='utf-8') as f:
            demo = f.read()
        
        response = erniebot.ChatCompletion.create(
            model='ernie-4.0',
            messages=[{
                'role': 'user',
                'content': f"请根据处方OCR结果生成json，格式参考{demo}，OCR结果为{ocr_result},注意用量部分可能需要计算和语序调整，例如：处方中显示规格50mg*6，用量为每次50mg每日三次，你需要换算为每日三次每次一颗"
            }]
        )
        return response.get_result()
    # 修改 baidu_helper.py 中的 tts_realtime 方法
    def tts_realtime(self, text):
        """实时语音合成与播放"""
        result = self.speech_client.synthesis(
            text, 'zh', 1, {'spd': 5, 'pit': 5, 'vol': 5, 'per': 4}
        )
        
        if not isinstance(result, dict):
            # 将MP3字节流转换为PCM格式
            audio = AudioSegment.from_file(io.BytesIO(result), format="mp3")
            pcm_data = audio.export(format="wav").read()
            
            # 使用pyaudio实时播放
            p = pyaudio.PyAudio()
            stream = p.open(
                format=p.get_format_from_width(audio.sample_width),
                channels=audio.channels,
                rate=audio.frame_rate,
                output=True
            )
            stream.write(pcm_data)
            stream.stop_stream()
            stream.close()
            p.terminate()
        else:
            print("TTS failed:", result)
