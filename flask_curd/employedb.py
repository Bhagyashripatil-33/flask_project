import sqlite3
con=sqlite3.connect('Employees.db')
print("successfuly opend")
s='create table Employee(id int primary key ,name varchar(20) not null,sal int not null)'
con.execute(s)
print('table created sucessfully')
con.close()
