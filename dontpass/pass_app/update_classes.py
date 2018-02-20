# from settings import *
from django.core.exceptions import ObjectDoesNotExist

import settings

from get_info import get_info 
from models import Class, Section, CapSnap
from datetime import datetime, time

def update_classes():
    classes = get_info(settings.classes)
    for cls in classes:
        update_class(cls)

def update_class(cls):
    class_name = None

    try:
        class_name = Class.objects.get(name=cls["title"])
    except ObjectDoesNotExist:
        class_name = Class(name=cls["title"])

    class_name.save()

    for section in sections:
        sect = None
        most_recent = None

        try:
            sect = Section.objects.get(class_number=section['class_number'])
        except ObjectDoesNotExist:
            st = datetime.strptime(section['start_time'], "%I:%M %p")
            en = datetime.strptime(section['end_time'], "%I:%M %p")

            start = time(st.hour, st.minute)
            end = time(en.hour, en.minute)

            sect = Section(
                    class_number=section['class_number'], 
                    class_name=class_name,
                    section_num=section['section'], 
                    class_type=section['type'],
                    instructor=section['instructor'],
                    days=section['days'],
                    start_time=start,
                    end_time=end,
                    building=section['building'],
                    room=section['room']
                    )

        sect.save()

        try:
            most_recent = sect.capsnap_set.latest() 
            # Just return if there's no change, otherwise we'll take a snapshot
            if (
                    most_recent.open_seats == section['open_seats'] and
                    most_recent.reserved_seats == section['reserved_seats'] and
                    most_recent.taken_seats == section['taken_seats'] and
                    most_recent.waiting == section['waiting'] and
                    most_recent.closed == section['closed']):
                return
        except ObjectDoesNotExist:
            pass

        snap = CapSnap(
                section=sect,
                open_seats=section['open_seats'],
                reserved_seats=section['reserved_seats'],
                taken_seats=section['taken_seats'],
                waiting=section['waiting'],
                closed= (section['status'] == "Closed")
                )

        snap.save()


if __name__ == "__main__":
    update_classes()

