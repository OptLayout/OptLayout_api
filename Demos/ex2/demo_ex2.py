# %%
# %%
import sys
import os
# parentpath=os.getcwd().split("Subsea_Field_Layout_Opt") [0] + "Subsea_Field_Layout_Opt"
parentpath=os.getcwd().split("Demos") [0]
sys.path.append(parentpath)

from CLS_OptField import OptField

# # .ipynb does not need this
from multiprocessing import freeze_support
if __name__ == '__main__':
    freeze_support()

    # %%
    filepath=parentpath+"\\Demos\\ex2\\input_heiss.json"
    print("//////////////////////////////")
    print("executing on the following file:")
    print(filepath)
    print("//////////////////////////////")

    # %%
    # initialize a class instance
    myfield=OptField(filepath)

    # %%
    # %%
    # compute all cost contours as satellites
    myfield.get_contours()
    # simple visualization of the contours
    myfield.plot_contours()
    # %%
    # check one cluster, i.e., 1-site-N-wells
    myfield.get_1site()
    myfield.plot_1site()
    # optimal PK=[5.16460438e+05,  6.78234039e+06]
    myfield.plot_1site(showContour=1)
    # %%
    # check one cluster, i.e., 1-site-N-wells
    myfield.get_1site([0,1,2])
    myfield.plot_1site()
    # optimal PK=[ 516702.83944175 6782333.60229119]
    myfield.plot_1site(showContour=1)
    
    # set turn angle contraint for the 1st well 
    # so that its trajectory  won't have such a huge turn
    myfield.necon=[ [' -theta2+pi/3'], ['nan'], ['nan']]
    myfield.get_1site([0,1,2])
    myfield.plot_1site()
    # optimal PK= [ 516618.5892133  6782330.91730463]
    myfield.soluList_1site[1]

    # # %%
    # # save 1-site-N-wells results to json file
    # myfield.write_json_1site("heiss_traj_.json")

    # # %%
    # # save 1-site-N-wells results to excel file
    # myfield.write_excel_1site("heiss_output.xlsx")

    # # %%
    # # save cost contours of satellites to json file
    # myfield.write_json_contours("heiss_cstcontour_.json")

    # # %%
    # # save cost contours of satellites to excel file
    # myfield.write_excel_contours("heiss_output.xlsx")

    # # %%
    # # save cost contours of 1-site-N-well to json file
    # myfield.write_json_contour1site("heiss_cstcontour_cluster_.json",
    #                                 ClusterNO=1)

    # # %%
    # # save cost contours of 1-site-N-well to json file
    # myfield.write_excel_contour1site("heiss_output.xlsx",
    #                                 ClusterNO=1)


    # %%
    input("Press Enter to exit...")