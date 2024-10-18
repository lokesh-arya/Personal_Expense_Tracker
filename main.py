import datetime, csv, os

#add transaction
def option1():
    try:
        print("\nAdd Expense")
        amount = int(input("Enter the amount:"))

        category_list = ['Food', 'Transport', 'Entertainment','Others']
        print("Category: ")
        for x in range(len(category_list)):
            print(x+1, ')', category_list[x],end="\n")
    
        category = int(input("Choose category (eg. 1):"))
        category = category_list[category-1]

        date_choice = int(input("Choose date (1. Today/ 2. Specify):"))
        if date_choice == 1:
            date = datetime.date.today()
        else:
            date = input("Enter date (DD/MM/YY):")
            date = datetime.datetime.strptime(date, '%d/%m/%y').date()

        description = input('Write Description (Optional):')
        if not description:
            description = 'N/A'

        transaction = {'amount':amount, 'category':category, 'date':date, 'description': description}
        add_transaction(transaction)
    except:
        print('Error')

# edit transaction
def option2():
    print('\nEdit Expense')
    row_no = int(input('Enter row no that you want to edit:'))
    print(transaction_record[row_no-1])
    amount = int(input("Enter new amount:"))

    category_list = ['Food', 'Transport', 'Entertainment','Others']
    print("Category: ", end='')
    for x in range(len(category_list)):
        print(x+1, ')', category_list[x],end="\n")

    category = int(input("Choose new category (eg. 1):"))
    category = category_list[category-1]

    date_choice = int(input("Choose new date (1. Today/ 2. Specify):"))
    if date_choice == 1:
        date = datetime.date.today()
    else:
        date = input("Enter date (DD/MM/YY):")
        date = datetime.datetime.strptime(date, '%d/%m/%y').date()

    description = input('Write new Description (Optional):')
    if not description:
        description = 'N/A'

    transaction_record[row_no-1] = {'amount':amount, 'category':category, 'date':date, 'description': description}
    save_csv()

# Delete transaction
def option3():
    print('\nDelete Expense')
    row_no = int(input('Enter row no that you want to delete:'))
    print(transaction_record[row_no-1])
    option = input('Do you want to delete this transaction?[y/n]: ')
    if option == 'y':
        del transaction_record[row_no-1]
    save_csv()

#view summary of transaction
def option4():
    print('\nView Summary:')
    print('1) Spending of each category')
    print('2) Total spending')
    print('3) Spending over time')
    option = int(input("What do you want to do?: "))

    food_bill = 0
    transport_bill = 0
    entertainment_bill = 0
    others_bill = 0
    for i in transaction_record:
        if i['category'] == 'Food':
            food_bill += i['amount']
        if i['category'] == 'Transport':
            transport_bill += i['amount']
        if i['category'] == 'Entertainment':
            entertainment_bill += i['amount']
        if i['category'] == 'Others':
            others_bill += i['amount']
    if option == 1:
        print('\nFood: Rs.', food_bill)
        print('Transport: Rs.', transport_bill)
        print('Entertainment: Rs.', entertainment_bill)
        print('Others: Rs.', others_bill)

    if option == 2:
        print("\nTotal Spending: Rs.", food_bill+transport_bill+entertainment_bill+others_bill)

    if option == 3:
        today_bill = 0
        weekly_bill = 0
        monthly_bill = 0

        for i in transaction_record:
            if i['date'] == datetime.date.today():
                today_bill += i['amount']
        
        for i in transaction_record:
            if i['date'].strftime("%V") == datetime.date.today().strftime("%V"):
                weekly_bill += i['amount']
        
        for i in transaction_record:
            if i['date'].month == datetime.date.today().month:
                monthly_bill += i['amount']
        
        print('Spending over Time')
        print('Today Spending: Rs.', today_bill)
        print('This Week Spending: Rs.', weekly_bill)
        print('This Month Spending: Rs.', monthly_bill)

# add transaction at end of file
def add_transaction( transaction):
    transaction_record.append(transaction)
    with open('transaction_record.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=transaction.keys())
        if file.tell()==0: #if file is empty write header row
            writer.writeheader()
        writer.writerow(transaction)

# function for loading record in list in correct format
def load_transaction(filename):
    data = []
    if os.path.exists('transaction_record.csv'):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['amount'] = int(row['amount'])
                row['date'] = datetime.datetime.strptime(row['date'], '%Y-%m-%d')
                data.append(row)
    else:
        return []
    return data

# Update the csv file
def save_csv():
    with open('transaction_record.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=transaction_record[0].keys())
        writer.writeheader()
        writer.writerows(transaction_record)

# load previous trasaction record in list
transaction_record = load_transaction('transaction_record.csv')

# Menu running in loop until user hit exit
while True:
    try:
        print("\nMenu")
        print("1. Add Expense")
        print("2. Edit Expense")
        print("3. Delete Expense")
        print("4. View Summary")
        print("5. Exit")
        option = int(input("What do you want to do?: "))
        if option == 1:
            option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            option4()
        elif option == 5:
            break   # Exit loop - end program
    except Exception as e:
        print(e)
