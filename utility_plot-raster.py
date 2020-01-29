import pylab as pl
import elephant as el
import numpy as np
import math as m
import time
import sys
import datetime
import quantities as pq
import neo
import scipy
from matplotlib.backends.backend_pdf import PdfPages
from time import sleep
import csv
from os.path import exists
import os

def firingRateManual (spike_train, start=100., wnd=300.):
    
    spike_train = np.array(spike_train).astype(np.float).round()
    spike_train_in_wnd = spike_train[np.where((spike_train > start) & (spike_train < start+wnd))]
    FR = el.statistics.mean_firing_rate(spike_train, start , start+wnd)
    obj_returned={"FR":FR, "n_spike":np.count_nonzero(spike_train_in_wnd)}
    
    return obj_returned

#firing rate
def firingRate(spike_train,sig=100):
     kernel_gau=el.kernels.GaussianKernel(sigma=sig*pq.ms)

     try:         
         firing_rate=el.statistics.instantaneous_rate(neo.SpikeTrain(spike_train, units=pq.ms, t_start=np.array(spike_train).min(), t_stop=np.array(spike_train).max()), sampling_period=pq.Quantity([1], 'ms'), kernel=kernel_gau)        
     
     except:        
        firing_rate=0   
         
     return firing_rate # Write  file


# Write  file
def scriviFile (obj, path=os.getcwd()+"/mice/", output_file="outputKernel.txt"):
    
    if not os.path.isdir(path):
         os.mkdir(path)
    file = path+output_file
                
    if (exists(file)):
        out_file = open(file, "a")
        out_file.write("%s\n" % str(obj))
        out_file.close()
    else:
        out_file = open(file, "w")
        out_file.write("%s\n" % str(obj))
        out_file.close()
                                
