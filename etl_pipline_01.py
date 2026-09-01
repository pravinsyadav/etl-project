import csv               # whenever we are dealing with csv files we need to import csv to read and write files


#function for calculate total 
def cal_total(price, quantity):

    try:
        price = float(price)
        quantity = int(quantity)

        total = price * quantity
        return total
    
    except ValueError:
        return None



# following with open will open transaction file in reading mode 
with open("transaction.csv", "r") as file:
    reader = csv.DictReader(file)         # this convert each csv row into dictionary

    for row in reader:
        total = cal_total(row['price'], row['quantity'])
        print(row['id'], total)
