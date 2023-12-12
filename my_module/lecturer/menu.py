import pandas as pd
from my_module.features import loading_mess, export_ex, choose_list


def get_info(lecturer_id, lecturer_data):
    data = pd.read_excel(lecturer_data)
    subject = data[data["Mã giảng viên"] == str(lecturer_id)]
    subject = subject.reset_index(drop = True)
    subject = subject["Bộ môn"][0]
    return subject

def get_report(score, subject):
    read_file = pd.read_excel(score + f"\\{subject}\\report.xlsx", sheet_name = 'mail')
    read_file["Ngày"] = pd.to_datetime(read_file['Ngày'])
    read_file['Ngày'] = read_file['Ngày'].dt.strftime('%d/%m/%Y')

    print("Môn {0}:".format(subject))
    print(read_file.tail(30) if len(read_file) != 0 else "Dữ liệu rỗng!")
    #Dùng tail để hiện thông tin mới nhất, nếu chỉ dùng print(read_file) sẽ hiện như cc khi số lượng dòng quá nhiều
    print(f"Xem chi tiết tại:  {score}\\{subject}\\report.xlsx")    

    while True:
        option = input("\nTính năng:\n(0) Dùng bộ lọc\n(1) Quay lại menu Tính năng\n-> ")
        if (option == "0"):
           
           while True:
            condition = input('Nhập điều kiện để đưa vào hàm "pandas.DataFrame.loc[]".\nVí dụ: read_file.MSSV == "Ân danh" -> ')
            try:
                print(read_file.loc[eval(condition)] if len(read_file.loc[eval(condition)]) != 0 else "Dữ liệu rỗng!")
                #eval() : Biến chuỗi thành dạng biểu thức.
                break
            except:
                print("Nhập sai cú pháp!")
                break

        elif (option == "1") :
            print('\n')
            break
        print("Lỗi: Giá trị nhập không phù hợp")


def notify(lecturer_id, score, subject):
    def write(mess):
        while True:
            w = input(f"{mess}: ")
            if len(w) != 0:
                return w
            print(f"Vui lòng nhập {mess}.")
    link = score + f"\\{subject}\\report.xlsx"
    read_file = pd.read_excel(link, sheet_name = None)
    subject_list = list()
    for sheet in list(read_file.keys()):
        if sheet[0:len(sheet) - 1] == lecturer_id:
            subject_list.append(sheet)

    


    i = choose_list("\nChọn lớp để thông báo:", subject_list)
    title = write("Tiêu đề")
    body = write("Nội dung")

    while True:
        print(f'\nTiêu đề: {title}\nNội dung: {body}')
        option = input("\nBạn có muốn gửi thông báo này:\n(0) Gửi\n(1) Đổi tiêu đề\n(2) Đổi nội dung\n(3) Quay lại\n-> ")
        if option == "0":
            try:
                export_ex(link, i,[title, body])
                break
            except:
                print("Vui lòng đóng file muốn ghi!")
                continue
        elif option == "1":
            title = write("Tiêu đề")
            continue
        elif option == "2":
            body = write("Nội dung")
            continue
        elif option == "3":
            notify(lecturer_id, score, subject)
            break
        print("Lựa chọn không phù hợp")