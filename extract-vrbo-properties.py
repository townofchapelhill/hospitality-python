from pyquery import PyQuery
import re
import csv
import json

geo={}
csv_output = ['']*9

# Set CSV Header & line format
# csv_header = ['City','Latitude','Longitude','Type','Bathrooms','Bedrooms','Public Address','Localized City','Source']
# create output file & write header row
try:
   output_file = open("airbnb_chapelhill.csv", 'a')
   csvwriter = csv.writer(output_file, dialect='excel')
except IOError:
   print("Output file creation failed")
   exit(1)
# csvwriter.writerow(csv_header)

# Query the first page with location option
url = "https://www.vrbo.com/search/keywords:chapel-hill-nc-usa/@35.874919139908165,-79.113394930114,35.95736065574712,-79.01846618865892,13z?petIncluded=false&ssr=true"
# url = 'https://www.homeaway.com/results/keywords:Chapel%20Hill%2C+NC%2C+USA%29/Page:'

results = [['' for i in range(5)] for j in range(200)]
result_count = 0
page=1
while page < 2:
   x = PyQuery(url+str(page))
   start_location = end_location = 0
   while True:
       property_data={}
       start_location = x.html().find('"bathrooms":',end_location)+12
       end_location = x.html().find('}', start_location)+1
       try:
           property_data=json.loads(x.html()[start_location:end_location])
           results[result_count][0] = property_data['full'] + property_data['half']*0.5
       except:
           break
       start_location = x.html().find('"bedrooms":',end_location)+11
       end_location = x.html().find(',', start_location)
       results[result_count][1] = x.html()[start_location:end_location]

       start_location = x.html().find('"propertyType":',end_location)+15
       end_location = x.html().find(',', start_location)
       results[result_count][2] = re.sub(r'"', '', x.html()[start_location:end_location])

       start_location = x.html().find('detailPageUrl":',end_location)
       end_location = x.html().find(',', start_location)
       results[result_count][3] = x.html()[start_location:end_location]

       result_count += 1
   page += 1

print('result count:  {}'.format(result_count))

#property_url = "https://www.homeaway.com"
property_url = "https://www.vrbo.com"
property = 0
start_location = end_location = 0

while results[property][3] != "":
   query_string = re.sub(r'\\u002F', '/', results[property][3])
   start_location = query_string.find("/")
   end_location = query_string.find("?", start_location)
   # print("property {}".format(query_string[start_location:end_location]))
   y = PyQuery(property_url + query_string[start_location:end_location])
   start_location = y.html().find('geoCode') + 9
   end_location = y.html().find('}', start_location) + 1
   results[property][4] = y.html()[start_location:end_location]
   property += 1

for i in range(0,result_count):
   if results[i][0] == '':
     continue
   geo = json.loads(results[i][4])
   # City
   csv_output[0] = "Chapel Hill"
   #'Latitude'
   csv_output[1] = geo['latitude']
   #'Longitude'
   csv_output[2] = geo['longitude']
   #'Type'
   csv_output[3] = results[i][2]
   #'Bathrooms'
   csv_output[4] = results[i][0]
   #'Bedrooms'
   csv_output[5] = results[i][1]
   # Public Address
   csv_output[6] = ""
   # Localized City
   csv_output[7] = ""
   # Source
   csv_output[8] = "VRBO"
   csvwriter.writerow(csv_output)

# cleanup and exit
output_file.close()
