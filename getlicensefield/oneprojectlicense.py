import sys
import os
import MySQLdb
import MySQLdb.cursors
import getopt

projectpath = '' 		

def find_word(path,word):
    flag = 0
    with open(path, 'r') as f:
        line = f.readlines()
        for i in range(1,len(line)):
            if word.upper() in line[i].upper() or word.upper() in line[i-1].upper():
                #print line[i]
               # print line[i-1]
                flag = 1
                break
    return flag

def getlicense(path):
    conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="codeclone")
    cursor = conn.cursor()
    license_list = []
    name_list = []
    cursor.execute('select name_without_version,simname,version from t_license;')
    r = cursor.fetchall()
    for row in r:
        name_list.append(row)
    #print name_list
    for i in name_list:
        simname_ = i[1]
        v_ = i[2]
        if v_ == 'no':
            if (find_word(path,i[0])):
                #print simname_
                license_list.append(simname_)
        else:
            if (find_word(path,i[0])) and find_word(path,v_):
                #print simname_
                license_list.append(simname_)
    return license_list

def findlicense(path):
    license_addr_list = []
    for root,dirs,files in os.walk(path):
        for file in files:
            if (file.upper() == 'LICENSE'  or file.upper() == 'LICENSE.TXT' or file.upper() == 'LICENSE.MD' or file.upper() == 'COPYING'):
                license_addr_list.append(os.path.join(root,file))
    return license_addr_list

def getprojectlicense(path):
    license_list = []
    license_addr_list = findlicense(path)    
    for addr in license_addr_list:
        tmp_list = getlicense(addr)
        license_list = list(set(license_list).union(set(tmp_list)))
    #print license_addr_list
    #print license_list
    for i in license_list:
        print i
    return license_list

try:
    opts, args = getopt.getopt(sys.argv[1:],"hp:")
except getopt.GetoptError:
    print 'python getlicensefield.py -p <projectpath>'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'python getlicensefield.py -p <projectpath>'
        sys.exit()
    elif opt == '-p':
        projectpath = arg

getprojectlicense(projectpath)
    
