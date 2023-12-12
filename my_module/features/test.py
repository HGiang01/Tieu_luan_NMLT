import os
import pandas as pd
from datetime import datetime, date
# from my_module.features import choose_list


from time import sleep

# Hàm với hai đối số count : số dấu chấm; step : khoảng thời gian hiển thị giữa các chấm
def loading_mess(count : int, step : int, mess = "Đang tải") :
    print(mess , end="", flush=True)
    for item in range(count) :
        sleep(step)
        if item == count - 1 :
            print(".")
            break
        print(".", end="", flush=True)



def choose_list(mess, list_item, get_input = True):
    while True:
        print(f"{mess}")
        for i in range(len(list_item)):
            print(f"{i}. {list_item[i]}")
        if get_input != True: break
        i = input("-> ")
        try:
            if (list_item[int(i)] in list_item):
                return list_item[int(i)]
        except:
            print("Lựa chọn không phù hợp")

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
    print("Không có thông báo mới trong 7 ngày qua.")
    
    while True:
        option = choose_list("Chọn lớp: ", subject_list_class + ["Quay lại"], True)
        if option == "Quay lại": break
        print(no_list.iloc[:,1:-2].loc[no_list.Class == option].reset_index(drop = True))
        loading_mess(3,1,"")



mssv = 22166106
score_folder_path = r"C:\Users\Admin\Desktop\python\TL\TLGiang\score"
get_notify(get_core(mssv, score_folder_path, False))