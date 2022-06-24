import os
import sys
import optparse
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# import sklearn
# from sklearn.model_selection import train_test_split
# from sklearn import model_selection
# from sklearn.metrics import accuracy_score, confusion_matrix
# from sklearn.tree import DecisionTreeClassifier
# import array

#importing python modules from SUMO_HOME/tools directory

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci
import simpla

def get_options() :
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action = "store_true", default = False, help= "run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options



#contains TraCI control loop
def run():
    simpla.load("simpla.cfg")
    packVehicleData = []
    step = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()


        print(step)

        vehicles = traci.vehicle.getIDList()




        for i in range(0, len(vehicles)):


            vehid = vehicles[i]
            x, y = traci.vehicle.getPosition(vehicles[i])
            coord = [x, y]
            lon, lat = traci.simulation.convertGeo(x, y)
            gpscoord = [lon, lat]
            spd = round(traci.vehicle.getSpeed(vehicles[i]) * 3.6, 2)
            edge = traci.vehicle.getRoadID(vehicles[i])
            lane = traci.vehicle.getLaneID(vehicles[i])
            displacement = round(traci.vehicle.getDistance(vehicles[i]), 2)
            turnAngle = round(traci.vehicle.getAngle(vehicles[i]), 2)
            nextTLS = traci.vehicle.getNextTLS(vehicles[i])



            # Packing of all the data for export to CSV/XLSX
            vehList = [vehid, coord, gpscoord, spd, edge, lane, displacement, turnAngle, nextTLS]

            print("Vehicle: ", vehicles[i])
            print(vehicles[i], " >>> Position: ", coord, " | GPS Position: ", gpscoord, " |", \
                  " Speed: ", round(traci.vehicle.getSpeed(vehicles[i]) * 3.6, 2), "km/h |", \
                  # Returns the id of the edge the named vehicle was at within the last step.
                  " EdgeID of veh: ", traci.vehicle.getRoadID(vehicles[i]), " |", \
                  # Returns the id of the lane the named vehicle was at within the last step.
                  " LaneID of veh: ", traci.vehicle.getLaneID(vehicles[i]), " |", \
                  # Returns the distance to the starting point like an odometer.
                  " Distance: ", round(traci.vehicle.getDistance(vehicles[i]), 2), "m |", \
                  # Returns the angle in degrees of the named vehicle within the last step.
                  " Vehicle orientation: ", round(traci.vehicle.getAngle(vehicles[i]), 2), "deg |", \
                  # Return list of upcoming traffic lights [(tlsID, tlsIndex, distance, state), ...]
                  " Upcoming traffic lights: ", traci.vehicle.getNextTLS(vehicles[i]),
                  )

            idd = traci.vehicle.getLaneID(vehicles[i])

            #Machine learning algorithm





        # det_vehs = traci.inductionloop.getLastStepVehicleIDs("det_0")
        # for veh in det_vehs:
        #     print(veh)
        #     traci.vehicle.changeLane(veh, E7_2, 25)
        #     traci.vehicle.changeTarget("1", "E8")

    # if step >= 100:
    #
    #     traci.vehicle.changeLane("1", "E7_0", "25")
    #     traci.vehicle.changeLane("3", "E7_1", "25")
    #     traci.vehicle.changeTarget("1", "E8")
    #     traci.vehicle.changeTarget("3", "E8")



        step += 1


    traci.close()

    sys.stdout.flush()


#main entry point
if __name__ == "__main__":
    options =get_options()

    #check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    #traci starts sumo as a subprocess and then this script connects and runs

    traci.start([sumoBinary, "-c", "platoon2.sumocfg" , "--tripinfo-output", "--tripinfo.xml"])



    run()