from django.db import models
from datetime import datetime, timezone

class Class(models.Model):
    name = models.CharField('Class Name', max_length=10)

    class Meta:
        verbose_name_plural = "Classes"

    def __str__(self):
        return self.name

class Section(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)

    class_number = models.IntegerField('Class Number', primary_key=True, editable=False)
    section_num = models.IntegerField('Section Number')
    class_type = models.CharField('Type', max_length=4)
    instructor = models.CharField('Instructor', max_length=40)
    days = models.CharField('Days', max_length=5)
    start_time = models.TimeField('Start Time')
    end_time = models.TimeField('End Time')
    building = models.CharField('Building', max_length=40)
    room = models.CharField('Room', max_length=6)

    def __str__(self):
        return f"{self.class_name} - {self.class_number}"

class CapSnap(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    time = models.DateTimeField('Capture Time', auto_now_add=True)

    open_seats = models.IntegerField('Open Seats') 
    reserved_seats = models.IntegerField('Reserved Seats')
    taken_seats = models.IntegerField('Taken Seats')
    waiting = models.IntegerField('Waiting')
    closed = models.BooleanField('Closed')

    class Meta:
        verbose_name = "Capacity Snapshot"

    def __str__(self):
        tm = self.time.replace(tzinfo=timezone.utc).astimezone(tz=None)
        ct = datetime.strftime(tm, "%a, %b %d %H:%M") 
        return f"{self.section.class_name} ({self.section.class_number}) - {ct}"
    
