import pandas as pd
# import openpyxl
from my_module.student import student_checking, get_core, get_core0, get_core1
from my_module.lecturer import lecturer_checking, get_report
from my_module.features import back_step#, up_book

lecturer_data = pd.read_excel(r'C:\Users\Admin\Desktop\python\TL\TLGiang\account\lecturer.xlsx')
student_data = pd.read_excel(r'C:\Users\Admin\Desktop\python\TL\TLGiang\account\student.xlsx')
score_data = r"C:\Users\Admin\Desktop\python\TL\TLGiang\score"

#Chọn giao diện
while True :
    define = input("Bạn là\n(0) Sinh viên\n(1) Giảng viên\n-> ")
    if define == "0" :
        print('\n')
        mssv = student_checking(student_data, "MSSV", "Mật khẩu")
        break
    elif define == "1" :
        print('\n')
        lecturer_id = lecturer_checking(lecturer_data, "Mã giảng viên", "Mật khẩu")
        break
    
    print("Lỗi: Giá trị nhập khác 0 và 1")

def student() :
    while True:
        print("Tính năng:")
        option = input("(0) Xem điểm\n(1) Phản hồi\n(2) Tài liệu\n-> ")
        if (option == "0"):
            print('\n')
            get_core0(get_core(mssv, score_data)) #chạy get_core0 với các biến get_core trả về
            back_step(student)
            break

        elif (option == "1") :
            print('\n')
            get_core1(get_core(mssv, score_data))
            # back_step(student)
            break            
        
        elif (option == "2") :
            print('\n')
            pass

        print("Lỗi: Giá trị nhập không phù hợp")

def lecturer() :
    while True:
        print(f"\nTài khoản: {lecturer_id}\nTính năng:")
        option = input("(0) Lập đồ thị\n(1) Xem phản hồi\n(2) Tài liệu\n(3) Đóng chương trình\n -> ")
        if (option == "0") :
            print('\n')
            print("option 0")
            back_step(lecturer)
            break

        elif (option == "1") :
            print('\n') 
            get_report(lecturer_id, score_data, lecturer_data)
            lecturer()
            break
        
        elif (option == "2") :
            print('\n')
            #Sử dụng tài liệu file client_secrets.json và mycreds.txt để xác thực và cấp quyền cho tải file
            # up_book()
            back_step(lecturer)
            break
        
        elif (option == "3") :
            print('\n')
            back_step(lecturer)
            break

        print("Lỗi: Giá trị nhập không phù hợp")


match define :
    case "0" :
        student()
    case "1" :
        lecturer()