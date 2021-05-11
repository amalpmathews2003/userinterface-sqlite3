from tkinter import *
import sqlite3
import time
class interface(Tk):

	def __init__(self):
		super().__init__()
		self.title('SqlLite3')
		self.geometry('720x720')
		Label(self,text="Database Name ").grid(row=0,column=0)
		global database_name
		database_name=Entry(self,width=30)
		database_name.grid(row=0,column=1,padx=10,pady=10)
		show_database_btn=Button(self,text="Show Databases",command=None).grid(row=1,column=0,padx=10,pady=10)
		create_database_btn=Button(self,text="Create Database In working directory",command=lambda:self.create_databases(database_name.get())).grid(row=2,column=0,padx=10,pady=10)
		use_database_btn=Button(self,text="Use Database",command=lambda:self.use_database(database_name.get())).grid(row=3,column=0,padx=10,pady=10)

	def show_databases(self):
		return

	def create_databases(self,db_name):
		
		if db_name=='':
			root=Toplevel()
			Label(root,text="Enter database name in previous window").grid(row=0,column=0,padx=10,pady=10)
			return	

		conn=None
		try:
			conn=sqlite3.connect(db_name)
		except Error as e:
			print(e)
		finally:
			if conn:
				conn.commit()
				conn.close
		database_name.delete(0,END)
		database_name.insert(0,'Database created')
		return
	def use_database(self,db_name):
		root=Toplevel(self)
		root.title(db_name)
		if db_name=='':
			Label(root,text="Enter database name in previous window").grid(row=0,column=0,padx=10,pady=10)
			return
		root.geometry('720x720')
		Label(root,text="Table Name ").place(x=150,y=5)
		global table_name
		table_name=Entry(root,width=30)
		table_name.pack()
		Button(root,text="Show Tables",command=lambda:self.show_tables(db_name)).pack(padx=10,pady=10)
		Button(root,text="Create Table",command=lambda:self.create_tables(db_name)).pack(padx=10,pady=10)
		Button(root,text="Delete Table",command=lambda:self.delete_tables(db_name,table_name.get())).pack(padx=10,pady=10)
		Button(root,text="Use Table",command=lambda:self.use_table(db_name,table_name.get())).pack(padx=10,pady=10)
		return

	def show_tables(self,db_name):
		conn=sqlite3.connect(db_name)
		c=conn.cursor()
		c.execute("SELECT name FROM sqlite_master WHERE type='table';")
		names=c.fetchall()
		conn.close()
		new_window=Toplevel()
		#new_window.geometry('180x180')
		Label(new_window,text=names).pack()
		return

	def create_table(self,db_name,command):
		try:
			conn=sqlite3.connect(db_name)
			c=conn.cursor()
			c.execute(command)
		except Error as e:
			print(e)
		conn.commit()
		conn.close()
		return


	def create_fields(self,e1,e2,b2):
		field=(e1.get(),e2.get())
		b2.destroy()
		table_info.extend(field)
		return
	def create_entries(self,ro):
		global r
		r+=1
		e1=Entry(ro)
		e1.grid(row=r,column=0,padx=10,pady=10)
		e2=Entry(ro)
		e2.grid(row=r,column=1,padx=10,pady=10)
		global b1
		b1.grid(row=r,column=3)
		b2=Button(ro,text="Ok",command=lambda:self.create_fields(e1,e2,b2))
		b2.grid(row=r,column=2)
		return 

	def submit(self,root,db_name):
		global table_info
		root.destroy()
		name=table_name.get()
		command="create table "+name+" ("
		i=0
		for i in range(0,len(table_info)-1,i+2):
			if i>=2 and i<=len(table_info):
				command+=','
			command+=(str(table_info[i])+" "+str(table_info[i+1]))
		command+=");"
		self.create_table(db_name,command)
		return
	def create_tables(self,db_name):
		root=Toplevel()
		name=None
		name=table_name.get()
		if name=='':
			Label(root,text="Enter table name in previous window").grid(row=0,column=0,padx=10,pady=10)
			return

		root.title("Create "+name+" in "+db_name)
		root.geometry('720x720')
		global table_info
		table_info=[]
		global r
		r=1
		c=0
		l1=Label(root,text="Field Name")
		l1.grid(row=0,column=0,padx=10,pady=10)
		l2=Label(root,text="Datatype",padx=10,pady=10)
		l2.grid(row=0,column=1)
		global b1
		b1=Button(root,text="New Entry",command=lambda:self.create_entries(root))
		b1.grid(row=2,column=r)

		b4=Button(root,text="submit",command=lambda:self.submit(root,db_name))
		b4.place(x=600,y=600)
		self.create_entries(root)
		root.mainloop()
		return
	def delete_tables(self,db_name,table_name):
		conn=sqlite3.connect(db_name)
		c=conn.cursor()
		c.execute("drop table "+table_name)
		conn.commit()
		conn.close()
		return
		
	def use_table(self,db_name,table_name):
		w1=Toplevel(self)
		w1.title(table_name)
		w1.geometry('720x720')
		b1=Button(w1,text="Show schema of "+table_name,command=lambda:self.schema_table(db_name,table_name))
		b2=Button(w1,text="Select * "+table_name,command=lambda:self.show_full_table(db_name,table_name))
		b3=Button(w1,text="Insert to "+table_name,command=lambda:self.insert_table(db_name,table_name))
		b4=Button(w1,text="Select some from "+table_name,command=lambda:self.select_some_table(db_name,table_name))
		b5=Button(w1,text="Update query in "+table_name,command=lambda:self.Update_query_table(db_name,table_name))
		b1.pack(padx=10,pady=10)
		b2.pack(padx=10,pady=10)
		b3.pack(padx=10,pady=10)
		b4.pack(padx=10,pady=10)
		b5.pack(padx=10,pady=10)
		#b1.pack(padx=10,pady=10)
		return
	def schema_table(self,db_name,table_name):
		conn=sqlite3.connect(db_name)
		c=conn.cursor()
		c.execute("pragma table_info('"+table_name+"');")
		desc=c.fetchall()
		conn.close()
		description=Tk()
		description.title('Schema of table_name')


		heads=['cid','name','type','not_null','dflt_val','pk']

		for i in range(len(heads)):
			e=Entry(description)
			e.grid(row=0,column=i,padx=5,pady=5)
			e.insert(END,str(heads[i]))

		for i in range(len(desc)):
			for j in range(6):
					e=Entry(description)
					e.grid(row=i+1,column=j,padx=5,pady=5)
					e.insert(END,str(desc[i][j]))

		return

	def show_full_table(self,db_name,table_name):
		conn=sqlite3.connect(db_name)
		c=conn.cursor()
		c.execute("pragma table_info('"+table_name+"');")
		heads=c.fetchall()
		c.execute("select *,oid from "+table_name)
		desc=c.fetchall()
		conn.close()
		show=Toplevel()
		show.title(table_name)
		for i in range(len(heads)):
			e=Entry(show,font='bold')
			e.grid(row=0,column=i,padx=5,pady=5)
			e.insert(END,str(heads[i][1]))
		e=Entry(show,font='bold')
		e.grid(row=0,column=len(heads),padx=5,pady=5)
		e.insert(END,'oid')
		for i in range(len(desc)):
			for j in range(len(desc[i])):
				e=Entry(show)
				e.grid(row=i+2,column=j,padx=5,pady=5)
				e.insert(END,str(desc[i][j]))

		return
	def insert_table(self,db_name,table_name):
		conn=sqlite3.connect(db_name)
		c=conn.cursor()
		c.execute("pragma table_info('"+table_name+"');")
		heads=c.fetchall()
		conn.close()
		sho=Toplevel()
		sho.title(table_name)
		heads_names=[]
		insert_info=[]
		i=0
		for i in range(len(heads)):
			e=Entry(sho)
			e.grid(row=0,column=i,padx=5,pady=5)
			e2=Entry(sho)
			e2.grid(row=1,column=i,padx=5,pady=5)
			insert_info.append(e2)
			e.insert(END,str(heads[i][1]))
			heads_names.append((heads[i][1],heads[i][2]))
		Button(sho,text="Insert",command=lambda:self.insert_to_table(db_name,table_name,insert_info,heads_names,sho)).grid(row=i,column=0)
		return
	def insert_to_table(self,db_name,table_name,insert_info,heads,sho):
		command="insert into "+table_name+" ("

		for i in range(len(insert_info)):
			if insert_info[i].get():
				if i>=1 and i<=len(insert_info)-1:
					command+=","
				command+=heads[i][0]
		command+=") values("

		for i in range(len(insert_info)):
			if insert_info[i].get():
				if i>=1 and i<=len(insert_info)-1:
					command+=','
				if heads[i][1]=="integer":
					command+=insert_info[i].get()
				elif heads[i][1]=="text":
					command+="'"+insert_info[i].get()+"'"
		command+=");"
		conn=sqlite3.connect(db_name)
		c=conn.cursor()
		c.execute(command)
		conn.commit()
		conn.close()
		for i in insert_info:
			i.delete(0,END)
		return
	def select_some_table(self,db_name,table_name):
		sel=Toplevel()
		sel.title(table_name)
		Label(sel,text="Tick required columns").grid(row=0,column=0,padx=10,pady=10)
		conn=sqlite3.connect(db_name)
		c=conn.cursor()
		c.execute("pragma table_info('"+table_name+"');")
		heads=c.fetchall()
		#print(heads)
		selected=[]
		for i in range(len(heads)):
			c=StringVar()
			Checkbutton(sel,text=heads[i][1],variable=c,onvalue=heads[i][1],offvalue=None).grid(row=i+1,column=0,padx=10,pady=10)
			selected.append(c)
		c=StringVar()
		Checkbutton(sel,text="oid",variable=c,onvalue="oid",offvalue=None).grid(row=len(heads)+1,column=0,padx=10,pady=10)
		selected.append(c)

		Button(sel,text="Show",command=lambda:self.show_some_table(db_name,table_name,selected)).grid(row=len(heads)+3,column=0)
		sel.mainloop()
		return

	def select_fields(self,check):
		s=''
		for i in range(len(check)):
			if check[i].get():
				s+=check[i].get()
				s+=','
		s=s[:-1]
		return s
	def show_some_table(self,db_name,table_name,selected):
		s=self.select_fields(selected)
		#print(s)
		conn=sqlite3.connect(db_name)
		c=conn.cursor()
		command="select " +s+ " from "+table_name
		c.execute(command)
		s=c.fetchall()
		conn.close()
		win2=Toplevel()
		win2.title(table_name)
		for i in range(len(selected)):
			if selected[i].get():
				e=Entry(win2,font='bold')
				e.insert(END,selected[i].get())
				e.grid(row=0,column=i)

		for i in range(len(s)):
			for j in range(len(s[0])):
				e=Entry(win2)
				e.insert(END,str(s[i][j]))
				e.grid(row=i+1,column=j,padx=5,pady=5)
		return

	def select_oid(self,db_name,table_name,e1,w2):
		oid=e1.get()
		conn=sqlite3.connect(db_name)
		c=conn.cursor()
		c.execute("pragma table_info('"+table_name+"');")
		heads=c.fetchall()
		c.execute("select * from "+table_name+" where oid="+oid)
		details=c.fetchall()
		conn.close()
		entries=[]
		for i in range(len(heads)):
			e1=Entry(w2)
			e1.grid(row=2,column=i)
			e1.insert(END,heads[i][1])
			e2=Entry(w2)
			e2.grid(row=3,column=i)
			e2.insert(END,details[0][i])
			entries.append((e1,e2))

		Button(w2,text="Save query",command=lambda:self.update_query(db_name,table_name,heads,entries,oid)).grid(row=4,column=0,ipadx=10)
	def Update_query_table(self,db_name,table_name):
		w2=Toplevel()
		w2.title('Update '+table_name)
		Label(w2,text="oid").grid(row=0,column=0,padx=10,pady=10)
		e1=Entry(w2)
		e1.grid(row=0,column=1,padx=10,pady=10)
		Button(w2,text="show",command=lambda:self.select_oid(db_name,table_name,e1,w2)).grid(row=0,column=2,padx=10,pady=10)
		return

	def update_query(self,db_name,table_name,heads,entries,oid):
		command="update "+table_name+" set "
		for i in range(len(entries)):
			if heads[i][2]=='text':
				command+=entries[i][0].get()+"='"+entries[i][1].get()+"'"
			if heads[i][2]=='integer':
				command+=entries[i][0].get()+"="+entries[i][1].get()+""
			if i>=0 and i<len(entries)-1:
				command+=','

		command+=" where oid="+oid+";"
		conn=sqlite3.connect(db_name)
		c=conn.cursor()
		c.execute(command)
		conn.commit()
		conn.close()
		for i in range(len(entries)):
			entries[i][1].delete(0,END)




