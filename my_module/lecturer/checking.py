from my_module.features import loading_mess
import pandas as pd
import numpy as np

def lecturer_checking(data_path, lecturer_col_name : str,password_col_name : str) :
    data = pd.read_excel(data_path)
    count = 0
    while count < 3 :
        lecturer_id = input("Mã giảng viên: ")
        password_input = input("Mật khẩu: ")
        for id, password in zip(data[lecturer_col_name], data[password_col_name]) :
            if lecturer_id == str(id) and password_input == str(password) :
                print("Đăng nhập thành công\n")
                return lecturer_id
        print("Tài khoản hoặc mật khẩu không chính xác")
                    
        count += 1
        if (count != 3) :
            print(f"Còn {3 - count} lần nhập")
            loading_mess(3, 1, mess="Chờ 3 giây để đăng nhập lại")
            print('\n')
            continue
        else :
            print("Đã nhập sai 3 lần\n")

        #NHẬP MÃ CAPCHA ĐỂ RESET MẬT KHẨU
        isSuccess = True
        while isSuccess :
            name_input_capcha = input("Nhập tên tài khoản đặt lại mật khẩu:\n-> ")
            for name in data[lecturer_col_name] :
                if name_input_capcha == str(name) :
                    isSuccess = False
                    print('\n')
            if isSuccess :
                print("Lỗi: Không tìm thấy tài khoản\n")
    
    while True :
        capcha_code = capcha()
        capcha_input = input(f"Nhập mã capcha để đặt lại mật khẩu: {capcha_code}\n-> ")

        if (capcha_input == capcha_code) :
            #Thay đổi mật khẩu
            repass = input("Vui lòng nhập mật khẩu mới:\n-> ")
            #Tìm ra vị trí thay đổi mật khẩu dựa trên mssv
            for name_lecturer, idx in zip(data[lecturer_col_name], range(0, len(data[lecturer_col_name]))) :
                if name_input_capcha == str(name_lecturer) :
                    try :
                        data.loc[idx, password_col_name] = repass
                        loading_mess(3, 1, mess="Đang thiết lập lại mật khẩu")
                        break
                    #Nếu cột dữ liệu chuyển đổi không phù hợp kiểu dữ liệu với nhau
                    except :
                        data[password_col_name].astype(object)
                        data.loc[idx, password_col_name] = repass
                        loading_mess(3, 1, mess="Đang thiết lập lại mật khẩu")
                        break
            break
        print("Sai capcha\n")
    #Lưu lại thay đổi
    data.to_excel(data_path, index=False)
    return 'datlaimatkhau'
    

def capcha(size = 5) -> str:
    #Tạo mảng dec của kí tự thường, hoa và số trong acsii
    slower_char_code_in_ascii = [i for i in range(97, 123)]
    upper_char_code_in_ascii = [i for i in range(65, 91)]
    num_code_in_ascii = [i for i in range(48, 58)]

    data = slower_char_code_in_ascii + upper_char_code_in_ascii + num_code_in_ascii
    
    capcha_str = list()
    for item in range(0, size) :
        #Chọn ra số ngẫu nhiên trong mảng để chuyển đổi từ ascii sang thường
        char = chr(np.random.choice(data))
        capcha_str.append(char)
    
    return ''.join(capcha_str)