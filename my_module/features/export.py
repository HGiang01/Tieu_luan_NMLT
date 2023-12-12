import openpyxl
import pandas as pd
import numpy as np
from datetime import datetime
from my_module.features import loading_mess

def export_ex(link, sheet_ex = "Sheet1", append_list = []):
    data = pd.read_excel(link, sheet_name=sheet_ex)
    # lấy stt mới dựa trên stt cuối cùng (là stt lớn nhất) của file
    stt = int(np.nan_to_num(data["STT"].max()))
    #Not a Number
    # ngày dạng hh:mm dd/mmm/yy
    date_now = datetime.now().strftime('%d-%b-%y')
    wb = openpyxl.load_workbook(link) #mở file
    sheet = wb[sheet_ex] #chọn Sheet
    # Thêm hàng mới 
    sheet.append([stt + 1, date_now] + append_list)
    wb.save(link) #lưu lại trên file đang thao tác
    loading_mess(3, 1, "Gửi thành công!")