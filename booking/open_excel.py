import csv


with open('D:\Downloads_chrome\Geely.csv', 'r', newline='') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        print(row)
