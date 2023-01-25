import os, time, subprocess
from datetime import date
from collections import Counter

class dimm_inventory:    
    def __init__(self,inventory):
        proxy = 'http://proxy-us.intel.com:911'
        try:
            from xlrd import open_workbook
        except:
            with open('libs.sh','w') as bash_file:
                bash_file.write('export http_proxy='+proxy+'\n'+'export https_proxy='+proxy+'\n'+'pip install xlrd\n'+'pip install tqdm\n'+'unset http_proxy\nunset https_proxy')
            os.system('chmod 777 libs.sh \n ./libs.sh')
            time.sleep(3.5)
            os.system('rm libs.sh \n clear')
        from xlrd import open_workbook
        self.book = open_workbook(inventory)
        self.dws = self.book.sheet_by_index(0)
    
    def check_ssh_connection(self):
        with open('ssh_test.txt') as f:
            try:
                ssh_result = f.readline()
                ssh_result = str(ssh_result).replace('\n','')
            except:
                print('Unable to establish SSH connection...')
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
            self.location_list[i] = self.location_list[i].replace('Bank Locator','').replace('_',' ')
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
    
    def get_node_name(self):
        try:
            self.user = subprocess.check_output('pwd')
            self.user = str(self.user)
            self.user = self.user.split('/')
            self.user = self.user[2] 
            with open('node.txt','r') as node_file:
                self.node = node_file.read()
                self.node = self.node.replace('\n','')
        except:
            self.node = 'Unable to get node name'
        return self.user, self.node
    
    def get_ticket_number(self):
        try:
            with open('pool.txt','r') as pool_file:
                self.ticket_number = pool_file.read()
                self.ticket_number = self.ticket_number.split('_')
                self.ticket_number = self.ticket_number[-2]
                try:
                    self.ticket_number = self.ticket_number.split('-')
                    self.ticket_number = self.ticket_number[-1]
                    self.ticket_number = int(self.ticket_number)    
                except:
                    pass
                if type(self.ticket_number) == int:
                    self.ticket_number = 'ASCGA-'+str(self.ticket_number)
                else:
                    self.ticket_number = 'Not in manintenance pool' 
        except:
            self.ticket_number = 'Unable to get ticket number'
            
        return self.ticket_number    
    
    
def main():
    dimm_info = dimm_inventory('cmdb_ci_hardware.py')
    ssh_test = dimm_info.check_ssh_connection()
    if ssh_test == '0':
        user, node = dimm_info.get_node_name()
        ticket_number = dimm_info.get_ticket_number()
        dmidecode_info = dimm_info.get_dmidecode_data()
        location_list, serials_list = dimm_info.get_location_serials()
        full_rows =  dimm_info.get_inventory_rows()
        with open('dimm inventory.csv','w',encoding = 'utf-8') as file:
            file.write('Location,Vendor,Model,Serial Number,Barcode,Borrower'+'\n')
        try:
            models = []
            for index, x in enumerate (serials_list):
                full_dimm_info = dimm_info.match_info(x,full_rows)
                if ',' in full_dimm_info:
                    full_dimm_info = full_dimm_info.replace(',','')
                print(location_list[index]+' | '+full_dimm_info)
                with open('dimm inventory.csv','a',encoding = 'utf-8') as file:
                    full_dimm_info = full_dimm_info.replace('|',',')
                    file.write(location_list[index]+','+full_dimm_info+('\n'))
                full_dimm_info = full_dimm_info.split(',')
                models.append(full_dimm_info[1])
            counter = Counter(models)
            common_models = ([ [k,]*v for k,v in counter.items()])
            for index, i in enumerate(common_models):
                num_of_models = len(common_models)
                i = str(i[index])
                i = i.replace('/n','')  
                with open('tracker.csv','a') as file:
                    file.write(str(date.today())+','+str(len(common_models[index]))+','+i+','+ticket_number+','+','+str(len(common_models[index]))+',,'+user+','+node+'\n')
                    file.close()
        except:
            pass
    else:
        print('No SSH connection...')

if __name__ == "__main__":
    main() 
