import os
import pandas as pd
from datetime import datetime
from my_module.features import loading_mess, export_ex, choose_list

# tách ra để sử dụng nhiều lần không cần phải code lại
def get_core(mssv, score_folder_path, get_input = True) :
    subject_list = os.listdir(score_folder_path)
    subject_list_study, subject_list_class  = list(), list()
    #Lọc ra danh sách môn sinh viên đăng ký
    for index in range(0, len(subject_list)):
        data = pd.read_excel(score_folder_path + f"\\{subject_list[index]}" + f"\\{subject_list[index]}.xlsx", sheet_name=None)
        for sheet in list(data.keys()) :
            if any(data[sheet]["MSSV"] == int(mssv)) :
                subject_list_class.append(sheet)
                subject_list_study.append(subject_list[index])
    option = 0
    if get_input == True:
        print("Chọn môn: ") #**# Khong nhập gì -> Lỗi
        #     link = score_folder_path + f"\\{subject_list[int(option)]}" + f"\\report.xlsx"
        #                                                  ^^^^^^^^^^^
        #     ValueError: invalid literal for int() with base 10: ''
        for index, subject in zip(range(0, len(subject_list_study)), subject_list_study) :
            print(f"({index})", subject)

        while True :
            option = input("-> ")
            #Nếu lựa chọn nằm trong index của subject_list_study thì được xem là phù hợp
            if any(option in str(idx) for idx in range(0, len(subject_list_study))) :
                break
            print("Lựa chọn không phù hợp")
    return mssv, score_folder_path, subject_list_study, option, subject_list_class

#CHỨC NĂNG XEM ĐIỂM
def get_core0(get):
    mssv, score_folder_path, subject_list, option = get[:len(get) - 1] #lấy từ hàm get_core trả về
    #Khi đặt sheet_name=None nghĩa là sẽ đọc tất cả các sheet, và data sẽ trở thành một dict với key:value là sheet_name:value
    data = pd.read_excel(score_folder_path + f"\\{subject_list[int(option)]}" + f"\\{subject_list[int(option)]}.xlsx", sheet_name=None)

    #Tìm trong tất cả sheet, để tìm mssv trùng
    for sheet in list(data.keys()) :
        if any(data[sheet]["MSSV"] == int(mssv)) :
            result = data[sheet][data[sheet]["MSSV"] == int(mssv)]
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

            print("Hệ 10: {0}\nHệ 04: {1}\nTrạng thái: {2}\n".format(round(sum_, 2), four, status))
            break
                
    

    
    
#CHỨC NĂNG PHẢN HỒI
def get_core1(get):
    mssv, score_folder_path, subject_list, option = get[:len(get) - 1]
    #Lấy đường dẫn đến file phản hồi của môn đã chọn
    link = score_folder_path + f"\\{subject_list[int(option)]}" + f"\\report.xlsx"
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
    loi_nhan = input("Lời nhắn: ")
    while True:
        review = input("Bạn có chắc muốn gửi lời nhắn này?\n(0) Gửi\n(1) Chỉnh sửa\n(2)  Quay lại menu Tính năng\n-> ")
        if (review == "0"):
            export_ex(link, "mail",[mssv, loi_nhan])
            print('\n')
            break
        elif (review == "1"):
            loi_nhan = input("Lời nhắn: ")
            continue
        elif (review == "2"):
            print('\n')
            break
        else:
            print("Lựa chọn không phù hợp")

#XEM THÔNG BÁO CỦA GIẢNG VIÊN
def get_notify(get):
    _, score_folder_path, subject_list, _, subject_list_class = get

    no_list = list()
    for x, y in zip(subject_list, subject_list_class):
        df = pd.read_excel(score_folder_path + f"\\{x}" + f"\\report.xlsx", sheet_name=y)
        df.insert(df.shape[1], "Class", y)
        today = datetime.today()
        df["Ngày"] = pd.to_datetime(df['Ngày'])
        df['Today'] = (today - df['Ngày']).dt.days
        df['Ngày'] = df['Ngày'].dt.strftime('%d/%m/%Y')
        
        no_list.append(df)

    no_list = pd.concat(no_list).sort_values(by='Ngày')
    no_list = no_list.assign(STT=list(range(1, len(no_list) + 1)))
    no_new = no_list.loc[no_list.Today < 7]
    no_new = no_new.assign(STT=list(range(1, len(no_new) + 1)))

    print("Thông báo mới:")
    if len(no_new) != 0:
        for i in range(len(no_new)):
            print("{0}. Lớp {1}: {2}. ({3})".format(no_new.iloc[i,0], no_new.iloc[i,4], no_new.iloc[i,2], no_new.iloc[i,1]))
    else:
        print("Không có thông báo mới trong 7 ngày qua.")

    while True:
        option = choose_list("Chọn lớp: ", subject_list_class + ["Quay lại"], True)
        if option == "Quay lại": break
        print(no_list.iloc[:,1:-2].loc[no_list.Class == option].reset_index(drop = True))
        loading_mess(3,1,"")
    

