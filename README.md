# Library-System
Group Project for CMPT 354 - Database Systems

This project implements a Library Management System using Python and SQLite, suppoting basic library interactions.


## Table of Contents
1. [Navigation Guide](#1-navigation-guide)
2. [Installation](#install)
3. [Getting Started](#start)
4. [Features](#features)
5. [Database](#database)



<a name="navigation"></a>

## 1. Navigation Guide

```bash
repository
├── addTable.ipynb      ## jupyter notebook for adding tables
├── library2.db         ## SQL database
├── main.py             ## main script
├── Report.py           ## Report
```



<a name="install"></a>

## 2. Installation

This project requires using Python and built-in Python libraries are used, so no need to manually install libraries.



<a name="start"></a>

## 3. Getting Started

Suggestion: Use PyCharm to efficiently switch between algorithms.

#### 3.1. Clone and Navigate
```bash
# 1. Clone this repo to your local machine
git clone $THISREPO
# 2. Navigate into the repository directory
cd $THISREPO
```

#### 3.2. Run project
Option A: Command line
```bash
python main.py
```

Option B: File System
Double click on the _main.py_ file.



<a name="features"></a>

## 4. Features
Shortcuts: 
- Enter 'q' will exit the library system.
- Enter 'm' will return to main menu.

#### Main Menu
Choices can be activated by entering the corresponding number:
```
1. Find item
2. Borrow item
3. Return item
4. Donate item
5. Find event
6. Register event
7. Volunteer
8. Ask librarian
9. Switch member
Q. Quit
```

#### Searching
When searching for *Item*, following search option are available:
```
a. Item ID
b. Item Type
c. Title
d. Book ISBN
e. Type + Title
f. Show all Items
```

Event
```
a. Event ID
b. Event Type
c. Event Name
d. Event Type + Event Name
e. Date
f. Location
g. Show all Events
```



<a name="database"></a>

## 5. Database
#### Existing Tables
For the existing Tables, check Report's page 1~3 for description.

### Edit Database
To modify, _addTable.ipynb_ provides the sample structure for both adding new table and modifying existing table.

