from my_module.features import loading_mess
import pandas as pd
import numpy as np


def student_checking(data_path, mssv_col_name : str,password_col_name : str) :
    data = pd.read_excel(data_path, sheet_name=None)
    count = 0
    while count < 3 :
        mssv_input = input("MSSV: ")
        password_input = input("Mật khẩu: ")

        for sheet in list(data.keys()) :
            for mssv, password in zip(data[sheet][mssv_col_name], data[sheet][password_col_name]) :
                if mssv_input == str(mssv) and password_input == str(password) :
                    print("Đăng nhập thành công\n")
                    return mssv_input
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
            mssv_input_capcha = input("Nhập tên tài khoản đặt lại mật khẩu:\n-> ")
            for sheet in list(data.keys()) :
                for mssv in data[sheet][mssv_col_name] :
                    if mssv_input_capcha == str(mssv) :
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
            for sheet in list(data.keys()) :
                #Tìm ra vị trí thay đổi mật khẩu dựa trên mssv
                for mssv, idx in zip(data[sheet][mssv_col_name], range(0, len(data[sheet][mssv_col_name]))) :
                    if mssv_input_capcha == str(mssv) :
                        try :
                            data[sheet].loc[idx, password_col_name] = repass
                            loading_mess(3, 1, mess="Đang thiết lập lại mật khẩu")
                        #Nếu cột dữ liệu chuyển đổi không phù hợp kiểu dữ liệu với nhau
                        except :
                            data[sheet][password_col_name].astype(object)
                            data[sheet].loc[idx, password_col_name] = repass
                            loading_mess(3, 1, mess="Đang thiết lập lại mật khẩu")
                            break
            break
        print("Sai capcha\n")
    #Lưu lại thay đổi
    with pd.ExcelWriter(data_path, engine='openpyxl') as writer:
        for sheet, value in data.items() :
            value.to_excel(writer, sheet_name=sheet, index=False)
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

