# do some preliminary data munging before working in jupyter notebook
import csv
import re

# dictionary of the characters that need to be removed
cleaning_dict = {
    '*': '', 
    '#': '', 
    'Kenya .': 'Kenya',
    ' VA': '',
    ' MD': '', 
    ' PA': '',
}

# method to remove unwanted characters
def removeChar(cell):
    pattern = re.compile(r'(?<!\w)(' + '|'.join(re.escape(key) for key in cleaning_dict.keys()) + r')(?!\w)')
    return pattern.sub(lambda x: cleaning_dict[x.group()], cell)

# fix the format of the time columns for future use
def fixTimes(cell):
    if len(cell.split(':')) == 2:
        return f'00:{cell}'
    return cell

# fix the format of the time columns for future use
def fixDigits(cell):
    if len(cell.split(':')[0]) == 1:
        cells = cell.split(':')
        cells[0] = f'0{cells[0]}'
        return ':'.join(cells)
    return cell

# set up empty dataset to be exported to csv file
dataset = []

# tab deliminated txt files were first opened in numbers and then exported to cvs
# use with open to iterate through every cell and run the cleaning functions
with open('MA_Exer_PikesPeak_Females.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        gun = removeChar(row['Gun Tim'])
        net = removeChar(row['Net Tim'])
        pace = removeChar(row['Pace'])
        gun = fixTimes(gun)
        net = fixTimes(net)
        pace = fixDigits(pace)
        pace = fixTimes(pace)
        place = row['Place']
        divtot = row['Div/Tot']
        num = row['Num']
        name = row['Name']
        ag = row['Ag']
        hometown = row['Hometown']
        newRow = {'Place': place, 'Div/Tot': divtot, 'Num': num, 'Name': name, 'Ag': ag, 'Hometown': hometown, 'Gun Tim': gun, 'Net Tim': net, 'Pace': pace}
        dataset.append(newRow)

print(dataset)

# column names
fieldnames=['Place', 'Div/Tot', 'Num', 'Name', 'Ag', 'Hometown', 'Gun Tim','Net Tim','Pace']

# export to csv
with open(r'newfile.csv', 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for r in dataset:
        writer.writerow(r)

# run in terminal using python3 munge.py