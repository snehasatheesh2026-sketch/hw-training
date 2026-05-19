inevntory = {
    "apple":150.0,
    "banana": 100.0,
    "milk": 90.5,
    "sugar": 160.0
}

print("items in the store you can choose form it")

for i,j in inevntory.items():

    print(f"{i}---- ${j}")

cart = (input("enter the iteams name here")).split() # user can select iteams

print(f"\ncart")

print(type(inevntory))

print(type(inevntory["apple"]))

print(type(cart))


total_bill = 0

for i in cart:

    if i in inevntory:

        total_bill+=inevntory[i]
    else:

        print(f"Unavailable iteam {i}")

print(f"Total Amount {total_bill}") # total bill is prinitng


# converting into a set to get unique items 

print(f"unique item in the cat{set(cart)}")

categories = {"fruits","dairy","backery"}

print(categories)

print(type(categories))


# adding the one item into inventory with price =None

inevntory["kurkure"] =None

print(inevntory["kurkure"])

print(type(inevntory["kurkure"]))


if total_bill >100:

    is_discount_applied = True
else:
    is_discount_applied = False

print("discount ", is_discount_applied)

print(type(is_discount_applied))





