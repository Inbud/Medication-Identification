from baidu_helper import BaiduHelper
def test_playback():
    helper = BaiduHelper()
    # 测试短语音
    helper.tts_realtime("实时播放测试")
    # 测试长语音
    helper.tts_realtime("请遵医嘱，每日三次，每次一袋，温水冲服")

if __name__ == "__main__":
    test_playback()