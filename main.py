import sqlite3
import time
import sys
from datetime import datetime, timedelta

# Connect to SQLite database
conn = sqlite3.connect("library2.db") 
cursor = conn.cursor()
userid = 0

def confirm(opt):
    match opt.lower():
        case 'y' | 'yes':
            return 'y'
        case 'n' | 'no':
            return 'n'
        case _:
            return 0

def isMenu(opt):
    match opt.lower():
        case 'm' | 'menu' | '0':
            return 1
        case _:
            return 0
    
def isQ(opt):
    match opt.lower():
        case 'q' | 'quit':
            return 1
        case _:
            return 0

def quit():
    print("👋 Quiting the Library System. Bye~ 👋\n")
    time.sleep(0.3)
    
    sys.exit()

def com(): 
    conn.commit()

# helper function for option 1
def output_Item(term):
    # Fetch query results inside the function
    rows = cursor.fetchall()

    # Length of table's border line
    lineLen = 90
    if term == "ISBN":
        lineLen = 110

    # Check whether has match from query
    # If at least one match
    if rows:
        ret = 1
        print()
        if term != "all":
            print("Filtered Items Result:")
        else:
            print("All Items List:")
            
        # Table labels
        print("=" * lineLen)
        if term == "ISBN":
            print(f"{'Item ID':<13}{'Title':<45}{'Type':<17}{'Status':<13}{'ISBN':<17}")
        else:
            print(f"{'Item ID':<13}{'Title':<45}{'Type':<17}{'Status':<13}")
        # Table entries
        for row in rows:
            print("-" * lineLen)
            # ID 0, Title 3, Type 1, Status 2, ISBN 5
            if term == "ISBN":
                print(f"   {row[0]:<10}{row[3]:<45}{row[1]:<17}{row[2]:<13}{row[5]:<17}")   
            else:
                print(f"   {row[0]:<10}{row[3]:<45}{row[1]:<17}{row[2]:<13}")   
    # else no match tuple
    else:
        ret = 0
        print("=" * lineLen)
        print(f"... No items found with the given {term} ...")
    print("=" * lineLen)
    print()
    time.sleep(1)
    return ret  # 1 = at least a match, 0 = no match

def input_itemType():
    # Output a list of itemType for user
    cursor.execute("SELECT DISTINCT itemType FROM Item")
    item_types = [row[0] for row in cursor.fetchall()] 
    print("Available Item Types: ", "\t".join(item_types))
    time.sleep(0.3)

    itemType = input("➢ Enter item Type: ")
    # Cast the user input
    if itemType.lower() == "dvd":
        return "DVD"
    else:
        itemType = itemType.lower()
    
    # Check whether valid input type
    if itemType in item_types:
        return itemType
    else:
        print("Type not exist")
        return -1

def query_ID():
    itemid = input("➢ Enter the itemID: ")
    # Query
    cursor.execute("SELECT * FROM Item where itemID = ?", (itemid,))
    # Query result
    # is valid id (id exist)
    if output_Item("ID"):   
        return itemid
    # else no id match 
    else:
        return 0


# Option 1
def find_item():
    while True:
        # Find menu
        print("1. search options #:")
        print("   0. ↩ back to menu ")
        print("   a. item ID")
        print("   b. item Type")
        print("   c. Title")
        print("   d. book ISBN")
        print("   e. Type + Title")
        print("   f. all items")
        print("----------------------------------------")

        # input find option
        option = input("➢ Enter your search option #: ")
        option = option.lower()

        # 0. back to menu
        if isMenu(option):   
            main_menu()
        
        elif isQ(option):
            quit()

        # a. item ID
        elif option == "a": 
            query_ID()

        # b. item Type
        elif option == "b": 
            # User input the type
            type = input_itemType()
            # if not valid input 
            if type == -1:
                pass

            # Query
            cursor.execute("SELECT * FROM Item where itemType = ?", (type,))
            # Query result
            output_Item("Type")     

        # c. title
        elif option == "c": 
            title = input("➢ Enter the title: ")
            # Query 
            cursor.execute("SELECT * FROM Item WHERE LOWER(title) = ?", (title.lower(),))
            # Query result
            output_Item("Title")

        # d. book ISBN
        elif option == "d": 
            print("Reminder, only books have ISBN")
            isbn = input("➢ Enter the ISBN in the format of 000-0-00-000000-0: ")
            # Query 
            cursor.execute("SELECT * FROM Item NATURAL JOIN Books where ISBN = ?", (isbn,))
            # Query result
            output_Item("ISBN")

        # e. Type + Title
        elif option == "e": 
            # Type
            print("First, ")
            # User input the type
            type = input_itemType()
            # if not valid input 
            if type == -1:
                pass

            # Title
            print("Then, ")
            title = input("➢ Enter the Title: ")

            # Query 
            cursor.execute("SELECT * FROM Item WHERE itemType = ? AND LOWER(title) = ?", (type, title.lower()))
            # Query result
            output_Item("Type + Title")

        # f. all items
        elif option == "f": 
             # Query
            cursor.execute("SELECT * FROM Item")
            # Query result
            output_Item("all")

        else:
            print(" !!Invalid find option #. Please try again !!")
            time.sleep(1)


