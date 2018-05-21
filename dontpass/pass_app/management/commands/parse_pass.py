import re
import bs4
from bs4 import BeautifulSoup, SoupStrainer
from enum import IntEnum

class gridCols(IntEnum):
    SECTION = 0
    TYPE = 1
    CLSNUM = 2
    INST = 3
    OPEN_S = 4
    RES_S = 5
    SEAT_T = 6
    WAITING = 7
    STATUS = 8
    DAYS = 9
    START = 10
    END = 11
    BUILDING = 12
    ROOM = 13

def get_class_or_empty_list(obj):
    val = obj.get("class")
    return val if val else []

def parse_pass(html):
    numsections = 0

    strainer = SoupStrainer("div", class_="select-course")

    soup = BeautifulSoup(html, 'html.parser', parse_only=strainer)
    for class_block in soup.children:
        sections = []

        class_name = class_block.h3.text
        name = class_name.split("-")[0]
        name = name.rstrip().lstrip()
        clsname = re.sub(' +',' ', name)

        for row in class_block("tr"):
            if "key-cancel" in get_class_or_empty_list(row): 
                continue

            # First need to see if this is a notes row or a data row
            start_elem = row.find("td", class_="sectionNumber")
            if start_elem == None:
                continue

            cols = list(row("td"))
            i = cols.index(start_elem)

            # For some reason a section has a * in it, remove anything that's not a number
            section_num = int(re.sub("[^0-9]", "", cols[i].text))
            status = cols[i+gridCols.STATUS].text.lstrip().rstrip()
            
            sections.append({
                "section": section_num, 
                "type": cols[i+gridCols.TYPE].text,
                "class_number": int(cols[i+gridCols.CLSNUM].text),
                "instructor": cols[i+gridCols.INST].text,
                "open_seats": int(cols[i+gridCols.OPEN_S].text),
                "reserved_seats": int(cols[i+gridCols.RES_S].text),
                "taken": int(cols[i+gridCols.SEAT_T].text),
                "waiting": int(cols[i+gridCols.WAITING].text),
                "status": status,
                "days": cols[i+gridCols.DAYS].text,
                "start_time": cols[i+gridCols.START].text,
                "end_time": cols[i+gridCols.END].text,
                "building": cols[i+gridCols.BUILDING].text,
                "room": cols[i+gridCols.ROOM].span.text,
                })
            numsections += 1

        # Add a 0.01 to fix division by 0 error, if the denominator is 0 the numerator is certainly 0 as well
        sections = sorted(sections, key=lambda k: (k["taken"]+k["waiting"])/(k["open_seats"]+k["reserved_seats"]+k["waiting"]+k["taken"]+0.01))
        result = {"title": clsname, "sections": sections}
    
    print(numsections)


if __name__ == "__main__":
    with open("pass.html", "r") as htmlfile:
        parse_pass(htmlfile.read())

