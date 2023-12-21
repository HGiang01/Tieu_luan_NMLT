import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
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
    #Dùng tail để hiện thông tin mới nhất, nếu chỉ dùng print(read_file) sẽ không thể hiện tổng quát khi số lượng dòng quá nhiều

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
        option = input("\nBạn có muốn gửi thông báo này:\n(0) Gửi\n(1) Đổi tiêu đề\n(2) Đổi nội dung\n-> ")
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
        print("Lựa chọn không phù hợp")

#ĐỒ THỊ
## ------------------------------------------------------CHỌN MÔN-----------------------------------------------------------
def pick_subject(id, lecturer_data_path, score_path) :
    score_folder_path = score_path
    data = pd.read_excel(lecturer_data_path)
    subject = data[data["Mã giảng viên"] == id]
    subject = subject.reset_index(drop = True)
    subject_list = subject["Bộ môn"].to_list()
    while True:
        try:
            print('Chọn môn:')
            for idx, sub in zip(range(len(subject_list)), subject_list):
                print(f'({idx}) {sub}')
            option = int(input('-> '))
            if option in range(len(subject_list)):
                break
            else:
                print('Lỗi: Lựa chọn không phù hợp')
        except:
            print("Lỗi: Sai định dạng ")
        # đường dẫn tới file excel sau khi chọn môn
    xlsx_path = score_folder_path + f"\\{subject_list[int(option)]}" + f"\\{subject_list[int(option)]}.xlsx"
    # gán biến tên môn
    subject_list = subject_list[option]
    # gọi ra tên của tất cả các lớp học có trong file
    class_sheet = pd.ExcelFile(xlsx_path).sheet_names
    # trả về đường dẫn file excel, môn học, list lớp
    return  xlsx_path, subject_list, class_sheet

def final_score(xlsx_path,class_sheet, class_=any , _class_ = any):         # _class_ : số tương ứng với lớp
# lấy điểm giữa kỳ, cuối kỳ, tên 2 học kỳ từ hàm colum_data
    if class_ == any:
        # biến tên lớp
        class_ = class_sheet[_class_]
    data_mid_sem_1 , data_end_sem_1 , colum_name1 ,\
    colum_name2 = colum_data2_1c(xlsx_path,class_)
    data_ = []
    for i in range(len(data_mid_sem_1)):
        data_.append(data_mid_sem_1[i]*0.3 + data_end_sem_1[i]*0.7)
    return data_,data_mid_sem_1 , data_end_sem_1 , colum_name1 ,colum_name2

def plot_option():
    print('Đối tượng vẽ:\n(0) Một đối tượng\n(1) Tổng quan')
    while True:
        option = input('-> ')
        if any([option in i for i in ['0', '1']]):
            break
        print('Lỗi: lựa chọn không phù hợp')
    return option

## CHỌN LỚP
def pick_class(class_sheet):
    while True:
        print("Chọn lớp: ")
        for i in range(len(class_sheet)):
             print((f"({i}) {class_sheet[i]}"))
        num_class = input("-> ")
        if any(num_class in str(i) for i in range(len(class_sheet))):
            break
        print('Lỗi: lựa chọn không phù hợp')
    return int(num_class)

###------------------------------------------- CÁC HÀM LẤY VÀ TÍNH DỮ LIỆU CHO CHART--------------------------------------

##----------------------------------------------------- LẤY DỮ LIỆU 1 colum---------------------------------------

# 1 sheet 1 colum
def colum_data1_1c(xlsx_path,colum_name,class_):
    data_excel = pd.read_excel(xlsx_path,class_)
    data_score = data_excel[colum_name].tolist()
    return data_score

## -----------------------------------------------------LẤY DỮ LIỆU 2 colums---------------------------------------
# 1 sheet 2 colums
def colum_data2_1c(xlsx_path,class_):
# class_: biến tên lớp 
        colum_name1 = "Giữa kỳ"
        colum_name2 = "Cuối kỳ"
        data_excel = pd.read_excel(xlsx_path,class_)
        data_sem_1 = data_excel[colum_name1].tolist()
        data_sem_2 = data_excel[colum_name2].tolist()
        return data_sem_1 , data_sem_2 , colum_name1 , colum_name2

## ------------------------------------------Đếm theo khoảng điểm cho 1 học kỳ------------------------------------------
def range_data1(data_score,bin): 

    # đếm số phần tử thõa mãn khoảng 10 khoảng cách đều từ 0 - 10 
    range_ , bins = np.histogram(data_score,bin)
    return range_, bins
## Đếm theo khoảng điểm cho 2 học kỳ 
def range_data2(data_range_1 , data_range_2): 
    # đếm số phần tử thõa mãn khoảng 5 khoảng cách đều từ 0 - 10 ( 0 - 2.5 - 5 - 7.5 - 10)
    range_1 , binss1 = np.histogram(data_range_1,np.linspace(0,10,11))
    range_2 , binss2 = np.histogram(data_range_2,np.linspace(0,10,11))
    return range_1, binss1, range_2 , binss2

