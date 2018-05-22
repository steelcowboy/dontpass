# from settings import *
import settings

from get_info import get_info 

max_room_len = 0

def main():
    full_outp = ""

    # classes = get_info()
    classes = None

    with open("/home/steelcowboy/pass_html/pass-2018521-1545.html", "r") as ihtml:
        classes = get_info(ihtml)

    quarter = classes["quarter"]
    classes = classes["classes"]

    full_outp += f"\033[31m{quarter}\033[0m\n\n"
    for cls in classes:
        full_outp += print_class(cls)

    print(max_room_len)
    return full_outp

def print_class(cls):
    global max_room_len
    found_professor = False
    
    show_inst = settings.show_all_inst
    show_clos = settings.show_closed

    START = ""
    END = ""
    if settings.color:
        START = "\33[1;32m]"
        END = "\33[0m"

    outp = ""

    outp += START + ("=" * 20) + "  " + cls["title"] + "  " + ("=" * 20) + END + "\n"

    format_str = "{:^8} | {:^4} | {:^14} | {:^30} | {:^10} | {:^16} | {:^10} | {:^8} | {:^12} | {:^6} | {:^8} | {:^12} | {:^4}\n"
    outp += format_str.format("Section", "Type", "Class Number", "Instructor", "Open Seats", "Reserved Seats", "Taken", "Waiting", "Status", "Days", "Timespan", "Building", "Room")
    outp += "-"*144 + "\n"

    sections = cls["sections"]
    for section in sections:
        max_room_len = max(max_room_len, len(section['room']))

        inst_last = section['instructor'].split(",")[0]

        # Handle compound last names 
        inst_last = inst_last.split()
        inst_last = inst_last[0]
        
        # Also from settings  
        inst_cond = show_inst or inst_last in settings.instructors
        clos_cond = show_clos or section["status"] == "Open"

        if inst_cond and clos_cond:
            found_professor = True
            outp += format_str.format(section['section'], section["type"],
                section['class_number'], section['instructor'], 
                section['open_seats'], section['reserved_seats'], 
                section['taken'], section['waiting'], 
                section['status'], section['days'], f"{section['start_time']} - {section['end_time']}",
                section['building'], section['room'])

    if found_professor:
        return outp + "\n"
    else:
        return ""

if __name__ == "__main__":
    main()

