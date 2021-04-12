#!/usr/bin/python3

month = {
    'Jan' : '01',
    'Feb' : '02',
    'Mar' : '03',
    'Apr' : '04',
    'May' : '05',
    'Jun' : '06',
    'Jul' : '07',
    'Aug' : '08',
    'Sep' : '09',
    'Oct' : '10',
    'Nov' : '11',
    'Dec' : '12'
}

states = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FM": "Federated States Of Micronesia",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MH": "Marshall Islands",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "MP": "Northern Mariana Islands",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PW": "Palau",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VI": "Virgin Islands",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}

# Allow for the user to select data from only certain states

statesToSelect = input("Select States by Abbreviation seperated by commas (up to 10): ")
statesToSelect = statesToSelect.split(',')
print(statesToSelect)
empty = []

# nexus file will contain only header data
# sequences.fasta will contain the final fasta file to be used for analysis
nexus = open('nexus2.fasta', 'w')
new = open('sequences.fasta', 'w')
with open('finalsequences.fasta') as sequences:
    count = 0
    writer = False
    for line in sequences:
        count += 1
        if line.startswith('>'):
            if line.split('|')[1] not in empty and line.split('|')[1] in statesToSelect:
                empty.append(line.split('|')[1])
        if line.startswith(">") and line.split('|')[1] in statesToSelect and line.split('|')[2][3:6] in month.keys():
            nexus.write(line.split('|')[0] + '|' + line.split('|')[1] + '|' + line.split('|')[2][0:3] + month[line.split('|')[2][3:6]] + '-' + line.split('|')[2][-5:])
            new.write(line.split('|')[0] + '|' + line.split('|')[1] + '|' + line.split('|')[2][0:3] + month[line.split('|')[2][3:6]] + '-' + line.split('|')[2][-5:])
            writer = True
            print(line.split('|')[1])
            continue;
        elif line.startswith(">") and line.split('|')[1] in states.keys() and line.split('|')[1] in statesToSelect and (line.split('|')[2][0:4] == '2020' or line.split('|')[2][0:4] == '2021'):
            nexus.write(line.split('|')[0] + '|' + line.split('|')[1] + '|' + line.split('|')[2][-3:-1] + '-' + line.split('|')[2][5:7] + '-' + line.split('|')[2][0:4] + '\n')
            new.write(line.split('|')[0] + '|' + line.split('|')[1] + '|' + line.split('|')[2][-3:-1] + '-' + line.split('|')[2][5:7] + '-' + line.split('|')[2][0:4] + '\n')
            writer = True
            print(line.split('|')[1])
            continue;
        elif line.startswith(">") and line.split('|')[1] not in statesToSelect:
            writer = False
            continue;
        else:
            if(writer == True):
                new.write(line)
new.close()
print(empty)
