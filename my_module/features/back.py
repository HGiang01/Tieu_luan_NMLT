def back_step(*args, name_function, mess) :
    #Quay lại với lựa chọn
    while True:
        option = input(f"{mess}:\n(0) Không\n(1) Có\n-> ")
        if (option == "0") :
            break
        elif (option == "1") :
            print('\n')
            return name_function(*args)
        print("Lựa chọn không phù hợp")