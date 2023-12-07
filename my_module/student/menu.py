import os
import pandas as pd
import openpyxl
import numpy as np
from datetime import datetime
from my_module.features import loading_mess

# tách ra để sử dụng nhiều lần không cần phải code lại
def get_core(mssv, score_folder_path) :
    subject_list = os.listdir(score_folder_path)
    print("Chọn môn: ")
    for index, subject in zip(range(0, len(subject_list)), subject_list) :
        print(f"({index})", subject)

    while True :
        option = input("-> ")
        #Nếu lựa chọn nằm trong index của subject_list thì được xem là phù hợp
        if any(option in str(idx) for idx in range(0, len(subject_list))) :
            break
        print("Lựa chọn không phù hợp")
    return mssv, score_folder_path, subject_list, option

#CHỨC NĂNG XEM ĐIỂM
def get_core0(get):
    mssv, score_folder_path, subject_list, option = get #lấy từ hàm get_core trả về
    data = pd.read_excel(score_folder_path + f"\\{subject_list[int(option)]}" + f"\\{subject_list[int(option)]}.xlsx")
    result = data[data["MSSV"] == int(mssv)]
    #Tiến hành reset index vì lấy phần từ trong cột sẽ chọn theo index
    #Khi không có drop thì dataframe sẽ thêm một cột là index cũ trước reset
    result = result.reset_index(drop = True)

    print("Giữa kỳ: {0}\nCuối kỳ: {1}\n".format(result["Giữa kỳ"][0], result["Cuối kỳ"][0]))
    #GK: 30% CK: 70%
    sum_ = result["Giữa kỳ"][0]*0.3 + result["Cuối kỳ"][0]*0.7
    if (sum_ >= 8.5) :
        four = "A"
        status = "Đạt"
    elif (sum_ >= 7.4) :
        four = "B"
        status = "Đạt"
    elif (sum_ >= 5.5) :
        four = "C"
        status = "Đạt"
    elif (sum_ >= 4) :
        four = "D"
        status = "Đạt"
    else :
        four = "F"
        status = "Chưa đạt"

    print("Hệ 10: {0}\nHệ 4: {1}\nTrạng thái: {2}\n".format(round(sum_, 2), four, status))
    
#CHỨC NĂNG PHẢN HỒI
def get_core1(get):
    mssv, score_folder_path, subject_list, option = get
    #Lấy đường dẫn đến file phản hồi của môn đã chọn
    link = score_folder_path + f"\\{subject_list[int(option)]}" + f"\\report.xlsx"
    data = pd.read_excel(link)
    # lấy stt mới dựa trên stt cuối cùng (là stt lớn nhất) của file
    stt = int(np.nan_to_num(data["STT"].max()))
    #Not a Number
    # ngày dạng hh:mm dd/mmm/yy
    date_now = datetime.now().strftime('%d-%b-%y')
    time_now = datetime.now().strftime('%H:%M')
    print('\n')

    # chọn ẩn danh
    while True:
        private = input("Bạn có muốn ẩn danh?\n(0) Không\n(1) Có\n-> ")
        if (private == "0"):
            break
        elif (private == "1"):
            mssv = "Ẩn danh"
            break
        print("Lựa chọn không phù hợp")
    print('\n')

    #review lời nhắn và gửi
    while True:
        loi_nhan = input("Lời nhắn: ")
        review = input("Bạn có chắc muốn gửi lời nhắn này?\n(0) Gửi\n(1) Chỉnh sửa\n(2)  Quay lại menu Tính năng\n-> ")
        if (review == "0"):
            wb = openpyxl.load_workbook(link) #mở file
            sheet = wb['Sheet1'] #chọn Sheet
            # Thêm hàng mới 
            sheet.append([stt + 1, time_now, date_now, mssv, loi_nhan])
            wb.save(link) #lưu lại trên file đang thao tác
            loading_mess(3, 1, "Gửi thành công!")
            print('\n')
            break

        elif (review == "1"):
            continue
        elif (review == "2"):
            print('\n')
            break
        else:
            print("Lựa chọn không phù hợp")


