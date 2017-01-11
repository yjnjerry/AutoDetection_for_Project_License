import sys
import os
import MySQLdb
import MySQLdb.cursors
import getopt

license_address_set = []
license_set = []
filepath = ''
#input a file path, output all the paths of license which are affecting the file

#findlicense("/media/hadoop/e6d8daa4-8445-470c-9032-2b19bef434f5/javascript_code/1467783486342/gulp-build-project-master/gulp/node_modules/gulp-uglify/node_modules/gulp-util/node_modules/lodash._reescape/index.js")
def find_word(path,word):
    flag = 0
    with open(path, 'r') as f:
        line = f.readlines()
        for i in range(1,len(line)):
            if word.upper() in line[i].upper() or word.upper() in line[i-1].upper():
                #print line[i]
                #print line[i-1]
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
        simname_ = ' ' + i[1] + ' '
        v_ = i[2]
        if v_ == 'no':
            if (find_word(path,i[0])):
               # print simname_
                license_list.append(simname_)
        else:
            if (find_word(path,i[0])) and find_word(path,v_):
               #print simname_
                license_list.append(simname_)
    return license_list

def findlicense(path):
    p = os.path.dirname(path)
    #print p
    for i in os.listdir(p):
        if ( i.upper() == 'LICENSE' or i.upper() == "LICENSE.TXT" or i.upper() == "LICENSE.MD" or i.upper() == "COPYING"):
            tmp = os.path.join(p,i)
            #print tmp
            license = getlicense(tmp)
            #print os.path.join(p,i)
            license_set.append(license) 
            license_address_set.append(os.path.join(p,i))
    q=p
    #print q.split("/")[len(q.split("/"))-1]
    #if (p != "/media/hadoop/e6d8daa4-8445-470c-9032-2b19bef434f5/javascript_code"):
    if (len(q.split("/")) != 5 ): 
        findlicense(p)
    else: 
        print (str(license_address_set))
        print (str(license_set))
#p = getlicense("/media/hadoop/e6d8daa4-8445-470c-9032-2b19bef434f5/javascript_code/1467767826088/cloudbreak-blueprint-response-status/LICENSE")
#print p

try:
    opts, args = getopt.getopt(sys.argv[1:],"hp:")
except getopt.GetoptError:
    print 'python getlicensefield.py -p <filepath>'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'python getlicensefield.py -p <filepath>'
        sys.exit()
    elif opt == '-p':
        filepath = arg

findlicense(filepath)
