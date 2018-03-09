import numpy as np
import csv
import collections

# mortality is a dictionary that maps each overall rating to a list of each hospital's mortality national comparison
mortality = collections.defaultdict(list)
# readmission is a dictionary that maps each overall rating to a list of each hospital's readmission national comparison
readmission = collections.defaultdict(list)

# state county is a dictionary that maps each state/county to the number of hospitals in the county, how many of them are non-profit or acute care, as well all a list of all of the hospitals in the county's overall ratings
stateCounty = {}

#open the csv file and read line by line
with open('Hospital General Information.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        #if the state/county doesn't already exist, initialize it
        if ((row['State'], row['County Name'])) not in stateCounty: stateCounty[(row['State'], row['County Name'])] = {
            'Number of Hospitals': 0,
            'Number of Non-profit': 0,
            'Number of Acute care': 0,
            'overall ratings': list()
        }

        # increase the overall count of the number of hospitals in the county
        stateCounty[(row['State'], row['County Name'])]['Number of Hospitals'] += 1
        # count the amount of hospitals that are Voluntary non-profit
        if(row['Hospital Ownership'] == 'Voluntary non-profit - Private'):
            stateCounty[(row['State'], row['County Name'])]['Number of Non-profit'] += 1
        # count the number of hospitals that are acute care
        if(row['Hospital Type'] == 'Acute Care Hospitals'):
            stateCounty[(row['State'], row['County Name'])]['Number of Acute care'] += 1
        # if the hospital has an overall rating, add it's rating to the list of other hospital's ratings
        if(row['Hospital overall rating'] != 'Not Available'):
            stateCounty[(row['State'], row['County Name'])]['overall ratings'].append(row['Hospital overall rating'])

            # dictionary for mapping the national average statements to integers
            AvgToInt = {
                    'Below the national average': 1,
                    'Same as the national average': 2,
                    'Above the national average': 3,
                    'Not Available': None
                    }
            # add the hospital's mortality rating as an integer to the list in the mortality dictionary with the corosponding overall rating
            mortality[row['Hospital overall rating']].append((AvgToInt[row['Mortality national comparison']]))
            # add the hospital's readmission rating as an integer to the list in the readmission dictionary with the corosponding overall rating
            readmission[row['Hospital overall rating']].append((AvgToInt[row['Readmission national comparison']]))

    # calculate the mean for each overall rating in the mortality dictionary and store it in a sorted list
    mortalityList = list()
    for key in mortality:
        mortalityList.append((key, (np.mean(filter(None, mortality[key])))))
    mortalityList = list(sorted(tuple(mortalityList), key=lambda tup: tup[0]))

    # calculate the mean for each overall rating in the readmission dictionary and store it in a sorted list
    readmissionList = list()
    for key in readmission:
        readmissionList.append((key, (np.mean(filter(None, readmission[key])))))
    readmissionList = list(sorted(tuple(readmissionList), key=lambda tup: tup[0]))

    #process the gathered data for each state/county, store it in a sorted list
    outputList = list()
    for key in stateCounty:
        outputList.append({
        'State': (key[0]),
        'County': (key[1]),
        'Number of Hospitals': (stateCounty[key]['Number of Hospitals']),
        'Percent private or nonprofit': ((100 / stateCounty[key]['Number of Hospitals']) * stateCounty[key]['Number of Non-profit']),
        'number of acute care hospitals': (stateCounty[key]['Number of Acute care']),
        'avg acute care rating': (np.mean(list(map(int, stateCounty[key]['overall ratings'])))),
        'median acute care rating': (np.median(list(map(int, stateCounty[key]['overall ratings']))))
        })
    outputList = (sorted(tuple(outputList), key=lambda tup: tup['Number of Hospitals']))

    # Print the overall rating to mortality and readmission
    print('Mortality national comparison as a function of hospital overall rating on a scale of 1 to 3')
    for i in mortalityList:
        print(i)
    print('readmission national comparison as a function of hospital overall rating on a scale of 1 to 3')
    for i in readmissionList:
        print(i)

    #write each line of the state/county data to a csv file
    with open('output.csv', 'w') as csvfile:
        fieldnames = ['State', 'County', 'Number of Hospitals', 'Percent private or nonprofit', 'number of acute care hospitals', 'avg acute care rating', 'median acute care rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in outputList:
            writer.writerow({
            'State': i['State'],
            'County': i['County'],
            'Number of Hospitals': i['Number of Hospitals'],
            'Percent private or nonprofit': i['Percent private or nonprofit'],
            'number of acute care hospitals': i['number of acute care hospitals'],
            'avg acute care rating': i['avg acute care rating'],
            'median acute care rating': i['median acute care rating']
            })
