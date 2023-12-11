def choose_list(mess, list_item):
    while True:
        print(f"{mess}")
        for i in range(len(list_item)):
            print(f"{i}. {list_item[i]}")
        i = input("-> ")
        try:
            if (list_item[int(i)] in list_item):
                return i
        except:
            print("Lựa chọn không phù hợp")