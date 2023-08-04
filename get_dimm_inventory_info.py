import os, time
from tabulate import tabulate
from xlrd import open_workbook

class dimm_inventory:    
    def __init__(self,inventory):
        self.book = open_workbook(inventory)
        self.dws = self.book.sheet_by_index(0)
    
    def check_ssh_connection(self):
        with open('ssh_test.txt') as f:
            try:
                ssh_result = f.readline()
                ssh_result = str(ssh_result).replace('\n','')
            except:
                print('Unable to establish SSH connection...')
                os.popen('rm ssh_test.txt')
                quit()
            os.popen('rm ssh_test.txt')
        return ssh_result
     
    def get_dmidecode_data(self):
        with open("dmidecode.txt", "r") as file:
            self.dmidecode_info = file.read()
            self.dmidecode_info = self.dmidecode_info.replace('\n','').replace('\t','')
            self.dmidecode_info = self.dmidecode_info.split('--')
        return self.dmidecode_info
    
    def get_location_serials(self):
        self.location_list = []
        self.serial_list = []
        for x in self.dmidecode_info:
            try:
                x = x.split(':')
                self.location_list.append(x[1])
                self.serial_list.append(x[7])
            except:
                pass
        for i,x in enumerate(self.serial_list):
            self.serial_list[i] = self.serial_list[i].replace(' ','')
        for i,x in enumerate(self.location_list):
            self.location_list[i] = self.location_list[i].replace('Bank Locator','').replace('_',' ').replace('DIMM','Slot')
        if '-' in self.serial_list[0]:
            for i,x in enumerate(self.serial_list):
                x = x.split('-')
                self.serial_list[i] = x[1]
        else:
            pass
        return self.location_list, self.serial_list
    
    def get_inventory_rows(self):
        rows = 0
        for x in self.dws:
            rows += 1
        return rows-1
    
    def match_info(self,serial,rows):
        row = 0
        while row <= rows:
            value = str(self.dws.cell(row,0)).replace('text:','').replace("'",'')
            if serial in value:
                self.dimm_data = (str(self.dws.cell(row,1)).replace('text:','').replace("'",'')+' | '+str(self.dws.cell(row,2)).replace('text:','').replace("'",'')+' | '+str(self.dws.cell(row,0)).replace('text:','').replace("'",'')+' | '+str(self.dws.cell(row,3)).replace('text:','').replace("'",'')+' | '+str(self.dws.cell(row,4)).replace('text:','').replace("'",''))
                break
            row += 1
        try:
            self.dimm_data = self.dimm_data
        except:
            self.dimm_data = False
        return self.dimm_data

def main():
    dimm_info = dimm_inventory('cmdb_ci_hardware.xls')
    ssh_test = dimm_info.check_ssh_connection()
    if ssh_test == '0':
        headers = 'Location,Vendor,Model,Serial Number,Barcode,Borrower'
        dmidecode_info = dimm_info.get_dmidecode_data()
        location_list, serials_list = dimm_info.get_location_serials()
        full_rows =  dimm_info.get_inventory_rows()
        with open('dimm inventory.csv','w',encoding = 'utf-8') as file:
            file.write(f'{headers} \n')
        try:
            final_table = []
            headers = headers.split(',')
            for index, x in enumerate (serials_list):
                full_dimm_info = dimm_info.match_info(x,full_rows)
                if ',' in full_dimm_info:
                    full_dimm_info = full_dimm_info.replace(',','')
                table = full_dimm_info.split("|")
                position = location_list[index]
                table.insert(0,position)
                final_table.append(table)
                with open('dimm inventory.csv','a',encoding = 'utf-8') as file:
                    full_dimm_info = full_dimm_info.replace('|',',')
                    file.write(location_list[index]+','+full_dimm_info+('\n'))
            print(tabulate(final_table, headers='\033[1m'+headers+'\033[0m', tablefmt="rounded_outline"))
            os.popen('rm dmidecode.txt')
        except:
            pass
    else:
        print('No SSH connection...')

if __name__ == "__main__":
    main() 
