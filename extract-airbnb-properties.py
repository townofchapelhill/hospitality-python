import airbnb
import airbnb_secrets
import csv

items=1
output_filename="airbnb_chapelhill.csv"
# Set CSV Header & line format
csv_header = ['City','Latitude','Longitude','Type','Bathrooms','Bedrooms','Public Address','Localized City','Source']

api = airbnb.Api()
# api = airbnb.Api(airbnb_secrets.login, airbnb_secrets.password)
api = airbnb.Api(access_token=airbnb_secrets.access_token)
try:
   output_file = open(output_filename, 'w')
   csvwriter = csv.writer(output_file, dialect='excel')
except IOError:
   print("Output file creation failed")
   exit(1)

csvwriter.writerow(csv_header)

while True:
   try:
      response = api.get_homes("Chapel Hill, NC, USA",items_per_grid=10, offset=items)
   except Exception:
      print("Terminating on error")
      raise Exception
      break
   print("Starting item: "+ str(items) + " responses: " + str(len(response['explore_tabs'][0]['sections'][0]['listings'])))
#   items += 50
   items += len(response['explore_tabs'][0]['sections'][0]['listings'])
   if len(response['explore_tabs'][0]['sections'][0]['listings']) == 0:
      break
   # ETL processing result set
   for x in range(0, len(response['explore_tabs'][0]['sections'][0]['listings'])):
      # build the output values in key order
      csv_output=['null']*9
      csv_output[0]=response['explore_tabs'][0]['sections'][0]['listings'][x]['listing']['city']
      csv_output[1]=response['explore_tabs'][0]['sections'][0]['listings'][x]['listing']['lat']
      csv_output[2]=response['explore_tabs'][0]['sections'][0]['listings'][x]['listing']['lng']
      csv_output[3]=response['explore_tabs'][0]['sections'][0]['listings'][x]['listing']['room_and_property_type']
      csv_output[4]=response['explore_tabs'][0]['sections'][0]['listings'][x]['listing']['bathrooms']
      csv_output[5]=response['explore_tabs'][0]['sections'][0]['listings'][x]['listing']['bedrooms']
      csv_output[6]=response['explore_tabs'][0]['sections'][0]['listings'][x]['listing']['public_address']
      csv_output[7]=response['explore_tabs'][0]['sections'][0]['listings'][x]['listing']['localized_city']
      csv_output[8]="AirBnB"
      csvwriter.writerow(csv_output)

# cleanup and exit
output_file.close()