# helper function for option 2
def due_after(item_type):
    match item_type:
        case "printed_book":
            return 30
        case "online_book":
            return 21
        case _:
            return 7
        
def get_current_date():
    return datetime.now().strftime('%Y-%m-%d')

def print_who(id):
    print(f"Member ID: {id}")


# opiton 2
def borrow_item():
    while True:
        # Borrow menu
        print("2. Borrow options #:")
        print("   0. ↩ back to menu ")
        print("   a. borrow item")
        print("----------------------------------------")

        # Input borrow option
        option = input("➢ Enter your borrow option #: ")
        option = option.lower()

        # 0. back to menu
        if isMenu(option):   
            main_menu()

        elif isQ(option):
            quit()

        # a. borrow item
        elif option == "a":
            itemid = query_ID()
            # if no match id
            if not itemid:
                return 
            
            opt = input("➢ Is this the correct item? Y/N: ")
            # If is correct Item
            if confirm(opt) == "y":

                # check if Item's status == 'available'
                cursor.execute("SELECT * FROM Item WHERE itemID = ?", (itemid,))
                # Query result
                item = cursor.fetchone()
                # if 'available'
                if item and item[2] == 'available':
                    # Get the item type 
                    item_type = item[1]  

                    # online book always available
                    if item_type != "online_book":
                        # Update item status to 'borrowed'
                        cursor.execute("UPDATE Item SET itemStatus = 'borrowed' WHERE itemID = ?", (itemid,))
                        com()

                    # Get the current date
                    borrow_date = get_current_date()
                    

                    # Calculate the due date based on the item type
                    # get the amount of days this item can be borrowed
                    due_days = due_after(item_type)  
                    # dueDate = today + ^due_days
                    due_date = (datetime.now() + timedelta(days=due_days)).strftime('%Y-%m-%d')  # Calculate the due date

                    # Get the count of existing borrowIDs
                    cursor.execute("SELECT COUNT(borrowID) FROM Borrow")
                    # query count result
                    borrow_count = cursor.fetchone()[0]  
                    # Increment count to get the next borrowID
                    borrowid = int(borrow_count) + 1  

                    # Insert a new borrow entry into the Borrow table
                    global userid
                    cursor.execute("INSERT INTO Borrow (borrowID, itemID, memberID, borrowDate, dueDate) VALUES (?, ?, ?, ?, ?)", 
                                   (borrowid, itemid, userid, borrow_date, due_date))
                    com()
                    print_who(userid)
                    print(f"  ✔️  Item borrowed successfully! Due date: {due_date}")

                # otherwise, 'borrowed' or 'purchasing' can't borrow
                else:
                    print("Item is unavailable.")

            # If not correct Item
            elif confirm(opt) == "n":
                print("Not the item you are looking for?")
                print("----------------------------------------")
                time.sleep(1)
            
            # If quiting system
            elif isQ(opt):
                quit()
            
            # If other than Y/N/Q
            else:
                print(" !! Invalid input other than Y/N !!")
                print("Going back to menu...")
                time.sleep(1)
                main_menu()

        else:
            print(" !! Invalid borrow option #. Please try again !!")   
            time.sleep(1)


