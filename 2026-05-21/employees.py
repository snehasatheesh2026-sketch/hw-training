import pandas as pd

df = pd.read_csv("companyDB.Employees.csv")


print(f"missing vales: {df.isna().sum()}")

print(f"total missing values in the dataset {df.isna().sum().sum()}")

print(f"data type of the field{df.dtypes}")

print(df.info)


#-----------------------------------------

print(df.head() ) # first 5 rows


print(df.tail()) # last 5 rows

print(df.describe())

print(df[df.duplicated()] )


#----------------------------------------

for i in df.columns.tolist():      # checkinh colums have duplicates   aa

    counts = df[i].value_counts()     

    for value, count in counts.items():

        if count >= 2:                   # and if have duplicates its writting into a txt file 
          file = open("duplicate.txt", "a")
          file.write(f"\n{i} --> {value} repeated {count} timesn")
    else:
       file = open("duplicate.txt", "a")
       file.write(f"\n{i}  -- not have repeating value" )





#--------------------------------------------------

df.to_csv("output.csv", index=False)


import pandas as pd           # csv converting into xml

df = pd.read_csv("output.csv")

xml_data = df.to_xml(
    root_name="employees",
    row_name="employee",
    index=False
)

with open("employees.xml", "w") as f:
    f.write(xml_data)

print("CSV converted to XML")
