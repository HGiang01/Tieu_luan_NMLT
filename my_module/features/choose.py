def choose_list(mess, list_item, get_input = True):
    while True:
        print(f"{mess}")
        for i in range(len(list_item)):
            print(f"({i}) {list_item[i]}")
        if get_input != True: break
        i = input("-> ")
        try:
            if (list_item[int(i)] in list_item):
                return list_item[int(i)]
        except:
            print("Lựa chọn không phù hợp")