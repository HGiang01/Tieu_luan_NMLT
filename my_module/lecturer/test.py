import os
import pandas as pd

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


def get_notify(get):
    mssv, score_folder_path, subject_list, option, subject_list_class = get
    notify_list = list()
    for x, y in zip(subject_list, subject_list_class):
        notify_list.append(pd.read_excel(score_folder_path + f"\\{x}" + f"\\report.xlsx", sheet_name=y))
    print(notify_list)
get_notify(get_core("22166106", r"C:\Users\Admin\Desktop\python\TL\TLGiang\score", False))