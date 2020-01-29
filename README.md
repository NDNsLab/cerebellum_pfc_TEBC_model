# cerebellum_pfc_TEBC_model

To run the simulation, run the experiment file of each group. The software will generate activity files for all areas.

After generating the experiment file. Use the cr_calculation.py file, to calculate the CR of the control group and cr_calculation_SpG.py, to calculate the CR of the experimental group.

Sample: python <name of file: .py> ' < / directory path/ :str> ' < number of session: int> 
  
When you start the experimental group cr calculation, a "CR-CS_US" folder will be created inside the relative group directory.
Inside this folder the file "fr_max_mice.txt" will be generated.
Copy this file into the experimental group folder before launching the experimental group CR calculation file "cr_calculation_SpG.py"

Use the "utility_plot-raster.py" file to make chart of activity for areas: Inferior Olivary Nucleus, Punkinije Cells, Granular Cells, M1 and PFC.  

Sample: python < name of file: .py> '< / directory path / :str >' < number of session start :int> < number of session stop :int>
