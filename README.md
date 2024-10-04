~~ Dumb Simple RAT ~~

Prior to deployment in each script there is a line like below:
rat = RAT_CLIENT('127.0.0.1', 80)
for the client this determines the server it is connecting to

rat = RAT_SERVER('0.0.0.0', 80)
for the server this determines the interfaces and ports it's listening to
change these as required

run the server script
eg. python3 server.py

run client on client/target device
eg. python3 client.py

Once the connection is made you're off to the races
See below commands and other features

This tool, once a connection is made, automatically logs all commands sent and their recieved outputs from the client
This is stored in a csv file under the current working directory on the server

taskfile example:
Is attached with this tool

Available commands:
  shell - normal shells, bash/cmd depending on client OS"
  kill or exit - is what it says, kills the script running on the client and server
  log - show the directory for the current csv log being used by the connection
  help - displays this listing
  taskfile - allows you to make a file with multiple commands to be 
      executed in a specified order seperated by newlines
