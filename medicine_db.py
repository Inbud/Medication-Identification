from baiduhelper import BaiduHelper


APP_ID = '118123288'
API_KEY = '2rfD88yLK52Ap2I50vYO2pbO'
SECRET_KEY = 'uKAXPPT5so9U0KWQ6M12UDTbbA3qVg0p'
ACCESS_TOKEN = '9c65fffa42e7ebf28b9fcd1d1537b582a3b31094'
helper = BaiduHelper(APP_ID, API_KEY, SECRET_KEY, ACCESS_TOKEN)

filepath = helper.start_camera()
image = helper.get_file_content(filepath)
# image = helper.get_file_content('demo.jpg')
result = helper.client_Ocr.basicGeneral(image)
# print(result)

# 测试数据
# result = {
#     'words_result': [
#         {'words': '儿科'}, 
#         {'words': '众意好医师演示处方笺'}, 
#         {'words': '费别：自费'}, 
#         {'words': '医疗证/医保卡号：'}, 
#         {'words': '处方编号：120008'}, 
#         {'words': '姓名：张三'}, 
#         {'words': '性别：男'}, 
#         {'words': '年龄：1岁7月'}, 
#         {'words': '门诊/住院病历号：BL1508120005'}, 
#         {'words': '科室病区/床位号)：全科'}, 
#         {'words': '临床诊断：手足口病'}, 
#         {'words': '开其日期：201508-12'}, 
#         {'words': '住址/电话：广东广州市/07562222470'}, 
#         {'words': 'Rp.'}, {'words': '1.头孢克颗粒'}, 
#         {'words': '50mg*6袋'}, {'words': '×1盒'}, 
#         {'words': '用法：口服每次50mg'}, 
#         {'words': '每日二次'}, 
#         {'words': '2利巴韦林颗粒'}, 
#         {'words': '50mg*18袋'}, 
#         {'words': '×1盒'}, 
#         {'words': '用法：口服'}, 
#         {'words': '每次50mg'}, 
#         {'words': '每日三次'}, 
#         {'words': '3板蓝根颗粒'}, 
#         {'words': '10g*20袋/盒'}, 
#         {'words': '×1大袋'}, 
#         {'words': '用法：口服'}, 
#         {'words': '每次10g'}, 
#         {'words': '每日三次'}, 
#         {'words': '4口腔炎喷雾剂'}, 
#         {'words': '10m1:30g×1盒'}, 
#         {'words': '用法：外涂患处'}, 
#         {'words': '每次适量每日三次'}, 
#         {'words': '(以下空白)'}, 
#         {'words': '药品费用'}, 
#         {'words': '诊疗费'}, 
#         {'words': '医材费'}, 
#         {'words': '检查治疗费'}, 
#         {'words': '其它费'}, 
#         {'words': '合计'}, 
#         {'words': '40.50'}, 
#         {'words': '10.00'}, 
#         {'words': '1.00'}, 
#         {'words': '35.00'}, 
#         {'words': '0.00'}, 
#         {'words': '86.50'}, 
#         {'words': '医师：李医生'}, 
#         {'words': '蔷憩'}, 
#         {'words': '药品金额：40.50'}, 
#         {'words': '审核药师：'}, 
#         {'words': '雪0'}, 
#         {'words': '调配药师/士：'}, 
#         {'words': '核对、发药药 师：'}
#     ], 
#         'words_result_num': 55, 
#         'log_id': 1922617180959352236
# }

with open('demo.json', 'r', encoding = 'utf-8') as f:
    demo = f.read()
    medicine_db = helper.ernie_response(
        f"请根据处方OCR结果提取有效信息生成json，格式为{demo}，处方OCR结果为{result}，注意用量部分可能需要计算和语序调整，例如：处方中显示规格50mg*6，用量为每次50mg每日三次，你需要换算为每日三次每次一颗",
        []
    )
    # print(medicine_db)

    medicine_db_lines = medicine_db.splitlines()
    if len(medicine_db_lines) > 2 and medicine_db_lines[0].strip().startswith("```") and medicine_db_lines[-1].strip() == "```":
        medicine_db_json_str = "\n".join(medicine_db_lines[1:-1])
    else:
        medicine_db_json_str = medicine_db 

    with open('medicine_db.json', 'w+', encoding = 'utf-8') as f:
        f.write(medicine_db_json_str)
        