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
    filepath=parentpath+"\\Demos\\ex1\\input_ex1.json"
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
    myfield.get_1site([0,25,26])
    # simple visualization of the 1-site-N-wells trajectories
    myfield.plot_1site()
    # show the cost contour of the 1-site-N-wells
    myfield.plot_1site(showContour=1)

    # %%
    myfield.soluList_1site[1]

    # %%
    # compute KsitesNwells
    myfield.get_Ksites()
    # simple visualization of K-sites-N-wells
    myfield.plot_Ksites()
    
    # %%
    # save 1-site-N-wells results to json file
    myfield.write_json_1site(".\\results\\ex1_traj_.json")

    # %%
    # save 1-site-N-wells results to excel file
    myfield.write_excel_1site(".\\results\\ex1_output.xlsx", "Atraj_No_")

    # %%
    # save cost contours of satellites to json file
    myfield.write_json_contours(".\\results\\ex1_cstcontour_.json")

    # %%
    # save cost contours of satellites to excel file
    myfield.write_excel_contours(".\\results\\ex1_output.xlsx")

    # %%
    # save cost contours of 1-site-N-well to json file
    myfield.write_json_contour1site(".\\results\\ex1_cstcontour_cluster_.json",
                                    ClusterNO=1)

    # %%
    # save cost contours of 1-site-N-well to json file
    myfield.write_excel_contour1site(".\\results\\ex1_output.xlsx",
                                    ClusterNO=1)

    # %%
    # save K-sites-N-wells results to json file
    myfield.write_json_Ksites(".\\results\\ex1_Ktraj_.json")

    # %%
    # save K-sites-N-wells results to json file
    myfield.write_excel_Ksites(".\\results\\ex1_output.xlsx", "Ktraj_No_")

    # %%
    input("Press Enter to exit...")