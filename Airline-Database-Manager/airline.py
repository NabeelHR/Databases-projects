import mysql.connector
import re
import traceback


admin = ("admin", "azsx123")
receptionist = ("recep", "lolpo")

def display_flights(flights):
	w=15
	print("_______________________________________________________________________________________________________________________________")
	print ("FLIGHT_ID".ljust(w), "Date".ljust(w), "Departing Time".ljust(w), "Arrival Time".ljust(w), "Take Off".ljust(w), "Destination".ljust(w), "Ticket Fare".ljust(w), "Airplane".ljust(w))
	print("_______________________________________________________________________________________________________________________________")
	w=16
	if len(flights) == 0:
		print ("no flights  available :(")
	for flight in flights:
		for val in flight:
			2
#			print(str(val).ljust(w), end='')
		print ('\n')
	print("_______________________________________________________________________________________________________________________________")

def display_passengers(bois):
	w=29
	print("__________________________________________________________________________________________________________________________________")
	print ("CNIC number".ljust(w), "Name".ljust(w), "Nationality".ljust(w), "Address".ljust(w), "Phone Number".ljust(w))
	print("__________________________________________________________________________________________________________________________________")
	w=30
	if len(bois) == 0:
		print ("no boises  available :(")
	for lad in bois:
		for val in lad:
			print(str(val).ljust(w), end='')
		print ('\n')
	print("__________________________________________________________________________________________________________________________________")

def display_tickets(tickets):
	w = 13
	print("_______________________________________________")
	print("****".ljust(w), "CNIC number".ljust(w), "Flight ID".ljust(w), "****")
	print("_______________________________________________")
	w = 14
	for ticket in tickets:
		print("****".ljust(w), end='')
		for val in ticket:
			print(str(val).ljust(w), end='')
		print ("****",'\n')
	print("_______________________________________________")

################################################################
## THE FOLLOWING ARE FUNCTIONS FOR THE RECEPTIONIST USE CASES ##
################################################################
def receptionist_options():
	print("Pick an option from the following:\n",
		"A) Enter a new passenger record \n",
		"B) Update an existing passenger's details\n",
		"C) Find all flights between two dates between 2 citites\n",
		"D) Generate a new ticket for a passenger\n",
		"E) Find the cheapest flight between 2 citites\n",
		"F) View flight history for a certain passenger\n",
		"G) Cancel a particular ticket\n",
		"OR PRESS Q to quit anytime!\n"
		)

def new_passenger(cursor):
	query = "INSERT INTO passenger VALUES (%s, %s, %s, %s, %s)"
	try:
		cnic = int(input('Enter CNIC: '))
		name = input('Enter full name: ')
		nationality = input ('Enter nationality: ')
		address = input ('Enter address: ')
		phone = int(input ('Enter phone number: '))

		cursor.execute(query, (cnic, name, nationality, address, phone))
		print("Entry appended successfully!")
	except:
		print("Pls ensure correct formatting and try again!")

def update_passenger_options():
	print("Choose from the following\n",
		"1) Update Name\n",
		"2) Update Nationality\n",
		"3) Update address\n",
		"4) Update Phone number\n",
		)

def update_name(cursor, cnic_id):
	new_name = input("Enter new name you wish to update: ")
	query = "UPDATE passenger SET full_name = '%s' WHERE cnic = %s" % (new_name, cnic_id)
	cursor.execute(query)

def update_nationality(cursor, cnic_id):
	new_nation = input("Enter new nationality you wish to update: ")
	query = "UPDATE passenger SET nationality = '%s' WHERE cnic = '%s'" % (new_nation, cnic_id)
	cursor.execute(query)

def update_address(cursor, cnic_id):
	new_add = input("Enter new address you wish to update: ")
	query = "UPDATE passenger SET address = '%s' WHERE cnic = %s" % (new_add, cnic_id)
	cursor.execute(query)

def update_phone(cursor, cnic_id):
	new_phone = input("Enter new phone number you wish to update: ")
	query = "UPDATE passenger SET phone = '%s' WHERE cnic = %s" % (new_phone, cnic_id)
	cursor.execute(query)

def flights_bw_dates(cursor):
	dept_city = input("Departing from: ")
	arr_city = input("Destination: ")
	print("Use yy-mm-dd format")
	dept_date = input('View flights starting from date: ')
	arr_date = input('Till date: ')
	query = "SELECT * FROM flight WHERE (flight_date BETWEEN '%s' AND '%s') AND departure_airport = '%s' AND arrival_airport = '%s'" % (dept_date, arr_date, dept_city, arr_city)
	cursor.execute(query)
	display_flights(cursor.fetchall())

