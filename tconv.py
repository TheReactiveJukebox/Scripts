#!/usr/bin/env python3
import sys
import csv

# table headings
head = """
<table>
  <thead>
    <tr>
      <td>Tag</td>
      <td colspan="5">Montag</td>
      <td colspan="5">Dienstag</td>
      <td colspan="5">Mittwoch</td>
      <td colspan="5">Donnerstag</td>
      <td colspan="5">Freitag</td>
    </tr>
    <tr>
      <td>Uhrzeit</td>
      <td>8</td><td>10</td><td>12</td><td>14</td><td>16</td>
      <td>8</td><td>10</td><td>12</td><td>14</td><td>16</td>
      <td>8</td><td>10</td><td>12</td><td>14</td><td>16</td>
      <td>8</td><td>10</td><td>12</td><td>14</td><td>16</td>
      <td>8</td><td>10</td><td>12</td><td>14</td><td>16</td>
    </tr>
  </thead>
  <tbody>
"""

# template for new person
template = """
    <tr>
      <td>{}</td>
      <td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>
      <td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>
      <td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>
      <td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>
      <td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>
    </tr>
"""

# closing tags at the end of the table
tail = """
  </tbody>
</table>
"""

# map doodle's values to our values
value_mapping = {
    "OK": " &#10004; ",
    "(OK)": "(&#10004;)",
    "": "          ",
}


def mapping(value: str) -> str:
    return value_mapping.get(value, value)

# process csv
output = head
reader = csv.reader(open(sys.argv[1], "r"))
for row in reader:
    output += template.format(*map(mapping, row))
output += tail
print(output)
