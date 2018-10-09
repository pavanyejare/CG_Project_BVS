import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","admin","bvs" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

#data1 = { 0 : '12', 1 : '231', 2 : '32', 3 : 'Pavan Yejare', 4 : '23', 5 : 'male', 6 : '2'}


def store(data) :
        
	r = data
	print r
        id = int(r[0])
        acc = int(r[1])
	vill = int(r[2])
        name = r[3]
	age = int(r[4])
        gender = r[5]
	status = int(r[6])
	sql = "insert into regi(id,accno,village,name,age,gender,finger) values (%d, %d, %d, '%s', %d, '%s', %d)" %(id, acc, vill, name, age, gender, status) 
	try:
            cursor.execute(sql)
	    db.commit()
	    print "Done"
	except:
		db.rollback()
   		print "Error: unable to fecth data"
#store(data1)
def search(id) : 
	i = int(id)
	sql1 = "select * from regi where finger=%d" %(i)
	print sql1
	try:
            cursor.execute(sql1)
            results = cursor.fetchall()
            id = results[0]
            name = row[3]
            age = row[4]
	    status = row[7]
	    data = {'id' : id, 'name' : name, 'age':age, 'status' : status}
	    if status == 0:
		new_sql = "update regi set status = 1 where finger=%d" %(i)
                cursor.execute(new_sql)
	        db.commit()
	    return(data)
 
        except:
            print "Error: unable to fecth data"


search(1)