# helper function for option 3
def unret_list(id):
    # Fetch borrowed items for the member
    cursor.execute("""
        SELECT b.borrowID, i.itemID, i.title, i.itemType, i.itemStatus, b.borrowDate, b.dueDate
        FROM Item i NATURAL JOIN Borrow b 
        WHERE b.memberID = ? AND i.itemStatus = 'borrowed'
        GROUP BY i.itemID, b.memberID
    """, (id,))

    borrowed_items = cursor.fetchall()

    # Check if the member has borrowed any items
    if borrowed_items:
        print_who(id)
        print(f"Unreturn items:")
        lineLen = 120
        print("=" * lineLen)
        print(f"{'borrowID': <13}{'ItemID':<12}{'Title':<40}{'Type':<15}{'Status':<15}{'Borrow Date':<15}{'Due Date':<15}")
        print("-" * lineLen)
        for item in borrowed_items:
            print(f"   {item[0]:<10}  {item[1]:<10}{item[2]:<40}{item[3]:<15}{item[4]:<15}{item[5]:<15}{item[6]:<15}")
        print("=" * lineLen)
        time.sleep(1)
        # Return an array of unreturned borrowID
        return [item[0] for item in borrowed_items]
    else:
        print(f"No borrowed items found for Member ID {id}.")
        return 0    # no unreturn item


# option 3
def return_item():
    while True:
        print("3. Return Item options #:")
        print("   0. ↩ back to menu ")
        print("   a. Return a Item (one item at a time)")
        print("----------------------------------------")

        # input find option
        option = input("➢ Enter your return option #: ")
        option = option.lower()

        # 0. back to menu
        if isMenu(option):   
            main_menu()

        # If quiting system
        elif isQ(option):
            quit()

        # a. Return Item
        elif option == "a":
            global userid
            # Output a list of unreturn items
            unreturned_ids = unret_list(userid)

            # If exist unreturn item
            if unreturned_ids: 
                # User input borrowID to return
                borrowid = input("➢ Enter borrowID that you want to return: ")

                # Check if the input borrowID is in the list of unreturned IDs
                if int(borrowid) in unreturned_ids:

                    # get today's date for returnDate
                    return_date = get_current_date()
                    # update this borrow's returnDate in tbale: Borrow
                    cursor.execute("UPDATE Borrow SET returnDate = ? WHERE borrowID = ?", (return_date, borrowid))

                    # Update itemStatus in table: Item to 'available'
                    cursor.execute("UPDATE Item SET itemStatus = 'available' WHERE itemID = (SELECT itemID FROM Borrow WHERE borrowID = ?)", (borrowid,))

                    com()
                    print_who(userid)
                    print(f"  ✔️  Borrow ID {borrowid} has been successfully returned.")
                elif isMenu(borrowid):
                    main_menu()
                else:
                    print(" !! Invalid borrowID !!")
                    time.sleep(1)
            # else no unreturn item
            else:
                print("No item to return.")
                print("Going back to menu")
                time.sleep(1)
                main_menu()            

        
        # invalid option
        else:
            print(" !! Invalid return option #. Please try again !!") 
            time.sleep(1)  


# helper function for option 4
def cost_list(item_type):
    match item_type:
        case "printed_book":
            return 20
        case "online_book":
            return 15
        case "magazine":
            return 10
        case "DVD":
            return 5
        case _:
            return 0

def isBook(item_type):
    match item_type:
        case "printed_book" | "online_book":
            return 1
        case _:
            return 0


