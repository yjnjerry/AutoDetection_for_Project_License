#situation of multilicense 
import MySQLdb
import MySQLdb.cursors
import os
import sys
import getopt

def find_word(filename, word):
    flag = 0
    word = word
    with open(filename, 'r') as f:
        line = f.readlines()
        for i in range(1,len(line)):
	    if word.upper() in line[i].upper() or word.upper() in line[i-1].upper():
                print line[i]
                print line[i-1]
	        flag = 1
                break
    return flag

def find_license(path):
    license_flag = 0
    result_list = []
    license_addr_list = []
    for root,dirs,files in os.walk(path):
        for file in files:
            if (file.upper() == 'LICENSE' or file.upper() == 'LICENSE.TXT' or file.upper() == 'LICENSE.MD' or file.upper() == 'COPYING'):
	        tmp_list = []
                license_flag = license_flag + 1
                tmp_list.append(path)
		tmp_list.append(os.path.join(root, file))
                result_list = tmp_list
                license_addr_list.append(tmp_list)
    if (license_flag == 1):
        return result_list
    elif (license_flag == 0):
	return 0
    else:
        return license_addr_list

def path_revise(path):
    p = os.path.basename(path)
    p = "/sourcecode/" + p
    print p
    return p
"""
path = '/home/ossproject/java_code'
filelist = os.listdir(path)
for filename in filelist:
    filepath = os.path.join(path, filename)
    if os.path.isdir(filepath):
        executing(filepath)
"""
def executing(p,db_host,db_user,db_passwd,db_name,db_tableget,db_tableset):
    conn=MySQLdb.connect(host=db_host,user=db_user,passwd=db_passwd,db=db_name)
    cursor = conn.cursor()
    name_list = []
    result_list = None
    license = None
    result_list = find_license(p)
    cursor.execute('select name_without_version,simname,version from %s;' %db_tableget)
    r = cursor.fetchall()
    for row in r:
        name_list.append(row)
    if (result_list == 0):
        print 'no license file in the path'
    elif (type(result_list[0]) != list):
        tmp = 0
        for i in name_list:
            simname_ = ' ' + i[1] + ' '
            v_ = i[2] 
            if v_ == 'no':
                if (find_word(result_list[1],i[0])):
                    print simname_
                    license = i[1]
                    print result_list[1]
                    tmp = 1
                    cursor.execute("update %s set license = '%s' where location = '%s';" %(db_tableset,license, path_revise(result_list[0])))
                    conn.commit()
            else:
                if (find_word(result_list[1],i[0])) and find_word(result_list[1], v_):
                    print simname_
                    license = i[1]
                    print result_list[1]
                    tmp = 1
                    cursor.execute("update %s set license = '%s' where location = '%s';" %(db_tableset,license, path_revise(result_list[0])))
                    conn.commit()
        if tmp == 0:
            print result_list[1]
            print 'the license was not found in the path'
    else:
        tmp = 0
        license = []
        for j_list in result_list:
            for i in name_list:
                v_ = i[2]
                simname_ = ' ' + i[1] +' '
                if v_ == 'no':
                    if (find_word(j_list[1],i[0])):
                        print simname_
                        license.append(i[1])
                        print j_list[1]
                        tmp += 1
                else:
                    if(find_word(j_list[1],i[0])) and find_word(j_list[1], v_):
                        print simname_
                        license.append(i[1])
                        print j_list[1]
                        tmp += 1 
        if tmp == 0:
            print j_list[1]
            print 'the license was not found in the path'
        else: 
            license = str(list(set(license)))
            license = '\"' + license + '\"'
            print license
            print j_list[1]
            #print "update %s set license = %s where location = %s;" %(db_tableset,license, path_revise(j_list[0]))

            cursor.execute("update %s set license = %s where location = '%s';" %(db_tableset, license, path_revise(j_list[0])))
            #cursor.execute("update %s set license = '%s' where location = '%s';" %(db_tableset, license, path_revise(j_list[0])))
            conn.commit()
    cursor.close()
    conn.close()

path = ''
db_host = ''
db_user = ''
db_passwd = ''
db_name = ''
db_tableget = ''
db_tableset = '' 
try:
    opts, args = getopt.getopt(sys.argv[1:],"hi:u:p:n:g:s:a:")
except getopt.GetoptError:
    print 'python db_getlicense.py -i <databasehostip> -u <databaseuser> -p <databasepassword> -n <databasename> -g <sourcetable> -s <aimtable> -a <path>'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'python db_getlicense.py -i <databasehostip> -u <databaseuser> -p <databasepassword> -n <databasename> -g <sourcetable> -s <aimtable> -a <path>'
        sys.exit()
    elif opt == '-i':
        db_host = arg
    elif opt == '-u':
        db_user = arg
    elif opt == '-p':
        db_passwd = arg
    elif opt == '-n':
        db_name = arg
    elif opt == '-g':
        db_tableget = arg
    elif opt == '-s':
        db_tableset = arg
    elif opt == '-a':
        path = arg

#path = '/home/ossproject/java_code'
#filelist = os.listdir(path)
for projectid in range(1, 100):
    conn1 = MySQLdb.connect(host=db_host,user=db_user,passwd=db_passwd,db=db_name,cursorclass = MySQLdb.cursors.DictCursor)
    cursor1 = conn1.cursor()
    cursor1.execute("select destDir2 from %s where id = %d" %(db_tableset, projectid))
    originalpath = cursor1.fetchone()
    if(originalpath != None):
        originalpath = originalpath['destDir2']
        print originalpath
        executing(originalpath,db_host,db_user,db_passwd,db_name,db_tableget,db_tableset)
        print projectid
        projectid += 1
    else:
        projectid += 1
        continue
    cursor1.close()
    conn1.close()
    

"""for filename in filelist:
    filepath = os.path.join(path, filename)
    if os.path.isdir(filepath):
        executing(filepath,db_host,db_user,db_passwd,db_name,db_tableget,db_tableset)
"""
"""
conn=MySQLdb.connect(host='localhost',user='root',passwd='999999',db='test')
cursor = conn.cursor()
name_list = []
result_list = None
license = None
p = "/home/ossproject/java_code/1475078977808"
result_list = find_license(p)
cursor.execute('select name,simname from t_license;')
r = cursor.fetchall()
for row in r:
    name_list.append(row)
if (result_list == 0):
    print 'no license file in the path'
else:
    tmp = 0
    for i in name_list:
	if (find_word(result_list[1],i[0]) or find_word(result_list[1],i[1])):
            print i[1]
	    license = i[1]
	    print result_list[0]
            tmp = 1
            break
    if tmp == 0:
        print result_list[1]
        print 'the license was not found in the path'

cursor.execute("update t_auto_project_java set license = '%s' where location = '%s';" %(license, path_revise(result_list[0])))

conn.commit()	
cursor.close()
conn.close()
"""