def new_ticket(cursor):
	print("Make sure both the flight and passenger already exist in database",
		"you cannot book a flight that doesn't exist")
	cnic_id = input("Enter cnic of person you wish to book a ticket for: ")
	flight_no = input("Enter flight number you wish to book: ")
	query = "INSERT INTO ticket VALUES (%s, '%s')" % (cnic_id, flight_no);
	cursor.execute(query)
	print("Ticket booked!!!")

def cheapest_flight(cursor):
	dept_city = input("View flights departing from: ")
	arr_city = input("Destination: ")
	query = "SELECT * FROM flight WHERE departure_airport = '%s' AND arrival_airport = '%s' ORDER BY fare ASC LIMIT 1" % (dept_city, arr_city)
	cursor.execute(query)
	display_flights(cursor.fetchall())

def flight_history(cursor):
	cnic_id = input("Enter CNIC number of customer to view their flight history: ")
	query = "SELECT * FROM flight WHERE flight_date < cast(now() as date) AND flight_id IN (SELECT flight_id FROM ticket WHERE cnic = '%s') " %(cnic_id)
	cursor.execute(query)
	display_flights(cursor.fetchall())

def cancel_ticket(cursor):
	print("Make sure that ticket already exists in database you can't cancel a ticket that doesn't exist")
	cnic_id = input("Enter CNIC number of customer to cancel their flight: ")
	flight_no = input("Enter flight number to cancel the ticket: ")
	query = "DELETE FROM ticket WHERE cnic = %s AND flight_id = '%s'" % (cnic_id, flight_no)
	cursor.execute(query)

#################################################################
## THE FOLLOWING ARE FUNCTIONS FOR THE ADMINISTRATOR USE CASES ##
#################################################################
def admin_options():
	print("Pick an option from the following:\n",
		"A) Add a new flight record\n",
		"B) Update details of a previously registered flight record\n",
		"C) Cancel a previously registered flight record\n",
		"D) View all flights landing and taking off from a city today\n",
		"E) View all data records\n",
		"OR PRESS Q to quit anytime!\n"
		)

def new_flight(cursor):
	query = "INSERT INTO flight VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
	try:
		flight_id = input('Enter flight_id: ')
		f_date = input('Enter flight date: ')
		dept_time = input('Enter time of departure: ')
		arr_time = input('Enter time of arrival: ')
		dept_city = input('Enter city for take off: ')
		arr_city = input('Enter destination city: ')
		fare = int(input('Enter ticket price: '))
		plane = input('Enter Airplane code: ')

		cursor.execute(query, (flight_id, f_date, dept_time, arr_time, dept_city, arr_city, fare, plane))
		print("Entry appended successfully!")
	except:
		print("Pls ensure correct formatting and try again!")
def update_flight_options():
	print("Choose from the following\n",
		"1) Update Date\n",
		"2) Update Departure Time\n",
		"3) Update Arrival Time\n",
		"4) Update Departure Airport\n",
		"5) Update Arrival Airport\n",
		"6) Update Ticket Price\n",
		"7) Update Airplane Model\n",
		)
def update_date(cursor, flight_no):
	new_date = input("Enter new date you wish to update: ")
	query = "UPDATE flight SET flight_date = '%s' WHERE flight_id = '%s'" % (new_date, flight_no)
	cursor.execute(query)

def update_dept_time(cursor, flight_no):
	new_time = input("Enter new time you wish to update: ")
	query = "UPDATE flight SET departure_time = '%s' WHERE flight_id = '%s'" % (new_time, flight_no)
	cursor.execute(query)

def update_arr_time(cursor, flight_no):
	new_time = input("Enter new time you wish to update: ")
	query = "UPDATE flight SET arrival_time = '%s' WHERE flight_id = '%s'" % (new_time, flight_no)
	cursor.execute(query)

def update_dept_city(cursor, flight_no):
	new_city = input("Enter new city you wish to update: ")
	query = "UPDATE flight SET departure_airport = '%s' WHERE flight_id = '%s'" % (new_city, flight_no)
	cursor.execute(query)

def update_arr_city(cursor, flight_no):
	new_city = input("Enter new city you wish to update: ")
	query = "UPDATE flight SET arrival_airport = '%s' WHERE flight_id = '%s'" % (new_city, flight_no)
	cursor.execute(query)
def update_ticket_price(cursor, flight_no):
	new_fare = input("Enter new price you wish to update: ")
	query = "UPDATE flight SET fare = '%s' WHERE flight_id = '%s'" % (new_fare, flight_no)
	cursor.execute(query)

def update_plane(cursor, flight_no):
	new_plane = input("Enter new airplane you wish to update: ")
	query = "UPDATE flight SET arrival_airport = '%s' WHERE flight_id = '%s'" % (new_plane, flight_no)
	cursor.execute(query)

