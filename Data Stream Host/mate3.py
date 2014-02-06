#!/usr/bin/python
# Filename: mate3.py

#Copyright (C) 2012 Jesus Perez <jepefe@gmail.com>
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 2 of the License, or
#(at your option) any later version.
# 
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License at <http://www.gnu.org/licenses/>
#for more details.



import fmmx
import flexnetdc
import fxinv
import radian


class mate3:
    def __init__(self):
        self.matedevices = [0]*10 #Ten is the max number of devices can be connected to mate3
        self.total_devices = None
        self.fxmodifiers = False
        
    
    def enable_fx_modifiers(self):
        self.fxmodifiers = True
        
    
        
        
    def parse_raw_data(self, mate_raw_data):
        #Erase unnecessary network data
        mate_raw_data = mate_raw_data[mate_raw_data.find('<'):mate_raw_data.rfind('>')+1]
        #Every device string starts with "<" count them to get total number of connected devices
        if self.total_devices == None:
            self.total_devices = mate_raw_data.count('<')

            
      
        #Start and end of very device string
        symbol1 = mate_raw_data.find('<')+1
        symbol2 = mate_raw_data.find('>')
        devices_data = [] #Data string of each device
        datastring = []
        raw_string = mate_raw_data

        for i in range(self.total_devices):

            aux = str(raw_string[symbol1:symbol2])
            datastring.append(aux.split(','))
            devices_data.append(datastring[i])
            raw_string = raw_string[symbol2+1:len(raw_string)]
            symbol1 = raw_string.find('<')+1
            symbol2 = raw_string.find('>')
            

            
        return devices_data
    
    def process_datastream(self, raw_datastream):
        parsed = self.parse_raw_data(raw_datastream)
        for i in parsed:

            #Fx inverters
            if i[1] == '2':             
                if  self.matedevices[int(i[0])-1] == 0:
                    self.matedevices[int(i[0])-1] = fxinv.fxinv()
                    if self.fxmodifiers:
                        self.matedevices[int(i[0])-1].enable_modifiers()
                self.matedevices[int(i[0])-1].set_status(i)
                self.matedevices[int(i[0])-1].dev_address = int(i[0])
                self.matedevices[int(i[0])-1].get_values_with_names()
            
              
            
            #Fm or Mx data
            if i[1] == '3':             
                if  self.matedevices[int(i[0])-1] == 0:
                    self.matedevices[int(i[0])-1] = fmmx.fmmx()
                self.matedevices[int(i[0])-1].set_status(i)
                self.matedevices[int(i[0])-1].dev_address = int(i[0])
                
                self.matedevices[int(i[0])-1].get_values_with_names()
                
            #FlexmaxDC data
            if i[1] == '4':             
                if  self.matedevices[int(i[0])-1] == 0:
                    self.matedevices[int(i[0])-1] = flexnetdc.flexnetdc()
                self.matedevices[int(i[0])-1].set_status(i)
                self.matedevices[int(i[0])-1].dev_address = int(i[0])
                self.matedevices[int(i[0])-1].get_values_with_names()  

            #Radian inverters
            if i[1] == '6':             
                if  self.matedevices[int(i[0])-1] == 0:
                    self.matedevices[int(i[0])-1] = radian.fxinv()
                    if self.fxmodifiers:
                        self.matedevices[int(i[0])-1].enable_modifiers()
                self.matedevices[int(i[0])-1].set_status(i)
                self.matedevices[int(i[0])-1].dev_address = int(i[0])
                self.matedevices[int(i[0])-1].get_values_with_names()

               
                
    
    def get_status(self):
        
        if self.total_devices != None:
            for i in self.matedevices:
                if i != 0:
                    print '-------------'+i.name+'----------------'
                    for val in range(i.valuenames_formatted.__len__()):
                        print str(i.get_values_with_names().keys()[val])+": \t\t\t\t"+str(i.get_values_with_names().values()[val])
                        
        else:
            print "No devices found"
            
    def get_status_dict(self, address):
        address = int(address)-1
        if self.total_devices != None:
            devices_status = {}
            if address == -1:
                for i in self.matedevices:
                    if i != 0:
                        devices_status['device'+str(i.dev_address)] = i.get_values_with_names()
                return devices_status
            else:
                if self.matedevices[address] != 0:
                    return self.matedevices[address].get_values_with_names()
                else:
                    return "No devices found"
                        
            
    
    def get_device_status(self,address):
        address = int(address)-1
        if self.matedevices[address] != 0:
            status = self.matedevices[address]
            return status
        else:
            return False
    
    def get_devies_info(self):
        device_info = []
        for i in self.matedevices:
            if i != 0:
                device_info.append([i.dev_address,i.name, i.valuenames_formatted ])
        return device_info
                
                 
        
    