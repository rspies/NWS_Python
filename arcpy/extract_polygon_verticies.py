# created by Ryan Spies 
# 1/8/2016
# Python 2.7
# Description: extract polygon vertices

import arcpy
#################### user input #####################
shp = "D:\\Projects\\NWS\\GIS\\SERFC\\SERFC_FY2016\\shapefiles\\map_basins\\map_basins.shp"
out_summary = "D:\\Projects\\NWS\\GIS\\SERFC\\SERFC_FY2016\\shapefiles\\map_basins\\vertices_summary.txt"
################## end user input #####################

summary = open(out_summary,'w')
summary.write('Basin\t'+'Area (mi2)\t' + 'points\n')
infc = arcpy.GetParameterAsText(0)
# Enter for loop for each feature
# search fields: feature number, shape x/y coordinates, feature name (attribute table)
for row in arcpy.da.SearchCursor(shp, ["OID@", "SHAPE@","NAME","LOC_AREA_m"]):
    # Print the current multipoint's ID
    print("Feature {}:".format(row[0]))
    print("Feature Name {}:".format(row[2]))
    print("Feature Area {}:".format(row[3]))
    summary.write((row[2]) + '\t' + str(row[3]) +'\t')
    partnum = 0

    # Step through each part of the feature
    for part in row[1]:
        # Print the part number
        print("Part {}:".format(partnum))

        #count the number of points in the part
        pnt_count = 0
        pnt_int = len(part)/19 # try to get 20 points
        
        if len(part) > 25:
            # Step through each vertex in the feature
            for pnt in part:
                if pnt:
                    # Print x,y coordinates of current point if divisible by pnt_int
                    if pnt_count % pnt_int == 0:
                        lon = abs(round(pnt.X,2)); lat = round(pnt.Y,2)
                        summary.write(str("%.2f" % lat) +',' + str("%.2f" % lon) + '\t')
                        print("{}, {}".format(lon, lat))
                    pnt_count += 1
                else:
                    # If pnt is None, this represents an interior ring
                    print("Interior Ring:")
        partnum += 1
    summary.write('\n')
summary.close()
