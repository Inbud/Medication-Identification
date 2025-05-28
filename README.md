# Medication-Identification

## 简介

Medication Identification 是一个基于百度服务的智能助手，能够通过拍照处方识别药品信息并语音播报用法用量，同时支持生成药物数据库。

## 功能

- 处方OCR识别：调用百度OCR接口提取处方文字信息
- 药品信息匹配：识别药品名称，查询本地或AI生成的药品数据库
- 语音播报：使用百度TTS实时合成与播放用法用量
- 文心一言（ErnieBot）AI处理：根据OCR结果生成结构化 JSON 数据
- 实时语音交互：监听语音指令，执行拍照、识别、查询、播报等操作

## 环境与依赖

- Python 3.x
- opencv-python
- SpeechRecognition
- pydub
- PyAudio
- baidu-aip
- erniebot
- playsound == 1.2.2

安装依赖：

```powershell
pip install -r requirements.txt
```

## 配置

在 `config.py` 中，填写百度AI和ErnieBot的 API Key 和 Token：

```python
SPEECH_APP_ID = '<你的百度语音识别AppID>'
SPEECH_API_KEY = '<你的百度语音识别API Key>'
SPEECH_SECRET_KEY = '<你的百度语音识别Secret Key>'

OCR_APP_ID = '<你的百度OCR AppID>'
OCR_API_KEY = '<你的百度OCR API Key>'
OCR_SECRET_KEY = '<你的百度OCR Secret Key>'

ERNIE_ACCESS_TOKEN = '<你的ErnieBot Access Token>'
```

## 项目结构

```text
.
├── baidu_helper.py            # 核心服务封装
├── config.py                  # 配置文件
├── main_assistant.py          # 智能助手主程序
├── main_generate_db.py        # 数据库生成主脚本
├── demo.jpg                   # 示例处方图片
├── demo.json                  # 示例 JSON 模板
├── requirements.txt           # 依赖列表
├── README.md                  # 项目说明
├── test_pydub.py              # TTS 播放测试
├── test_json_generate.py      # OCR 与 JSON 生成测试
├── test_ernie.py              # ErnieBot 接口测试
├── test_medicine_box.jpg      # 测试用处方图片
├── draft/                     # 草稿与备份目录
└── medicine_db.json           # 生成的药物数据库
```

## 测试

项目包含一些测试脚本：

- `test_pydub.py`：测试 TTS 播放功能
- `test_json_generate.py`：测试 OCR 识别与 JSON 生成
- `test_ernie.py`：测试 ErnieBot 接口

运行方式：

```powershell
python Medication-Identification/test_pydub.py
python Medication-Identification/test_json_generate.py
python Medication-Identification/test_ernie.py
```
