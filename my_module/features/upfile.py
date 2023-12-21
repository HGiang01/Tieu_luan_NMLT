from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

#TOKEN: là một đoạn mã chứa thông tin xác thực và ủy quyền cung cấp cho một ứng dụng.

#Tạo một đối tượng google để xác thực tài khoản
gauth = GoogleAuth()
#Mở và đọc thông tin xác thực từ file 'mycreds.txt' nếu file k tồn tại thì trả về None
gauth.LoadCredentialsFile("mycreds.txt")

if gauth.credentials is None:
    #Mở máy chủ web cục bộ yêu cầu đăng nhập và cấp quyền
    gauth.LocalWebserverAuth()
#Kiểm tra access_token 
elif gauth.access_token_expired:
    # Nếu token hết hạn thì tiến hành làm mới
    gauth.Refresh()
else:
    #Tiến hành cấp quyền để truy cập vào gg drive
    gauth.Authorize()
#Tiến hành lưu thông tin xác thực vào file 'mycreds.txt'
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

def up_book() :
    #Nhập đường dẫn đến file cần gửi lên
    path = input("Nhập đường dẫn đến file:\n-> ")
    #Kiểm tra đường dẫn có tồn tại hay không
    if not os.path.exists(path):
        print('Lỗi: Đường dẫn không tồn tại\n')
        up_book()
    #Kiểm tra đường dẫn có trỏ đền file hay không
    elif not os.path.isfile(path):
        print('Lỗi: Đường dẫn phải trỏ đến file không phải folder\n')
        up_book()

    #Đặt tên file
    while True :
        rename_op = input("Đặt lại tên file\n(0) Có\n(1) Không\n-> ")
        if (rename_op == "0") :
            name = input("Nhập tên\n-> ")
            #Đảo ngược đường dẫn lấy phần định dạng file
            rename = path[::-1]
            rename = rename[: rename.index(".") + 1]
            rename = rename[::-1]
            #Ghép phần tên mới và phần định dạng
            rename = name + rename
            break
        elif (rename_op == "1") :
            #Đảo ngược đường dẫn lấy phần tên file
            rename = path[::-1]
            rename = rename[:rename.index("\\")]
            rename = rename[::-1]   
            break
        print("Lỗi: Lựa chọn không phù hợp")
    
    file = drive.CreateFile({'title': rename, 'parents': [{'id': '1AP1E0aOiem_1WkJriombjLfZyaLuiq9b'}]})
    file.SetContentFile(path)
    file.Upload()
    print('\n')