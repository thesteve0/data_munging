__author__ = 'spousty'
import sys

# constants per run of the file
#gauge first
gauges = {"01377370", "01390450"}

#discharge first
gauges = {"01390450, 01387400", "01387420", "01387450", "01387500"}

#TODO need to do a separate table and processor for the well

table_name = "stations"

infile = open('/home/spousty/Downloads/TabDelimitedGaugeData.txt', 'r')
csv_outfile = open('./output.csv', 'w')
csv_outfile.write("'stationid,'date_time','time_zone','gauge','gauge_status','discharge','discharge_status','temp','temp_status'\n")
sql_outfile = open('./output.ddl', 'w')
json_outfile = open('./output.json', 'w')

def process_discharge_first(ine_items, csv_outfile, sql_outfile, json_outfile):
    reading = {}
    reading['station'] = line_items[1]
    reading['date_time'] = line_items[2]
    reading['time_zone'] = line_items[3]
    reading['discharge'] = line_items[4]
    reading['discharge_status'] = line_items[5]



def process_gauge_first(line_items, csv_outfile, sql_outfile, json_outfile):
    reading = {}
    reading['station'] = line_items[1]
    reading['date_time'] = line_items[2]
    reading['time_zone'] = line_items[3]
    reading['gauge'] = line_items[4]
    reading['gauge_status'] = line_items[5]

    #todo find the proper syntax here
    if(len(line_items) > 6):
        try:
            reading['discharge'] = line_items[6]
            reading['discharge_status'] = line_items[7]
        except:
            print("EXCEPTION: " + str(line_items.__len__()) + "   " + str(line_items))
    if(len(line_items) > 8):
        try:
            reading['temperature'] = line_items[8]
            reading['temperature'] = line_items[9]
        except:
            print("EXCEPTION: " + str(line_items.__len__()) + "   " + str(line_items))

    output_to_csv(reading, csv_outfile)
    return

def output_to_csv(reading, csv_outfile):
    the_line = reading['station'] + "," + reading['date_time'] + "," + reading['time_zone'] + "," + reading['gauge'] + "," + reading['gauge_status']
    if reading.__contains__('discharge'):
        the_line = the_line + "," + reading['discharge'] + "," + reading['discharge_status'] + "\n"
    else:
        the_line = the_line + "," + "NA" + "," + "NA" + "\n"

    csv_outfile.write(the_line)
    return

def output_to_sql(reading, sql_outfile):
    the_line = "insert into " + table_name + "(station_id, date_time, time_zone, gauge_reading, gauge_status, discharge, discharge_status) VALUES ("
    the_line = the_line + reading['station'] + ','

    return

def output_to_json(reading, json_outfile):

    return


#gauge first
# 01377370, 01390450 (With temp on end

#dishcharge first
# 01390450, 01387400, 01387420, 01387450, 01387500

current_id = 0

#setup two types, gauge first or flow first
# site 01390450 is a special example of gauge first
# The well is something all on it's own

lines = infile.readlines()
i = 1
for line in lines:
    if line.startswith("#"):
        print(line.strip())
        #print("-")
    else:
        line_items = line.strip().split("\t")
        # if line_items[1] == gauge:
        if line_items[1] in gauges:
            # outfile.write(line)
            i = i + 1
            process_gauge_first(line_items, csv_outfile, sql_outfile, json_outfile)




infile.close()
csv_outfile.close()
sql_outfile.close()
json_outfile.close()
print("done and processed this many lines of actual data: " + str(i))