# option 4
def donate_item():
    while True:
        print("4. Donate Item options #:")
        print("   0. ↩ back to menu ")
        print("   a. Donate a Item (one item at a time)")
        print("----------------------------------------")

        # input find option
        option = input("➢ Enter your donate option #: ")
        option = option.lower()

        # 0. back to menu
        if isMenu(option):   
            main_menu()

        # If quiting system
        elif isQ(option):
            quit()
            
        # a. Donate Item
        elif option == "a":
            # smth
            print("What type of item are you donating?")
            item_type = input_itemType()
            # if not valid input 
            if item_type == -1:
                pass

            # Valid input type, and
            isbn = 0
            # is donating a book
            if isBook(item_type):
                isbn = input("➢ Enter the ISBN in the format of 000-0-00-000000-0: ")
                # Query this ISBN
                cursor.execute("SELECT * FROM Item NATURAL JOIN Books where ISBN = ?", (isbn,))
                # Query result
                row = cursor.fetchone()
                # If ISBN  exist
                if row:
                    # Print book data
                    print("The Book:")
                    print("-" * 110)
                    print(f"{'Item ID':<13}{'Title':<45}{'Type':<17}{'Status':<13}{'ISBN':<17}")
                    print(f"   {row[0]:<10}{row[3]:<45}{row[1]:<17}{row[2]:<13}{row[5]:<17}")   
                    print("-" * 110)
                    print("  ✔️  Received! Thanks for the donation.")
                    print("----------------------------------------")
                    time.sleep(1)
                    pass
            # when not book, or ISBN not exist
            # ask for book title
            title = input("➢ Enter the book title:")
            # Get the count of distinct memberID values
            cursor.execute("SELECT COUNT(DISTINCT itemID) FROM Item")
            count = cursor.fetchone()[0]  
            itemid = int(count) + 1
            cost = cost_list(item_type)

            
            # no matter a book or not
            # insert into item table
            cursor.execute("""
                INSERT INTO Item (itemID, itemType, itemStatus, title, cost) 
                VALUES (?, ?, ?, ?, ?)
            """, (itemid, item_type, 'available', title, cost))

            # if is donating a book
            if isBook(item_type):
                # insert into table: Books with itemID = itemid, ISBN = isbn
                cursor.execute("""
                    INSERT INTO Books (itemID, ISBN)
                    VALUES (?, ?)
                """, (itemid, isbn))
            com()
            print("  ✔️  Received! Thanks for the donation.")
            print("----------------------------------------")
            time.sleep(1)

        # invalid option
        else:
            print(" !! Invalid return option #. Please try again !!")   
            time.sleep(1)


# option 5
def find_event():
    while True:
        print("\nSearch options for Events:")
        print("   0. ↩ Back to menu")
        print("   a. Event ID")
        print("   b. Event Type")
        print("   c. Event Name")
        print("   d. Event Type + Event Name")
        print("   e. Date")
        print("   f. Location")
        print("   g. Show all events")
        print("----------------------------------------")

        option = input("Enter your option #: ").lower()

        if isMenu(option):
            return  # Go back to the main menu
        
        elif isQ(option):
            quit()

        elif option == "a":
            event_id = input("➢ Enter the Event ID: ")
            cursor.execute("SELECT * FROM Events WHERE eventID = ?", (event_id,))

        elif option == "b":
            print("List of Event Types:")
            cursor.execute("SELECT DISTINCT eventType FROM Events")
            types = cursor.fetchall()
            for t in types:
                print(f"   {t[0]}")
            event_type = input("➢ Enter the Event Type: ").lower()
            cursor.execute("SELECT * FROM Events WHERE LOWER(eventType) = ?", (event_type,))

        elif option == "c":
            event_name = input("➢ Enter the Event Name: ").lower()
            cursor.execute("SELECT * FROM Events WHERE LOWER(eventName) = ?", (event_name,))

        elif option == "d":
            event_type = input("➢ Enter the Event Type: ").lower()
            event_name = input("➢ Enter the Event Name: ").lower()
            cursor.execute("SELECT * FROM Events WHERE LOWER(eventType) = ? AND LOWER(eventName) = ?", (event_type, event_name))

        elif option == "e":
            date = input("Date format: YYYY-MM-DD (include '-', MM and DD are two digits: 01 instead of 1)\n➢ Enter the Date: ")
            cursor.execute("SELECT * FROM Events WHERE date = ?", (date,))

        elif option == "f":
            location = input("➢ Enter the Location: ").lower()
            cursor.execute("SELECT * FROM Events WHERE LOWER(location) = ?", (location,))
        elif option == "g":
            cursor.execute("SELECT * FROM Events")
        else:
            print("Invalid option #. Please try again.")
            time.sleep(1)
            continue

        results = cursor.fetchall()
        
        if results:
            linelen = 95
            print("\nFiltered Events Result:")
            print("=" * linelen)
            print(f"{'Event ID':<10}{'Type':<15}{'Name':<35}{'Date':<12}{'Time':<10}{'Location':<30}")
            print("-" * linelen)
            for row in results:
                print(f"{row[0]:<10}{row[2]:<15}{row[3]:<35}{row[4]:<12}{row[5]:<10}{row[6]:<30}")
            print("=" * linelen)
            
        else:
            linelen = 27
            print("=" * linelen)
            print(" ... No events found ...")
            print("=" * linelen)
        
        time.sleep(1)


