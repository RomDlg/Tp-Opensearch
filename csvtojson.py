from csv import reader
import pandas as pd

file = open('github.json', 'a')

with open('repos.csv') as csv:
    csv_reader = reader(csv)
    index = 1

    for row in csv_reader:
        file.write('{"index":{"_index": "repositories","_id":' + str(index) + '}}\n')
        file.write('{ "username": "' + row[0] + '",')
        file.write(' "repository_name": "' + row[1] + '",')
        file.write(' "description": "' + row[2] + '",')
        file.write(' "last_update_date": "' + row[3] + '",')
        file.write(' "language": "' + row[4] + '",')
        file.write(' "number_of_stars": "' + row[5] + '",')
        file.write(' "tags": "' + row[6] + '",')
        file.write(' "url": "' + row[7] + '"}\n')
        index += 1
    file.close()

