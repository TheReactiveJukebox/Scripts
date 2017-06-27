# Summary
This script can be used to convert csv timetable data extracted from our doodle poll into an HTML table.

# Usage
Make the script executable. Add a file called `in.csv` (or whatever you want) to the working directory that adheres to the file format below.
Then run:
```bash
$ ./tconv.py in.csv
```

# File Format
Example file:

```
Person A,OK,,,,,OK,,,,,OK,OK,OK,OK,OK,OK,OK,OK,,OK,OK,OK,OK,OK,OK
Person B,OK,OK,,,,OK,,OK,OK,OK,OK,OK,OK,OK,OK,(OK),(OK),(OK),,OK,OK,OK,OK,,
Person C,OK,OK,,,,OK,,OK,OK,,,,(OK),(OK),(OK),OK,OK,,,OK,OK,OK,OK,OK,OK
Person D,OK,OK,OK,OK,OK,OK,,OK,OK,,,,OK,OK,OK,OK,OK,(OK),OK,OK,OK,(OK),(OK),OK,OK
```