# option 6
def register_event():
    
    event_id = input("➢ Enter the Event ID you want to register for: ")
    if isMenu(event_id.lower()):
        main_menu()
    elif isQ(event_id.lower()):
        quit()
        
    try:
        # Fetch event details
        cursor.execute("SELECT * FROM Events WHERE eventID = ?", (event_id,))
        event = cursor.fetchone()

        if not event:
            print("❌ Event not found. Please check the Event ID and try again.")
            time.sleep(1)
            return

        # Display event details
        print("\nEvent Details:")
        print(f"  Event Name:\t{event[3]}")
        print(f"  Event Type:\t{event[2]}")
        print(f"  Date:\t\t{event[4]}")
        print(f"  Time:\t\t{event[5]}")
        print(f"  Location:\t{event[6]}")

        # If this event already over
        # Check if the event date is in the past
        event_date = event[4]  # Assuming event[4] is the date in 'YYYY-MM-DD' format
        if event_date < get_current_date():
            print("⚠️  This event has already passed. You cannot register for it.")
            time.sleep(1)
            return

        # Confirm registration
        confirm = input("\n➢ Is this the correct event? (yes/no): ").lower()
        if confirm not in ['yes', 'y']:
            print("❌ Registration canceled.")
            time.sleep(1)
            return

        # Get member ID
        global userid
        member_id = userid

        # Check if the member is already registered for the event
        cursor.execute(
            "SELECT * FROM Event_Attendance WHERE eventID = ? AND memberID = ?",
            (event_id, member_id)
        )
        if cursor.fetchone():
            print("❌ You are already registered for this event.")
            time.sleep(1)
            return

        # Register the member for the event
        cursor.execute(
            "INSERT INTO Event_Attendance (eventID, memberID) VALUES (?, ?)",
            (event_id, member_id)
        )
        conn.commit()
        print("✅ Registration successful!")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    time.sleep(1)