### ---------------------------HÀM TỔNG CHO 1 ĐỐI TƯỢNG
def one_object(class_,subject,xlsx_path,class_sheet):
    data_,data_mid_sem_1 , data_end_sem_1 , colum_name1 ,colum_name2\
    = final_score(xlsx_path,class_sheet, class_ = class_)
    bin = [0 ,4 ,5.5 ,7.4 ,8.5 ,10]
    range_, bins = range_data1(data_,bin)
    range_1, binss1, range_2 , binss2 = range_data2(data_mid_sem_1 , data_end_sem_1)
    one_obj_chart(subject,class_, range_, bins, range_1, binss1, range_2 , binss2, colum_name1 , colum_name2)

def one_obj_chart(subject,class_, range_, bins, range_1, binss1, range_2 , binss2, colum_name1 , colum_name2):
    plt.style.use ('seaborn-v0_8-whitegrid')
    fig, (ax1,ax2) = plt.subplots(ncols = 2 ,nrows = 1)
    colors = ["#ED7D31", "#FFC000", "#4472C4", "#5B9BD5", "#A5A5A5"]
    fig.suptitle(f"Môn: {subject} \nLớp: {class_}", 
                    ha = 'center', va = "top",
                    fontsize = 20, fontweight = 'bold'
                    )
    # range_ : dữ liệu điểm học kỳ
    # binss : khoảng lấy dữ liệu
    # colum_name: tên học kỳ
    # size : dữ liệu điểm sau khi lọc bỏ các phần tử = 0
    # labels_ : khoảng tương ứng với size 

    # tính điểm tổng kết 2 học kỳ
    # sắp xếp data_ theo khoảng từ 0-10 steps = 1

    # loại bỏ các khoảng không có phần tử xuất hiện
    size_pie = [valu for valu in range_ if valu !=0]
    labels_pie = []
    for i in range(len(range_)):
        if range_[i] != 0:
            labels_pie.append(f"{bins[i]} - {bins[i+1]}")
    
    sticks_bar_1 = np.linspace(1,10,10)
    sticks_bar_2 = sticks_bar_1+0.4

## subplot 1 __ Pie 
    ax1.pie(size_pie,colors = colors, autopct='%1.1f%%', counterclock=False, startangle=90)
    
    ax1.set_title(f"Điểm trung bình học kỳ",
        fontsize = 14, fontweight = "bold", 
        color = "gray" )
    ax1.legend(labels_pie,
                title = "Khoảng điểm",
                loc = "upper right",
                bbox_to_anchor=(1.15, 0.9),
                frameon=True
                )
    
## subplot 2 __ bar
    bar_width = 0.4
    ax2.bar(sticks_bar_1, range_1, width = bar_width, label = "Giữa kỳ")
    ax2.bar(sticks_bar_2, range_2 , width = bar_width, label = "Cuối kỳ")
    ax2.set_xticks(sticks_bar_1 + bar_width / 2, labels = sticks_bar_1)
    ax2.set_xlabel('Khoảng điểm',
                    fontsize = 14,
                    color = "gray")
    ax2.set_ylabel ( "Số lượng",
                    fontsize = 14,
                    color = "gray")
    
    ax2.legend(title = "Điểm",
                loc = "upper left",
                frameon=True);

    # Tự động điều chỉ kích thước để tránh trùng lắp
    plt.tight_layout()
    plt.show();

def summary(xlsx_path,subject, class_sheet):
    plt.style.use ('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots()
    fig.suptitle(f"Thống kê điểm tổng kết môn {subject}",
                    ha = 'center', va = 'top',
                    fontsize = 20, fontweight = 'bold',
                    )
    ## _class_ : Số tương ứng vs lớp

    for _class_ in range(len(class_sheet)) :
    # tính điểm tổng kết 2 học kỳ
        data_,data_mid_sem_1 , data_end_sem_1 , colum_name1 ,colum_name2\
              = final_score(xlsx_path, class_sheet, _class_ = _class_)
    # sắp xếp data_ theo khoảng từ 0-10 steps = 1
        bin = [0 ,4 ,5.5 ,7.4 ,8.5 ,10]
        range_, bins = range_data1(data_,bin)
        
    # loại bỏ các giá khoảng có không có phần tử xuất hiện
        size = [valu for valu in range_ if valu !=0]
        
        labels =[]
        for i in range(len(range_)):
            if range_[i] != 0:
                labels.append(bins[i])
        # ax.set_xticklabels([str(value) for value in bins])
        ax.plot(labels,size,label = class_sheet[_class_], marker='o',markersize = 5);
    
    ax.set_xlabel ("Điểm", fontsize = 14, fontweight = "bold", color = "gray" ) 
    ax.set_ylabel ("Số lượng", fontsize = 14, fontweight = "bold", color = "gray")
    ax.set_xticks(bin, labels = bin)
    fig.legend(class_sheet,
                    title = "Lớp",
                    loc = "center right",
                    frameon = True
                    )
    plt.show()
    print('\n')    