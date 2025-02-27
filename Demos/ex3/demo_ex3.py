# %%
# %%
import sys
import os
# parentpath=os.getcwd().split("Subsea_Field_Layout_Opt") [0] + "Subsea_Field_Layout_Opt"
parentpath=os.getcwd().split("Demos") [0]
sys.path.append(parentpath)

from CLS_OptField import OptField

# # .ipynb acutally does not need this
from multiprocessing import freeze_support
if __name__ == '__main__':
    freeze_support()

    # %%
    # %%
    filepath=parentpath+"\\Demos\\ex3\\input_ex3.json"
    print("//////////////////////////////")
    print("executing on the following file:")
    print(filepath)
    print("//////////////////////////////")

    # %%
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
    # %%
    # check one cluster, i.e., 1-site-N-wells
    myfield.get_1site()
    myfield.plot_1site()

    # %%
    # show the cost contour of the 1-site-N-wells problem
    myfield.plot_1site(showContour=1)

    # %%
    # check current constraints
    myfield.necon

    # %% [markdown]
    # You can easily identify that the 2nd turn of the first well is smaller than 90 degrees (pi/2), while the second well's exceeds 90 degrees.

    # %%
    # check the 2nd turn angle(rad) of those trajectories
    [myfield.soluList_1site[i]['theta2'] for i in range(3)]

    # %%
    # replicate a case, and change "necon"
    myfield2=OptField(filepath)
    myfield2.necon=[ [' -PK[1]+1300'], ['-theta2+pi/2'], ['nan']]
    myfield2.get_1site()
    myfield2.plot_1site()

    # %%
    myfield2.soluList_1site[1]

    # %%
    # save 1-site-N-wells results to json file
    myfield.write_json_1site("ex3_traj_.json")

    # %%
    # save 1-site-N-wells results to excel file
    myfield.write_excel_1site("ex3_output.xlsx")

    # %%
    # save cost contours of satellites to json file
    myfield.write_json_contours("ex3_cstcontour_.json")

    # %%
    # save cost contours of satellites to excel file
    myfield.write_excel_contours("ex3_output.xlsx")

    # %%
    # save cost contours of 1-site-N-well to json file
    # Use ClusterNO to identify different clusters
    myfield.write_json_contour1site("ex3_cstcontour_cluster_.json",
                                    ClusterNO=1)

    # %%
    # save cost contours of 1-site-N-well to json file
    # Use ClusterNO to identify different clusters
    myfield.write_excel_contour1site("ex3_output.xlsx",
                                    ClusterNO=1)

    # %%
    input("Press Enter to exit...")