def make_chart (path):
    

    GC = 512
    ISI = "150C"
    version = 13
    session_time = 2500
    label_grf=''
    FRm_array=[]
    FR_mice_max_array=[]
    CRp_array=[]
    FR_mean_range_of_value_m1=[]
    FR_mean_range_of_value_m1_after_first_cs = []
    
    try:
        base_path=sys.argv[1]
        session_number=int(sys.argv[3])

    except:
        print ("Manca il path della cartella che contiene le sessioni o il numero delle sessioni \n")
        print ("Sample: python <name of file:.py> '</directory path/:str>' <number of session start:int> <number of session stop:int>")
        exit()
  
    path=base_path+path
    path_save = "/home/mirino/Documents/cerebellum/13/Simulazione Per Revisori (14)/150C/"
    
    print ("\n\n")    
    print ("***/%/*** Run session => " + path + "  ***/%/***")
    print ("\n\n")

                                
    #make a python dictionary with firingRate of value find into file name content'list_file_name.csv'                    
    with open(path+'list_file_name.csv') as csv_name_file:
        csv_reader_name_file = csv.reader(csv_name_file, delimiter=',')
        data=[]
        n_spike=[]
        firing_rate_m1_learning=[]
        learning=[]
        firing_rate_area= {}
        spike_area={}
        line_count_name_file = 0
        number_session=[]
        for row_name_file in csv_reader_name_file:
            
            try:       
                with open(path+row_name_file[0]) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                 
                    for row in csv_reader:
                        data.append(float(row[0]))
                        line_count += 0                
            except:
                continue
            
            if (row_name_file[0][:9] == 'output_m1'): 
                
                out_fr=firingRateManual(data)
                firing_rate_m1_learning.append(out_fr["FR"])
                n_spike.append(out_fr["n_spike"])
                
            
            if (row_name_file[0][:9] == "output_m1" or row_name_file[0][:9] == "output_ms" or row_name_file[0][:9] == "output_ps" or row_name_file[0][:9] == "output_p1" or row_name_file[0][:9] == "output_p2" or row_name_file[0][:9] == "output_sf" or row_name_file[0][:9] == "output_if"):    
                print ("Import file <= " + path+row_name_file[0] + "\n")
                print (row_name_file[0][:9])                    

                firing_rate_area[row_name_file[0][:9]+"_"+str.replace(row_name_file[0][-6:-4],'_','')] = firingRate(data) # put firing rate into dictionary                       
                number_session.append(int(str.replace(row_name_file[0][-6:-4],'_','')))                    

                try:
                    spike_area[row_name_file[0][:9]+"_"+str.replace(row_name_file[0][-6:-4], '_', '')] = np.loadtxt(path+row_name_file[0], delimiter=',')
                except:
                    continue
            
            row=[]
            data=[]
            line_count_name_file += 1
    
    print ("ATTENZIONE: RICORDA CHE I FILE VGC NON VENGONO CARICATI PER ALLEGERIRE IL CARICAMENTO")
                                        
     
   
                                       
    for count_us in np.unique(number_session):
    
            
            print ("\n\n ========================================================================= \n")
            print ("\n\n ========================================================================= \n\n")              
            print ("====> SECTION NUMBER ---> " + str(count_us) + "\n\n")            

            
    
          
            CR =firing_rate_m1_learning[count_us]
         
                      
            scriviFile(CR, path, "cr_di_sessione.txt")
              
            CRp_array.append(CR)              
            
            print(CRp_array)                      
                        

    
    for count in np.unique(number_session):
    
 
        pl.figure()
        pl.suptitle('Trace 150 - Controlo group (mice 0, session '+str(count)+')', fontsize=16)
        pl.subplots_adjust(hspace=0.9)                               
        pl.subplot(321) 
        pl.plot(spike_area["output_ms"+"_"+str(count)].transpose()[0], spike_area["output_ms"+"_"+str(count)].transpose()[1], linestyle='', marker=',', markerfacecolor='blue' , label='M1 spike')
        pl.xlabel('msec')
        pl.ylabel('M1 neurons')
        pl.xlim(0, 2500)
        pl.yticks([])
        pl.xticks(np.arange(0, 2500, 500))
                   
        pl.subplots_adjust(hspace=0.9)                               
        pl.subplot(322) 
        pl.plot(spike_area["output_ps"+"_"+str(count)].transpose()[0], spike_area["output_ps"+"_"+str(count)].transpose()[1], linestyle='', marker=',', markerfacecolor='blue' , label='PFC spike')            
        pl.xlabel('msec')
        pl.ylabel('PFC neurons')
        pl.xlim(0, 2500)
        pl.yticks([])
        pl.xticks(np.arange(0, 2500, 500))
       
        pl.subplots_adjust(hspace=0.9)                       
        pl.subplot(323) 
        pl.plot(spike_area["output_p1"+"_"+str(count)].transpose()[0], spike_area["output_p1"+"_"+str(count)].transpose()[1], linestyle='', marker=',', markerfacecolor='blue' , label='PC Fast spike')
        pl.xlabel('msec')
        pl.ylabel('PC fast neurons')
        pl.margins(y=0.2)
        pl.xlim(0, 2500)
        pl.xticks(np.arange(0, 2500, 500))
        pl.yticks([])

        pl.subplots_adjust(hspace=0.9)                       
        pl.subplot(324) 
        pl.plot(spike_area["output_p2"+"_"+str(count)].transpose()[0], spike_area["output_p2"+"_"+str(count)].transpose()[1], linestyle='', marker=',', markerfacecolor='blue' , label='PC slow spike')
        pl.xlabel('msec')
        pl.ylabel('PC slow neurons')
        pl.margins(y=0.2)
        pl.xlim(0, 2500)
        pl.xticks(np.arange(0, 2500, 500))
        pl.yticks([])
              
        pl.subplots_adjust(hspace=0.9)                               
        pl.subplot(325) 
        pl.plot(spike_area["output_sf"+"_"+str(count)].transpose()[0], spike_area["output_sf"+"_"+str(count)].transpose()[1], linestyle='', marker=',', markerfacecolor='blue' , label='GC spike')
        pl.xlabel('msec')
        pl.ylabel('GC neurons')
        pl.xlim(0, 2500)
        pl.yticks([])
        pl.xticks(np.arange(0, 2500, 500))
        
        pl.subplots_adjust(hspace=0.9)             
        pl.subplot(326) 
        pl.plot(spike_area["output_if"+"_"+str(count)].transpose()[0], spike_area["output_if"+"_"+str(count)].transpose()[1], linestyle='', marker=',', markerfacecolor='blue' , label='IO spike')
        pl.xlabel('msec')
        pl.ylabel('IO neurons')
        pl.xlim(0, 2500)
        pl.xticks(np.arange(0, 2500, 500))
        pl.yticks([])
        pl.margins(y=0.2)

        pl.savefig("session_"+str(count)+".png")
                   
        pl.clf()
            

for i in range (int(sys.argv[2]), int(sys.argv[3])):
        
    make_chart ('session_mice_'+str(i)+'/') 

