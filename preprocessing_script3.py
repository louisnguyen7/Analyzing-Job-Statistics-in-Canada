'''
preprocessing_script3.py
  Author(s): Louis Nguyen, Ahmet Ozer, Arya Oberoi, Zain Murad

  Project: Term Project Milestone 3
  Date of Last Update: March 24, 2025.

  Functional Summary
      preprocessing_script3.py reads a CSV file and extracts data fields based on user input.
      The data is then written to an output file called outputQ3.csv.
      
      It takes 7 fields: YEAR, Geography, Type of work, Wages, Education level, Male, Female
      Input should be in this order: 7, YEAR, Geography, Type of work, Wages, Education level, Male, Female
      Press the enter key after each time a field is inputted.

     Commandline Parameters: 2
        argv[1] = dataset in CSV format
     References
        Datasets from https://data.ontario.ca/dataset/wages-by-education-level/resource/7b325fa1-e9d6-4329-a501-08cdc22a79df
'''

import csv
import sys
import pandas as pd

def main(argv):

    #Open the file
    try:
        openFile = open(sys.argv[1], encoding="utf-8-sig")
    except IOError as err:
        print("Error", file=sys.stderr)
        sys.exit(1)

    readCSV = csv.reader(openFile, skipinitialspace=True)
    
    #Ask the user how many data fields they would like to use
    try:
        fieldsNum = int(input("How many data fields would you like to search for? "))
    except ValueError:
        print("Invalid input", file=sys.stderr)
        sys.exit(1)
    fields = []
    
    #Ask the user to input data fields individually
    print("Please enter any of the following fields: _id,YEAR,Geography,Type of work,Wages,Education level,Age group,Both Sexes,Male,Female")
    for i in range(fieldsNum):
        field = input("What would you like to search for? ")
        fields.append(field)

    lineNumber = 0

    #Match the inputted fields with the fields on the header line of the csv file
    for header in readCSV:
        selected_headers = [head for head in header if head in fields]
        print("Downloading data for fields: " + ', '.join(selected_headers))
        lineNumber += 1
        if lineNumber == 1:
            break
    
    rowIndex = [header.index(field) for field in selected_headers]
    
    dataFields = []

    counter = 0
    #Make a list only with the data fields chosen
    for row_data_fields in readCSV:
        data = []
        for i in rowIndex:
            data.append(row_data_fields[i])
        dataFields.append(data)

    with open('outputQ3.csv', 'a') as output_file:
        
        education_data = {}

        for i in range(len(dataFields)):
            if dataFields[i][0] == "2019" and dataFields[i][1] == "Canada" and dataFields[i][2] == "Both full- and part-time" and dataFields[i][3] == "Average hourly wage rate" and dataFields[i][4] != "Total, all education levels":
                education = dataFields[i][4]
                male = float(dataFields[i][5])
                female = float(dataFields[i][6])

                if education not in education_data:
                        education_data[education] = {'male': [], 'female': []}
                
                #Make lists with the wages for each education level
                education_data[education]['male'].append(male)
                education_data[education]['female'].append(female)
                
        #Calculate the average wages for male and female
        for edu, wages in education_data.items():
            avg_male = sum(wages['male']) / len(wages['male'])
            avg_female = sum(wages['female']) / len(wages['female'])
            
            
            #Write the dataset to a file
            output_file.write(f"2019,Canada, Both full- and part-time, Average hourly wage rate,\"{edu}\",{avg_male:.2f},{avg_female:.2f}\n")

main(sys.argv)