from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from pass_app.models import Quarter, Class, Section, CapSnap

from .get_info import get_info 
from . import settings
from datetime import datetime, time
from os.path import basename

def time_or_default(time_str):
    default_time = time(0, 0)
    result = None

    try:
        dt_result = datetime.strptime(time_str, "%I:%M %p")
        result = time(dt_result.hour, dt_result.minute)
    except ValueError:
        result = default_time

    return result

class Command(BaseCommand):
    help = 'Grab the classes from PASS and update the database'
    
    def add_arguments(self, parser):
        parser.add_argument(
                '--html',
                action='store',
                dest='html',
                help='Specify an HTML file to parse instead of pulling from PASS'
                )


    def handle(self, *args, **options):
        if options['html']:
            update_classes(options['html'])
        else:
            update_classes()

def update_classes(html_file = None):
    info = None
    explicit_time = None

    if html_file is not None:
        explicit_time = datetime.strptime(basename(html_file), "pass-%Y%m%d-%H%M.html")  
        with open(html_file, "r") as ihtml:
            info = get_info(ihtml)
    else:
        info = get_info()

    quarter = info["quarter"]
    classes = info["classes"]

    for cls in classes:
        update_class(cls, quarter, explicit_time)

def update_class(cls, qtr, explicit_time=None):
    class_name = None
    quarter = None
    
    try:
        quarter = Quarter.objects.get(quarter_shortname=qtr)
    except ObjectDoesNotExist:
        quarter = Quarter(quarter_shortname=qtr)
    
    quarter.save()

    try:
        class_name = Class.objects.get(name=cls["title"])
    except ObjectDoesNotExist:
        class_name = Class(name=cls["title"])

    class_name.save()

    for section in cls["sections"]:
        sect = None
        most_recent = None

        try:
            sect = Section.objects.get(class_number=section['class_number'])
        except ObjectDoesNotExist:
            sect = Section(
                    class_number=section['class_number'], 
                    quarter=quarter,
                    class_name=class_name,
                    section_num=section['section'], 
                    class_type=section['type'],
                    instructor=section['instructor'],
                    days=section['days'],
                    start_time=time_or_default(section['start_time']),
                    end_time=time_or_default(section['end_time']),
                    building=section['building'],
                    room=section['room']
                    )

        sect.save()

        try:
            # Get the most recent capture
            most_recent = sect.capsnap_set.latest('time') 
            # Just skip this section if there's no change,
            # otherwise we'll take a snapshot
            if (
                    most_recent.open_seats == section['open_seats'] and
                    most_recent.reserved_seats == section['reserved_seats'] and
                    most_recent.taken_seats == section['taken'] and
                    most_recent.waiting == section['waiting'] and
                    most_recent.closed == (section['status'] == "Closed")):
                continue
        except ObjectDoesNotExist:
            pass

        snap = CapSnap(
                section=sect,
                open_seats=section['open_seats'],
                reserved_seats=section['reserved_seats'],
                taken_seats=section['taken'],
                waiting=section['waiting'],
                closed= (section['status'] == "Closed")
                )

        if explicit_time is None:
            snap.time = explicit_time

        snap.save()
