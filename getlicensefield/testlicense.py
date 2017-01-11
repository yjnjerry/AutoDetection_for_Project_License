import os
def getlicense(path):
    license_flag = 0
    result_list = []
    license_addr_list = []
    for root,dirs,files in os.walk(path):
        for file in files:
            if (file == 'LICENSE' or file == 'LICENSE.txt' or file == 'LICENSE.md'):
                license_flag = license_flag + 1
                result_list.append(os.path.join(root, file))
                license_addr_list.append(result_list)
    if (license_flag == 1):
        print result_list
    elif (license_flag == 0):
        print 0
    else:
        print license_addr_list
getlicense("/media/hadoop/e6d8daa4-8445-470c-9032-2b19bef434f5/javascript_code/1467772096149/")        
