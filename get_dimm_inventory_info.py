import os
from xlrd import open_workbook
class dimm_info:    
    def __init__(self,inventory):
        self.book = open_workbook(inventory)
        self.hc = self.book.sheet_by_index(0)

    def get_dmidecode(self):
        with open('dmidecode.txt') as file:
            self.dmidecode_info = file.read()
            self.dmidecode_info = self.dmidecode_info.split('--')
        return self.dmidecode_info 
    
    def get_serial(self):
        self.get_serial = self.dmidecode_info
        self.serial_list = []
        for x in self.get_serial:
            serial = x.replace('Serial Number:','').replace('Asset Tag','').replace(' ','').replace('\t','').replace('\n','')
            serial = serial.split(':')
            try:    
                self.serial_list.append(serial[0])
            except:
                quit()
        return self.serial_list
    
    def get_dimm_location(self):
        self.get_dimm_location = self.dmidecode_info
        self.dimm_location = []
        for x in self.get_dimm_location:
            location = x.replace('Serial Number:','').replace('Asset Tag','').replace(' ','').replace('\t','').replace('\n','')
            location = location.split(':')    
            try:
                self.dimm_location.append(location[1])
            except:
                print("Unable to get data from server")
                quit()
        i = 0 
        while i < len(self.dimm_location):
            self.dimm_location[i] = self.dimm_location[i].replace('AssetTag','').replace('_',' ')
            i += 1
        return self.dimm_location
         
    def get_inventory_rows(self):
        rows = 0
        for x in self.hc:
            rows += 1
        return rows-1
    
    def __str__(self,serial,rows):
        row = 0
        while row <= rows:
            value = str(self.hc.cell(row,0)).replace('text:','').replace("'",'')
            if serial in value:
                self.dimm_data = (str(self.hc.cell(row,1)).replace('text:','').replace("'",'')+' | '+str(self.hc.cell(row,2)).replace('text:','').replace("'",'')+' | '+str(self.hc.cell(row,0)).replace('text:','').replace("'",'')+' | '+str(self.hc.cell(row,3)).replace('text:','').replace("'",'')+' | '+str(self.hc.cell(row,4)).replace('text:','').replace("'",''))
                break
            row += 1
        try:
            self.dimm_data = self.dimm_data
        except:
            self.dimm_data = False
        return self.dimm_data

def main():
    get_dimm_info = dimm_info('cmdb_ci_hardware.py')
    get_dmidecode = get_dimm_info.get_dmidecode()
    get_serial= get_dimm_info.get_serial()  
    get_location = get_dimm_info.get_dimm_location()
    get_rows =  get_dimm_info.get_inventory_rows()
    for index, x in enumerate (get_serial):
        full_dimm_info = get_dimm_info.__str__(x,get_rows)
        print(get_location[index]+'| '+full_dimm_info)

if __name__ == "__main__":
    main()
    