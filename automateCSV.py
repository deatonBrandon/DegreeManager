#''' Data Log '''#
# 12/31
#
# ---> This is how I will group data in the 'Major' column... * new_df = df.groupby(df["Major"].str[0:7]) *
#
# *** What I know ***
# column dtypes are FUBAR. 'Unactivated' and 'Activation Rate' are both mixes of dtypes when they should be int and float
# --> Must remove the commas and quotes 
# --> --> This brought me to learn :: Data Cleaning
# [SUCCESS!]
#
# dtype conversion successful! Replaced special characters and applied the average to the 3 number columns with a round of 3 decimal places.
# 
# 1/4/2023
# Attempting at further cleaning the grouped data
# Names in 'Major' shouldn't be only the first word
# There has to be a way to group these degrees and keep/create some description for the 'Major' column
#
# 1/11/2024
# [Major Success!]
# Degrees in ['Major'] column are split by degree name and the type/level of degree.
# --> This allows for efficient degree grouping

import pandas as pd

# read values and separate rows in 'Major' that can be grouped based on similar values
def clean_the_data(file):

    degree = pd.read_csv(file, index_col=False) 

    degree = degree.rename(columns = {'Activation Rate': 'Activation_Rate'})

# --> Assign string .splits and .replace functions to data clean and assign variable types
    degree['Activated'] = degree['Activated'].astype(float)
    degree['Unactivated'] = degree['Unactivated'].str.replace(",", "")
    degree['Unactivated'] = degree['Unactivated'].astype(float)
    degree['Activation_Rate'] = degree['Activation_Rate'].str.replace('%', "")
    degree['Activation_Rate'] = degree['Activation_Rate'].astype(float)

    major_splt = degree['Major'].str.split(" ")
    name_col = []
    type_col = []

# --> 'for loop' that separates the degree type & level from the string
    for i in major_splt:
        for x in i:
            num_lvl = x.isdigit()
        if num_lvl:
            type_col.append(''.join(i[-2:]))
            name_col.append(' '.join(i[:-2]))
        elif len(i[-1]) <= 3:
            type_col.append(''.join(i[-1:]))
            name_col.append(' '.join(i[:-1]))
        else:
            type_col.append(None)
            name_col.append(' '.join(i))

    degree['Major'] = name_col
    degree.insert(1, 'Types', type_col)

    new_df = degree.groupby('Major', as_index=False, group_keys=False, sort=False).agg({'Types': 'unique', 'Activated': 'mean', 'Unactivated': 'mean', 'Activation_Rate': 'mean'}).round(2)
    
    new_df.to_csv('Solution.csv', index=False)

def main():
    print("Welcome to the csv reader!")
    while True:
        name = input("Please enter the file name only. There is no case sensitivity: ")
        file_name = name.lower() + ".csv"
        try:
            clean_the_data(file_name)
            print("Success!")
            break
        except FileExistsError:
            print("Error reading this specific file. Please try again.")
            continue
        except FileNotFoundError:
            print("File is not found. Please try again.")
            continue
        except Exception:
            print("Something went wrong. Please try again.")

if __name__ == '__main__':
    main()