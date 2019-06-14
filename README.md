# Simple-Chat-Room
Python based application that uses low level socket api calls to perform networking and provide communication between Clients on Unix based Systems
This use select and socket module of python for achieving communication.
Socket module is used for creation of tcp sockets,listening for client sockets,accepting client sockets,connecting to server sockets and destroying sockets at end of communication.
Select module is used for management of sockets and command line inputs.


***NOTE***
This application works only in unix based system because the select module donot support I/O in windows.

***FURTHER ENHANCEMENT***
Future goal on this project is to use threading so it can work on windows.
Addition of GUI.

***RESOURCES***
https://developer.ibm.com/tutorials/l-pysocks/
https://stackoverflow.com/