def cancel_flight(cursor):
	print("Make sure that the flight already exists in the database")
	flight_no = input("Enter ID of flight that you wish to cancel: ")
	query = "DELETE FROM ticket WHERE flight_id = '%s'" % (flight_no)
	cursor.execute(query)
	query = "DELETE FROM flight WHERE flight_id = '%s'" % (flight_no)
	cursor.execute(query)

def view_flights(cursor):
	city = input("Enter Airport code to check for a specific day's flights: ")
	f_date = input("Enter date to check flights (enter 'today' to check for today's flights): ")
	if f_date == "today":
		f_date = "cast(now() as date))"
	query = "SELECT * from flight WHERE (flight_date = '%s') AND (departure_airport = '%s' OR arrival_airport = '%s') " % (f_date, city, city)
	cursor.execute(query)
	display_flights(cursor.fetchall())

def view_tables(cursor):
	print ("<------------		PASSENGERS TABLE   ------------>")
	cursor.execute("SELECT * FROM passenger")
	display_passengers(cursor.fetchall())
	print ("<------		FLIGHTS TABLE     ------------>")
	cursor.execute("SELECT * FROM flight")
	display_flights(cursor.fetchall())
	print ("<-----	TICKETS TABLE ----->")
	cursor.execute("SELECT * FROM ticket")
	display_tickets(cursor.fetchall())

#############################################
###### MAIN FUCTION (MENU LMAO REALLY) ######
#############################################
def main():
	mydb = mysql.connector.connect(
		host = "localhost",
		user = "root",
		passwd = "",
		database = "AIRLINE"
	)
	mycursor = mydb.cursor()
	print(" ###############################################################\n",
		"##################### HELLO AND WELCOME #######################\n",
		"###############################################################\n")
	print("Now enter login details")
	authentication = 0
	while authentication == 0:
		username = input("Enter username: ")
		pwd = input("Enter password: ")
		if (username, pwd) == admin:
			authentication = 2
		elif (username, pwd) == receptionist:
			authentication = 1
		else:
			print ("login failed\nTry again sweaty\n----------------------")
		print("----------------------")
	print("LOGIN SUCCESSFUL")

	if authentication == 1: ## USER HAS RECEPTIONIST LEVEL PRIVELEGES
		switcher = {
			'A': new_passenger,
			# option B handled elsewhere
			'C': flights_bw_dates,
			'D': new_ticket,
			'E': cheapest_flight,
			'F': flight_history,
			'G': cancel_ticket
			} 
		entry = ''
		while (1):
			print ("\n\n\n********************************")
			receptionist_options()
			entry = input()
			if re.search('^[A-G]|Q$', entry) == None:
				continue
			if entry == 'Q':
				break

			if entry == 'B': #UPDATE PASSENGER RECORD
				update_passenger_options()
				entry = int(input())
				updates = {
					1: update_name,
					2: update_nationality,
					3: update_address,
					4: update_phone,
				}
				try:
					cnic_id = input("Enter cnic of passenger you wish to update: ")
					updates[entry](mycursor, cnic_id)
				except:
					print("ERROR, invalid entry")
			else:
				try:
					switcher[entry](mycursor)## handles request
				except:
					print("INVALID ENTRIES")
					traceback.print_exc()
	
			mydb.commit()
			print("Press any key continue")
			input()
	else: #Authentication level 2 => ADMIN
		switcher = {
			'A': new_flight,
			#'B': option B to update flight handled elsewhere
			'C': cancel_flight,
			'D': view_flights,
			'E': view_tables,
			}
		entry = ''
		while (1):
			print ("\n\n\n********************************")
			admin_options()
			entry = input()
			if re.search('^[A-E]|Q$', entry) == None:
				print("Incorrect Entry")
				continue
			if entry == 'Q':
				break
			if entry == 'B': #UPDATE FLIGHT RECORD
				update_flight_options()
				entry = int(input())
				updates = {
					1: update_date,
					2: update_dept_time,
					3: update_arr_time,
					4: update_dept_city,
					5: update_arr_city,
					6: update_ticket_price,
					7: update_plane, 
				}
				try:
					flight_id = input("Enter ID of flight you wish to update: ")
					updates[entry](mycursor, flight_id)
				except:
					print("ERROR, invalid entry")
			else:
				try:
					switcher[entry](mycursor)
				except:
					traceback.print_exc()
					print("INVALID ENTRIES")
			mydb.commit()
			print("Press any key continue")
			input()

	# mycursor.execute("SELECT * FROM passenger")
	# display_passengers(mycursor.fetchall())

	# mycursor.execute("SELECT * FROM flight")
	# display_flights(mycursor.fetchall())

	# mycursor.execute("SELECT * FROM ticket")
	# display_tickets(mycursor.fetchall())


if __name__ == "__main__":
	main()