import settings

from get_info import get_info 

def main():
    full_outp = ""

    classes = get_info(settings.classes)
    for cls in classes:
        full_outp += print_class(cls)

    return full_outp

def print_class(cls):
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

    format_str = "{:^8} | {:^4} | {:^14} | {:^30} | {:^10} | {:^16} | {:^10} | {:^8} | {:^12} | {:^6} | {:^8}\n"
    outp += format_str.format("Section", "Type", "Class Number", "Instructor", "Open Seats", "Reserved Seats", "Taken", "Waiting", "Status", "Days", "Timespan")
    outp += "-"*144 + "\n"

    sections = cls["sections"]
    for section in sections:
        inst_last = section['instructor'].split(",")[0]

        # Handle compound last names 
        inst_last = inst_last.split()
        inst_last = inst_last[0]
        
        inst_cond = show_inst or inst_last in settings.instructors
        clos_cond = show_clos or section["status"] == "Open"

        if inst_cond and clos_cond:
            found_professor = True
            outp += format_str.format(section['section'], section["type"],
                section['class_number'], section['instructor'], 
                section['open_seats'], section['reserved_seats'], 
                section['taken'], section['waiting'], 
                section['status'], section['days'], section['timespan'])

    if found_professor:
        return outp + "\n"
    else:
        return ""

if __name__ == "__main__":
    print(main())

