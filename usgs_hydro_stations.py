__author__ = 'spousty'
import sys



# constants per run of the file
#gauge first
gauges = {"01377370", "01390450"}

#discharge first
discharges = {"01390450", "01387400", "01387420", "01387450", "01387500", "01376800"}

#the single well
well = {"410155074060201"}

river_table_name = "stations"

infile = open('/home/spousty/Downloads/TabDelimitedGaugeData.txt', 'r')

river_csv_outfile = open('./river_output.csv', 'w')
river_csv_outfile.write("'stationid,'date_time','time_zone','gauge','gauge_status','discharge','discharge_status','temp','temp_status'\n")
river_sql_outfile = open('./river_output.ddl', 'w')

well_csv_outfile = open('./well_output.csv', 'w')
well_csv_outfile.write("'stationid,'date_time','time_zone','depth','depth_status'\n")
well_sql_outfile = open('./well_output.ddl', 'w')

def process_wells(line_items, well_csv_outfile, well_sql_outfile):
    reading = {}
    reading['station'] = line_items[1]
    reading['date_time'] = line_items[2]
    reading['time_zone'] = line_items[3]
    reading['depth'] = line_items[4]
    reading['depth_status'] = line_items[5]
    well_output_to_csv(reading, well_csv_outfile)
    well_output_to_sql(reading, well_sql_outfile)
    return



def process_discharge_first(line_items, river_csv_outfile, river_sql_outfile):
    reading = {}
    reading['station'] = line_items[1]
    reading['date_time'] = line_items[2]
    reading['time_zone'] = line_items[3]
    reading['discharge'] = line_items[4]
    reading['discharge_status'] = line_items[5]
    if(len(line_items) > 6):
        try:
            reading['gauge'] = line_items[6]
            reading['gauge_status'] = line_items[7]
        except:
            print("EXCEPTION: " + str(len(line_items)) + "   " + str(line_items))

    river_output_to_csv(reading, river_csv_outfile)
    river_output_to_sql(reading, river_sql_outfile)
    return

def process_gauge_first(line_items, river_csv_outfile, river_sql_outfile):
    reading = {}
    reading['station'] = line_items[1]
    reading['date_time'] = line_items[2]
    reading['time_zone'] = line_items[3]
    reading['gauge'] = line_items[4]
    reading['gauge_status'] = line_items[5]

    if(len(line_items) > 6):
        try:
            reading['discharge'] = line_items[6]
            reading['discharge_status'] = line_items[7]
        except:
            print("EXCEPTION: " + str(len(line_items)) + "   " + str(line_items))
    if(len(line_items) > 8):
        try:
            reading['temperature'] = line_items[8]
            reading['temperature'] = line_items[9]
        except:
            print("EXCEPTION: " + str(len(line_items)) + "   " + str(line_items))

    river_output_to_csv(reading, river_csv_outfile)
    river_output_to_sql(reading, river_sql_outfile)
    return

def river_output_to_csv(reading, river_csv_outfile):
    the_line = reading['station'] + "," + reading['date_time'] + "," + reading['time_zone'] + ","
    try:
        the_line = the_line + reading.get('gauge', 'NA') + ","
        the_line = the_line + reading.get('gauge_status', 'NA') + ","
        the_line = the_line + reading.get('discharge', 'NA') + ","
        the_line = the_line + reading.get('discharge_status', 'NA') + ","
    except:
        print("EXCEPTION!!!! in get attr for river")

    the_line = the_line + "\n"
    river_csv_outfile.write(the_line)
    return

def well_output_to_csv(reading, well_csv_outfile):

    the_line = reading['station'] + "," + reading['date_time'] + "," + reading['time_zone'] + ","
    try:
        the_line = the_line + reading.get('depth', 'NA') + ","
        the_line = the_line + reading.get('depth_status', 'NA') + ","
    except:
        print("EXCEPTION!!!! in get attr for well")

    the_line = the_line + "\n"
    well_csv_outfile.write(the_line)

    return


def well_output_to_sql(reading, well_sql_outfile):
    the_line = "insert into " + river_table_name + "(station_id, date_time, time_zone, depth, depth_status) VALUES ("
    the_line = the_line + reading['station'] + "','" + reading['date_time'] + "', '" + reading['time_zone'] + "',"
    try:
        the_line = the_line + reading.get('depth', str(-999)) + ",'"
        the_line = the_line + reading.get('depth_status', '') + "'); \n"
    except:
        print("EXCEPTION!!!! in get attr for well")

    well_sql_outfile.write(the_line)

    return

def river_output_to_sql(reading, river_sql_outfile):
    the_line = "insert into " + river_table_name + "(station_id, date_time, time_zone, gauge, gauge_status, discharge, discharge_status) VALUES ("
    the_line = the_line + reading['station'] + "','" + reading['date_time'] + "', '" + reading['time_zone'] + "',"
    try:
        the_line = the_line + reading.get('gauge', str(-999)) + ",'"
        the_line = the_line + reading.get('gauge_status', '') + "',"
        the_line = the_line + reading.get('discharge', str(-999)) + ",'"
        the_line = the_line + reading.get('discharge_status', '') + "'); \n"
    except:
        print("EXCEPTION!!!! in get attr for river in SQL")

    river_sql_outfile.write(the_line)

    return


#########################################################################

current_id = 0


lines = infile.readlines()
i = 1
for line in lines:
    if line.startswith("#"):
        print(line.strip())
        i += 1
    else:
        line_items = line.strip().split("\t")
        # if line_items[1] == gauge:
        if line_items[1] in gauges:
            # outfile.write(line)
            i += 1
            process_gauge_first(line_items, river_csv_outfile, river_sql_outfile)
        elif line_items[1] in discharges:
            i += 1
            process_discharge_first(line_items, river_csv_outfile, river_sql_outfile)
        elif line_items[1] in well:
            i += 1
            process_wells(line_items, well_csv_outfile, well_sql_outfile)
        else:
            print(line)


infile.close()
river_csv_outfile.close()
river_sql_outfile.close()
well_csv_outfile.close()
print("done and processed this many lines of actual data: " + str(i))