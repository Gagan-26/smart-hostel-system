from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.IntegerField()
    password = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20, choices=[('admin', 'Admin'),('employee', 'Employee'),('student', 'Student'), ('hostelOwner', 'Hostel Owner')])
    

class Hostel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_rooms = models.PositiveIntegerField()

class HostelMeal(models.Model):
    name = models.CharField(max_length=100)
    mealFilePath = models.CharField(max_length=200)
    hostelId = models.ForeignKey(Hostel, on_delete=models.CASCADE)

class OrderHistory(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    hostelName = models.CharField(max_length=100, default='NA')
    booked_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_booked = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')


class Attendance(models.Model):
    orderId = models.ForeignKey(OrderHistory, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    isPresent = models.BooleanField(default=False)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class NoticeBoard(models.Model):
    title = models.CharField(max_length=100)
    notice = models.TextField()
    lastUpdated = models.DateTimeField(auto_now_add=True)

class Aboutus(models.Model):
    title = models.TextField()
    aboutUs = models.TextField()
    lastUpdated = models.DateTimeField(auto_now_add=True)

class Contactus(models.Model):
    email = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.TextField()


class ContactRequest(models.Model):
    email = models.CharField(max_length=100)
    subject = models.TextField()
    name = models.TextField()
    message = models.TextField()
    admin_message = models.TextField(default='NA')

    


