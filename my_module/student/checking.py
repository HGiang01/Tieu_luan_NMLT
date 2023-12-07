from my_module.features import loading_mess
import pandas as pd


def student_checking(data_path, mssv_col_name : str,password_col_name : str) :
    while True :
        mssv_input = input("MSSV: ")
        password_input = input("Mật khẩu: ")
        data = pd.read_excel(data_path, sheet_name=None)
        for sheet in list(data.keys()) :
            for mssv, password in zip(data[sheet][mssv_col_name], data[sheet][password_col_name]) :
                if mssv_input == str(mssv) and password_input == str(password) :
                    print("Đăng nhập thành công\n")
                    return mssv_input
        print("Tài khoản hoặc mật khẩu không chính xác")

        loading_mess(3, 1)