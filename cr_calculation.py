import elephant as el
import numpy as np
import sys
import quantities as pq
import neo
import csv
from os.path import exists
import os


#firing rate
def firingRate(spike_train,sig=100,  start=100., stop=300., ch=2.):
    
    kernel_gau=el.kernels.GaussianKernel(sigma=sig*pq.ms)
    
    if ch == 1.: #period
        firing_rate=el.statistics.instantaneous_rate(neo.SpikeTrain(spike_train, units=pq.ms, t_start=np.array(spike_train).min(), t_stop=np.array(spike_train).max()), sampling_period=pq.Quantity([1], 'ms'), kernel=kernel_gau)
  
    if ch == 2.: #all section
          
        SpikeTrainL = list(np.where(np.logical_and(np.array(spike_train)>=start, np.array(spike_train)<=stop)))     
        array_a =neo.SpikeTrain ( SpikeTrainL, units=pq.ms, t_start=np.array(SpikeTrainL).min(),  t_stop=np.array(SpikeTrainL).max())
        firing_rate=el.statistics.instantaneous_rate(array_a, sampling_period=pq.Quantity([1], 'ms'), kernel=kernel_gau)
        
     
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


def calculate_cr (path):
    
    version = 8.2
    session_time = 2500
    CRp_array=[]
    
    try:
        base_path=sys.argv[1]
    except:
        print ("The path of the folder containing the sessions or the number of sessions is missing \n")
        print ("Sample: python <name of file:.py> '</directory path/:str>' <number of session:int>")
        exit()
  
    path=base_path+path
    
    print ("***/%/*** Run session => " + path + "  ***/%/***")

                            
    #make a python dictionary with firingRate of value find into file name content'list_file_name.csv'                    
    with open(path+'list_file_name.csv') as csv_name_file:
       

        csv_reader_name_file = csv.reader(csv_name_file, delimiter=',')
        data=[]
        firing_rate_m1_learning=[]
        firing_rate_area= {}
        spike_area={}
        line_count_name_file = 0
        number_session=[]
        
        for row_name_file in csv_reader_name_file:
            
            #print ("2")
            try:
                #print ("3")
               
                with open(path+row_name_file[0]) as csv_file:
                    print (path+row_name_file[0])
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    
                 
                    for row in csv_reader:
                        data.append(float(row[0]))
                        line_count += 0                
            except:
                print ("E1")
                continue
            
            if (row_name_file[0][:9] == 'output_m1'): 
                print ("4")
                out_fr=np.array(firingRate(data, start=100., stop=300., ch=2.)).max()
                print (out_fr)

                firing_rate_m1_learning.append(out_fr)



            if (row_name_file[0][:9]=='output_m1' or row_name_file[0][:9]=='output_io' or row_name_file[0][:9]=='output_sg'):
                print ("5")                             
                print ("Import file <= " + path+row_name_file[0] + "\n")                   
                firing_rate_area[row_name_file[0][:9]+"_"+str.replace(row_name_file[0][-6:-4],'_','')] = firingRate(data) # put firing rate into dictionary                       
                number_session.append(int(str.replace(row_name_file[0][-6:-4],'_','')))                    
                try:
                    spike_area[row_name_file[0][:9]+"_"+str.replace(row_name_file[0][-6:-4], '_', '')] = np.loadtxt(path+row_name_file[0], delimiter=',')
                except:
                    print ("E2")
                    continue
                    
                   
            row=[]
            data=[]
            line_count_name_file += 1

    
   
                                        
    for count_us in np.unique(number_session):
    
            
            print ("\n\n ========================================================================= \n")
            print ("\n\n ========================================================================= \n\n")              
            print ("====> SECTION NUMBER ---> " + str(count_us) + "\n\n")            


          
            CR =firing_rate_m1_learning[count_us]/np.array(firing_rate_m1_learning).max()*100
                              

            scriviFile(round(CR), base_path+"CR-CS_US/", "cr_medio_di_sessione_"+str(path[-14:-1])+".txt")
            
           

             
            CRp_array.append(round(CR))
            

            
    try:
        
        scriviFile(np.array(firing_rate_m1_learning).max(), base_path+"CR-CS_US/", "fr_max_mice.txt");
        
    except Exception as e:
        print ("errore => " + str(e))
                        
for i in range (0,int(sys.argv[2])):
        
    calculate_cr ('session_mice_'+str(i)+'/') 
