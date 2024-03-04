import pandas as pd
import sys

def extract_class_list(insendi_file, class_name):
    class_list = pd.read_csv(insendi_file)
    extract = class_list.loc[class_list['group_name'] == class_name, ['given_name', 'family_name']]
    class_list = extract[['given_name', 'family_name']]
    class_list['Students'] = extract['given_name'] + " " + extract['family_name']
    class_list.drop(['given_name', 'family_name'], axis=1, inplace=True)
    temp = '_'.join(class_name.split(' '))
    class_list.to_csv(f"./class_lists/{temp}_list.csv", index=False)
    return class_list
        
def load_data(insendi_file, class_list):
    analytics = pd.read_csv(insendi_file)
    file_extension = class_list.split('.')[-1]
    
    if file_extension == 'txt' or file_extension == 'csv':
        classList = pd.read_csv(f"{class_list}", header=None, names=['Students'])
    elif file_extension == 'xlsx':
        classList = pd.read_excel(f"{class_list}", header=None, names=['Students'])
    else:
        sys.exit("Class list file format must be txt, csv, or xlsx")
    return analytics, classList

def extract_sections(analytics):
    section = str(input("Do you want extract for certain sections? (y/n): \n"))
    if section == 'y':
        day = str(input("\nEnter day(s) that you want to extract (e.g. 1,5 means day 1 to day 5): \n"))
        if len(day) == 1:
            m, n = int(day), int(day)
        elif len(day) == 3:
            m, n = map(int, day.split(','))
        else:
            sys.exit("Input must be 2 digits seperated by commas or 1 digit")
        
        columns_extract = [column for column in analytics.columns[5:-1] if int(column.split('.')[0]) in range(m, n+1)]
        columns_extract_reversed = columns_extract[::-1]
        columns_extract_reversed.append(analytics.columns[2])
        columns_extract = columns_extract_reversed[::-1]
    
    elif section == 'n':
        columns_extract = [column for column in analytics.columns[5:-1]]
        columns_extract_reversed = columns_extract[::-1]
        columns_extract_reversed.append(analytics.columns[2])
        columns_extract = columns_extract_reversed[::-1]
        columns_extract.append(analytics.columns[-1])
    
    else:
        sys.exit("Input must be y or n")
        
    return columns_extract

def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python [analytics.py] [insendi csv file] [class_name]")
    
    user = str(input("Do you have a class list? (y/n): \n"))
    if user == 'y':
        insendi_file = sys.argv[1]
        temp = sys.argv[2]
        class_list = f"./class_lists/{temp}_list.csv"
        
    elif user == 'n':
        insendi_file_list = str(input("\nEnter insendi list csv file name without .csv: \n"))
        class_ = sys.argv[2]
        class_name = " ".join(class_.split('_'))
        extract_class_list(f"./class_lists/{insendi_file_list}.csv", class_name)
        temp = '_'.join(class_name.split(' '))
        class_list = f"./class_lists/{temp}_list.csv"
        insendi_file = sys.argv[1]
    else:
        sys.exit("Input must be y or n")
    
    print("\nLoading data...\n")
    analytics, classList = load_data(insendi_file, class_list)
    print("Data loaded.\n")
    
    print("Extracting section analytics...\n")
    columns_extract = extract_sections(analytics)
    print("\nSection analytics extracted.\n")
        
    print("Extracting class analytics...\n")
    merged = pd.merge(analytics, classList, left_on='Student', right_on='Students', how='inner')
    merged[columns_extract].to_csv('./analytics/class_analytics.csv', index=False)
    print("Class analytics extracted.\n")
    
if __name__ == "__main__":
    main()