# option 7
def volunteer():
    try:
        global userid
        
        # Extract member details
        cursor.execute("SELECT memberID, memberName, phone FROM Member WHERE memberID = ?", (userid,))
        member = cursor.fetchone()
        member_id, name, phone = member  

        # Check if the member is already a staff member (volunteer)
        cursor.execute("SELECT staffID FROM Staff WHERE memberID = ?", (member_id,))
        staff = cursor.fetchone()
        # If this member is a Staff
        if staff:
            staff_id = staff[0]  # Use existing staff ID
        # Else this member is only a member
        else:
            print("You are not a staff yet, adding you to Staff member")
            # Get the count of distinct memberID values
            cursor.execute("SELECT COUNT(DISTINCT staffID) FROM Staff")
            count = cursor.fetchone()[0]  
            new_staffID = count + 1

            # Add the member as a staff member with the role 'volunteer'
            cursor.execute(
                "INSERT INTO Staff (staffID, name, phone, role, memberID) VALUES (?, ?, ?, 'volunteer', ?)",
                (new_staffID, name, phone, member_id)
            )
            com()
            print(f"✅ Added as a volunteer staff member with ID: {new_staffID}")
            time.sleep(1)

        # Ask for the Event ID to volunteer for
        event_id = input("➢ Enter the Event ID you want to volunteer for: ")

        # Fetch event details
        cursor.execute("SELECT date FROM Events WHERE eventID = ?", (event_id,))
        event = cursor.fetchone()

        if not event:
            print("❌ Event not found. Please check the Event ID and try again.")
            time.sleep(1)
            return

        # Check if the event is in the future
        event_date = datetime.strptime(event[0], '%Y-%m-%d').date()
        if event_date >= datetime.now().date():
            # Check if the user is already volunteering for this event
            cursor.execute(
                "SELECT * FROM Event_Helpers WHERE eventID = ? AND staffID = ?",
                (event_id, staff_id)
            )
            if cursor.fetchone():
                print("You are already volunteering for this event.")
            else:
                # Register the user as a volunteer for the event
                cursor.execute(
                    "INSERT INTO Event_Helpers (eventID, staffID) VALUES (?, ?)",
                    (event_id, staff_id)
                )
                conn.commit()
                print("✅ Volunteer registration successful!")
        else:
            print("⚠️  Event is over. Volunteer registration denied.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except ValueError as e:
        print(f"Invalid date or time format: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    time.sleep(1)


# Option 8
def ask_librarian():
    try:
        print("\n📚 Need help? \nHere are the librarians available to assist you:")
        
        # Fetch all staff members with the role 'Librarian'
        cursor.execute("SELECT name, phone, mail FROM Staff WHERE role = 'Librarian'")
        librarians = cursor.fetchall()

        lineLen = 57
        if librarians:
            # Display librarian details in a table format
            print("=" * lineLen)
            print(f"{'Name':<15}{'Phone':<20}{'Email':<30}")
            print("-" * lineLen)
            for librarian in librarians:
                print(f"{librarian[0]:<15}{librarian[1]:<20}{librarian[2]:<30}")
            print("=" * lineLen)
            print("\nFeel free to contact them for assistance!")
        else:
            print("❌ No librarians are currently available. Please check back later.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    time.sleep(1)



def welcome(id):
    cursor.execute("SELECT * FROM Member where memberID = ?", (id,))
    entry = cursor.fetchone()
    print(f" ~ 😀 Welcome:\t Member ID: {entry[0]},\tName: {entry[1]},\tContact: {entry[3]} ~")
    time.sleep(0.7)

def switch_member():
    
    global userid
    userid = input("➢ Enter your member ID here: ")
    try:
        userid = int(userid)
    except:
        print("ERROR: ID must be a integer number")
        return 0    # switch fail
    
    # check if valid ID
    cursor.execute("SELECT memberID FROM Member")
    ids = [row[0] for row in cursor.fetchall()]

    if userid in ids:
        # Query to get the member name based on input ID
        welcome(userid)
        return 1    # switch success
    else:
        print("!! invalid id !!")
        time.sleep(1)
        return 0    # switch fail

def add_member():
    name = input("➢ Please enter your display name for your membership: ")
    number = input("➢ Please enter your contact phone number. "
        "Separate with -. (e.g. 000-000-0000): ")

    cursor.execute("SELECT * FROM Member where phone = ?", (number,))
    existing_phone = cursor.fetchall()
    if number in existing_phone: 
        print("Phone number register already.")
        print(f"\tMember ID: {existing_phone[0]},\tName: {existing_phone[1]},\tContact: {existing_phone[3]}")
        time.sleep(1)
        return 0
    else:
        # Get the count of distinct memberID values
        cursor.execute("SELECT COUNT(DISTINCT memberID) FROM Member")
        count = cursor.fetchone()[0]  

        # Generate the new ID
        global userid
        userid = int(count) + 1
        print(f"New member ID: {userid}")
        print("Adding in progress...")
        time.sleep(1)

        # Insert the new member into the Member table
        cursor.execute("INSERT INTO Member (memberID, memberName, phone) VALUES (?, ?, ?)", (userid, name, number))
        com()

        welcome(userid)
        return 1
    
def member_login():
    while True:
        print("\n----------------------------------------")
        print("Enter # to ...")
        print("      0   login with Library member ID")
        print("      1   add membership  (first visit)")    
        print("----------------------------------------")
        opt = input("➢ Enter login option # here: ")
        if opt == '0':
            if switch_member():
                return 1
        elif opt == '1':
            if add_member():
                return 1
        elif isQ(opt):
            quit()
        else:
            print("!! invalid login option !!")
            time.sleep(1)
    
def main_menu():
    while True:
        print("\n========================================")
        today = get_current_date()
        print(f"📅  Today's Date: {today}")
        print("Library System Menu:\n  #. Action")
        print("  1. Find an item in the library")
        print("  2. Borrow an item from the library")
        print("  3. Return a borrowed item")
        print("  4. Donate an item to the library")
        print("  5. Find an event in the library")
        print("  6. Register for an event")
        print("  7. Volunteer for the library")
        print("  8. Ask for help from a librarian")
        print("  9. Switch Member login")
        print("  Q. 🗙 Quit Library System")
        print("========================================")
        choice = input("➢ Enter action choice #: ")
        
        if choice == '1':
            find_item()
        elif choice == '2':
            borrow_item()
        elif choice == '3':
            return_item()
        elif choice == '4':
            donate_item()
        elif choice == '5':
            find_event()
        elif choice == '6':
            register_event()
        elif choice == '7':
            volunteer()
        elif choice == '8':
            ask_librarian()
        elif choice == '9':
            member_login()
        elif isQ(choice):
            quit()
        else:
            print("!! Invalid action choice #. Please try again. !!")
            time.sleep(1)

def main():
    print("\n🌟 Hi, Welcome to the Library System 🌟")

    member_login()

    main_menu()


if __name__ == "__main__":
    main()
