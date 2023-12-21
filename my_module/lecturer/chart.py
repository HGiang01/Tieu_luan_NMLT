from my_module.lecturer.menu import *
from my_module.features.back import back_step
#### MAIN--------------------------------------------------------------------------------------------
def get_chart(id, lecturer_data_path, score_path):
### Chọn Môn
    #(đã sửa)
    xlsx_path,subject, class_sheet = pick_subject(id, lecturer_data_path, score_path) #Chọn môn
    ### CHỌN Đối tượng
    while True:
        plot_op = plot_option()
    ### 1 Đối tượng
        if plot_op == '0':
            num_class = pick_class(class_sheet)
            class_ = class_sheet[num_class]
            one_object(class_,subject,xlsx_path,class_sheet)
            break
    ###Tổng quan --------------------------------------------------------------------------------------------
        elif plot_op == '1':
            summary(xlsx_path = xlsx_path,
                    subject = subject,
                    class_sheet = class_sheet)
            break
        else:
            print("Chỉ nhập số trong khoảng cho trước")

