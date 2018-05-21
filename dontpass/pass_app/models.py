from django.db import models
from datetime import datetime, timezone

class Quarter(models.Model):
    quarter_shortname = models.CharField("Quarter Shortname", max_length=3)

    se_first = models.DateField("Special Exception 1st Round", blank=True, null=True)
    se_second = models.DateField("Special Exception 2nd Round", blank=True, null=True)

    cgs_first = models.DateField("Continuing Graduate Students 1st Round", blank=True, null=True)
    cgs_second = models.DateField("Continuing Graduate Students 2nd Round", blank=True, null=True)

    apl4_first = models.DateField("Academic Progress Level IV 1st Round", blank=True, null=True)
    apl4_second = models.DateField("Academic Progress Level IV 2nd Round", blank=True, null=True)

    apl3_first = models.DateField("Academic Progress Level III 1st Round", blank=True, null=True)
    apl3_second = models.DateField("Academic Progress Level III 2nd Round", blank=True, null=True)

    apl2_first = models.DateField("Academic Progress Level II 1st Round", blank=True, null=True)
    apl2_second = models.DateField("Academic Progress Level II 2nd Round", blank=True, null=True)

    apl1_first = models.DateField("Academic Progress Level I 1st Round", blank=True, null=True)
    apl1_second = models.DateField("Academic Progress Level I 2nd Round", blank=True, null=True)

    pnc_first = models.DateField("PolyPlanner Non-Compliant 1st Round", blank=True, null=True)
    pnc_second = models.DateField("PolyPlanner Non-Compliant 2nd Round", blank=True, null=True)

    def __str__(self):
        return quarter_shortname

class Class(models.Model):
    name = models.CharField('Class Name', max_length=10)

    class Meta:
        verbose_name_plural = "Classes"

    def __str__(self):
        return self.name

class Section(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE, default=1, null=True)

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
        get_latest_by = "time"

    def __str__(self):
        tm = self.time.replace(tzinfo=timezone.utc).astimezone(tz=None)
        ct = datetime.strftime(tm, "%a, %b %d %H:%M") 
        return f"{self.section.class_name} ({self.section.class_number}) - {ct}"
    
