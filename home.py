import pandas as pd
from my_module.student import student_checking, get_core, get_core0, get_core1, get_notify
from my_module.lecturer import lecturer_checking, get_info, get_report, notify
from my_module.features import back_step, loading_mess

lecturer_data_path = r'C:\Users\Admin\Desktop\python\TL\TLGiang\account\lecturer.xlsx'
student_data_path = r'C:\Users\Admin\Desktop\python\TL\TLGiang\account\student.xlsx'
score_data = r"C:\Users\Admin\Desktop\python\TL\TLGiang\score"

#Chọn giao diện
while True :
    define = input("Bạn là\n(0) Sinh viên\n(1) Giảng viên\n-> ")
    if define == "0" :
        print('\n')
        mssv = student_checking(student_data_path, "MSSV", "Mật khẩu")
        if (mssv == "datlaimatkhau") :
            print('\n')
            mssv = student_checking(student_data_path, "MSSV", "Mật khẩu")
        break
    elif define == "1" :
        print('\n')
        lecturer_id = lecturer_checking(lecturer_data_path, "Mã giảng viên", "Mật khẩu")
        if (lecturer_id == "datlaimatkhau") :
            print('\n')
            lecturer_id = lecturer_checking(lecturer_data_path, "Mã giảng viên", "Mật khẩu")
        break
    
    print("Lỗi: Giá trị nhập khác 0 và 1")

def student() :
    while True:
        print(f"\nTài khoản: {mssv}\nTính năng:")
        option = input("(0) Xem điểm\n(1) Phản hồi\n(2) Xem thông báo\n(3) Tài liệu\n(4) Thoát\n-> ")
        if (option == "0"):
            print('\n')
            get_core0(get_core(mssv, score_data)) #chạy get_core0 với các biến get_core trả về
            back_step(name_function=student, mess="Quay lại")
            break

        elif (option == "1") :
            print('\n')
            get_core1(get_core(mssv, score_data))
            back_step(name_function=student, mess="Quay lại")
            break            

        elif (option == "2") :
            print('\n')
            get_notify(get_core(mssv, score_data, False))
            back_step(name_function=student, mess="Quay lại")
            break            
        
        elif (option == "3") :
            print('\nTruy cập đường dẫn dưới đây:\n-> https://drive.google.com/drive/u/0/folders/1AP1E0aOiem_1WkJriombjLfZyaLuiq9b')
            print('\n')
            back_step(name_function=student, mess="Quay lại")
            break

        elif (option == "4") :
            print('\nChương trình kết thúc')
            break

        print("Lỗi: Giá trị nhập không phù hợp")

def lecturer() :
    while True:
        print(f"\nTài khoản: {lecturer_id}\nTính năng:")
        option = input("(0) Lập đồ thị\n(1) Xem phản hồi\n(2) Thông báo\n(3) Tài liệu\n(4) Thoát\n -> ")
        if (option == "0") :
            print('\n')
            print("option 0")
            back_step(name_function=lecturer, mess="Quay lại")
            break

        elif (option == "1") :
            print('\n')
            get_report(score_data, get_info(lecturer_id, lecturer_data_path))
            back_step(name_function=lecturer, mess="Quay lại")
            break
        elif (option == "2") :
            print('\n')
            notify(lecturer_id, score_data, get_info(lecturer_id, lecturer_data_path))
            back_step(name_function=lecturer, mess="Quay lại")
            break
        elif (option == "3") :
            print('\n')
            #Sử dụng tài liệu file client_secrets.json và mycreds.txt để xác thực và cấp quyền cho tải file
            # up_book()
            back_step(name_function=lecturer, mess="Quay lại")
            break
        
        elif (option == "4") :
            print('\nChương trình kết thúc')
            break

        print("Lỗi: Giá trị nhập không phù hợp")


match define :
    case "0" :
        student()
    case "1" :
        lecturer()