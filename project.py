import sqlite3
conn = sqlite3.connect('new.db')
print("Database opened successfully")
def _display_options(all_options,title,type):
    option_num = 1
    option_list = []
    print("\n",title,"\n")
    for option in all_options:
        code = option[0]
        desc = option[1]
        print("{0}.\t{1}".format(code, desc))
        option_list.append(code)
    selected_option = 0
    while selected_option == 0 and type[1]:
        prompt = "Enter the number of the "+type[0]+" you wish to choose: "
        selected_option = int(input(prompt))
        return selected_option

def ADD_NEW_PRODUCT():
    cursor = conn.execute("SELECT category_id,category_description from categories")
    row = cursor.fetchall()
    id_of_selected_option = _display_options(row, title="Product Categories", type=['product category',True])
    t = conn.execute("SELECT category_description from categories where category_id=?", (id_of_selected_option,))
    str = ""
    for i in t:
        str = i[0]

    cursor1 = conn.execute("SELECT product_id, product_description from product where category_id=?",
                           (id_of_selected_option,))
    row = cursor1.fetchall()
    prompt = "Products in the " + str + " category"
    _display_options(row, title=prompt, type=['select category',False])

    product_id = int(input("Enter the product code: "))
    product_description = input("Enter the description: ")
    manufactures = input("Enter the manufacture: ")
    model = input("Enter the product model: ")
    productList = [product_id, product_description, manufactures, model, id_of_selected_option]

    sqlite_insert_with_param = """INSERT INTO Product (product_id,product_description, manufactures, model, category_id, status) \
    VALUES (?, ?, ?, ?, ?, 'Available');"""
    conn.execute(sqlite_insert_with_param, productList)
    conn.commit()

    cursor3 = conn.execute("SELECT seller_id,seller_name from Seller")
    row = cursor3.fetchall()
    id_of_selected_option = _display_options(row, title="seller table", type=['Seller',True])

    data = conn.execute("SELECT seller_name from Seller where seller_id=?",(id_of_selected_option,))
    row = data.fetchall()
    str1 = ''
    for i in row:
        str1 = i[0]
    mylist = [id_of_selected_option,str1,product_id]

    sqlite_new = """INSERT INTO Seller (seller_id,seller_name, product_id) \
        VALUES (?, ?, ?);"""
    conn.execute(sqlite_new, mylist)
    conn.commit()
    print("New product added to the database")

def CHANGE_PRODUCT_STATUS():
    cursor = conn.execute("SELECT category_id,category_description from categories")
    row = cursor.fetchall()
    id_of_selected_option = _display_options(row, title="Product Categories", type=['category', True])
    t = conn.execute("SELECT category_description from categories where category_id=?", (id_of_selected_option,))
    str = ""
    for i in t:
        str = i[0]
    cursor = conn.execute("SELECT product_id, product_description from product where category_id=?",
                           (id_of_selected_option,))
    row = cursor.fetchall()

    prompt = "Products in the " + str + " category"
    id_of_selected_option = _display_options(all_options=row, title=prompt, type=['product', True]),

    cursor = conn.execute("SELECT product_description, status from Product where product_id=?",(id_of_selected_option))
    row = cursor.fetchall()
    str1 = ""
    str2 = ""
    for i in row:
        str1 = i[0]
        str2 = i[1]
    print(str1,str2)
    print('Product {0} is status {1}:'.format(str1,str2))
    status = ['Available', 'Temporarily Unavilable', 'Discontinued']
    emptyList = []
    for i in status:
        if (i != str2):
            emptyList.append(i)
    number = [1, 2]
    for item in emptyList:
        dic = dict(zip(number, emptyList))
    print('\n'.join("{}: {}".format(k, v) for k, v in dic.items()))
    choice = int(input("Enter the number of the status you wish to change the product to: "))

    cursor = conn.execute("UPDATE Product set=(?)",(dic.get(choice),)" where product_id=?",(id_of_selected_option,))
    conn.commit()


def DELETE_PRODUCT():
    cursor = conn.execute("SELECT category_id,category_description from categories ")
    row = cursor.fetchall()
    id_of_selected_option = _display_options(row, title="Product Categories", type=['product category',True])

    cursor1 = conn.execute("SELECT product_id, product_description from Product where category_id=?", (id_of_selected_option,))
    row = cursor1.fetchall()
    id_of_selected_option=_display_options(row, title="Product ", type=['product',True])

    data = conn.execute("SELECT product_description from Product where product_id=?", (id_of_selected_option,))
    row = data.fetchall()
    str = ''
    for i in row:
        str = i[0]

    prompt = " Do you really want to delete the " +str + " (Y or N) :"
    user = input(prompt)

    if user == 'Y':
        conn.execute("DELETE from Product where product_id=?", (id_of_selected_option,))
        conn.execute("DELETE from seller where product_id=?", (id_of_selected_option,))
        conn.commit()
        print("data delete successfully")
    elif user == 'N':
        print("THANK YOU ! VISIT AGAIN.")

if __name__ == '__main__':
    #   LOGIC OR BACKEND OF WORKING 'STUDENT MANAGEMENT SYSTEM'
    print("\n")
    print("\t\t\t\t ' ********** WELCOME TO ORINOCO SHOP ********** ' \n")
    run = True
    while run:
        print("PRESS FROM THE FOLLOWING OPTION : \n")
        print("PRESS 1 : Display all products in a category")
        print("PRESS 2 : Add a new product")
        print("PRESS 3 : Change the status of an existing product")
        print("PRESS 4 : Delete a product ")
        print("PRESS 5 : EXIT ")
        OPTION = int(input("ENTER YOUR OPTION : "))
        print("\n")
        print(end="\n")
        if OPTION == 1:
            cursor = conn.execute("SELECT category_id,category_description from categories")
            row = cursor.fetchall()
            id_of_selected_option = _display_options(row, title="Product Categories", type=['category',True])
            t = conn.execute("SELECT category_description from categories where category_id=?",(id_of_selected_option,))
            str = ""
            for i in t:
                str = i[0]
            cursor3 = conn.execute("SELECT product_id, product_description from product where category_id=?",(id_of_selected_option,))
            row=cursor3.fetchall()

            prompt = "Products in the "+str+" category"
            _display_options(all_options=row,title=prompt,type=['',False]),

        elif OPTION == 2:
            ADD_NEW_PRODUCT()
        elif OPTION == 3:
            CHANGE_PRODUCT_STATUS()
        elif OPTION == 4:
            DELETE_PRODUCT()
        elif OPTION == 5:
            print("THANK YOU ! VISIT AGAIN.")
            run = False
        else:
            print("PLEASE CHOOSE CORRECT OPTION FROM THE FOLLOWING.")
            print("\n")
conn.close()

