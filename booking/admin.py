from django.contrib import admin
from .models import Hostel,HostelMeal, OrderHistory, Aboutus, Contactus, UserProfile, Attendance, NoticeBoard, ContactRequest
# Register your models here.



admin.site.register(UserProfile)
admin.site.register(Hostel)
admin.site.register(HostelMeal)
admin.site.register(OrderHistory)
admin.site.register(Attendance)
admin.site.register(NoticeBoard)
admin.site.register(Aboutus)
admin.site.register(Contactus)
admin.site.register(ContactRequest)
