from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, Hostel, HostelMeal, OrderHistory, NoticeBoard, Attendance, Aboutus, Contactus, ContactRequest
from django.utils.text import slugify
from django.utils import timezone
from decimal import Decimal
from django.core.files.storage import FileSystemStorage
import uuid

def home(request):
    aboutus = Aboutus.objects.filter(id=1).first()
    contactus = Contactus.objects.filter(id=1).first()
    return render(request, 'index.html', {'aboutus':aboutus,'contactus':contactus})

def aboutus(request):
    return render(request, 'aboutus.html')


def signup(request):
    if request.method == 'POST':
 
        username = request.POST.get('txt')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('pswd')
        # user_type = request.POST.get('userType')

        # Create and save the user
        # Check if a user with the given email already exists
        user, created = UserProfile.objects.get_or_create(
            email=email,
            defaults={'username': username, 'password': password, 'user_type': 'student', 'phone' : phone}
        )

        if created:
            # User was created (does not already exist)
            # You can perform additional actions or redirect to a success page
            return render(request, 'login.html', {'user': user})
        else:
            # User already exists
            error_message = "User with this email already exists. Please log in."
            return render(request, 'login.html', {'error_message': error_message})


        # You might want to redirect to a success page or login page
            #  return render(request, 'login.html', {'error_message': 'Account registered successfully' })  # Replace 'success' with the actual URL name
    else:

        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        password = request.POST.get('pswd')

        try:
            user_profile = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            print("no user found")
            # User does not exist
            error_message = "Invalid login credentials. Please try again."
            return render(request, 'login.html', {'error_message': error_message})

        # Check if the entered password matches the stored password hash
 
        if password == user_profile.password:
            # Login successful
            request.session['user_email'] = user_profile.email
            request.session['user_name'] = user_profile.username            

            
            # Check user type and redirect to the appropriate dashboard
            print("User type is", user_profile.user_type)
            if user_profile.user_type == 'employee':
                all_hostels = Hostel.objects.all()
                return render(request, 'eDashboard.html',{'all_hostels': all_hostels}) 
            elif user_profile.user_type == 'student':
                all_hostels = Hostel.objects.all()
                return render(request, 'sDashboard.html',{'all_hostels': all_hostels})
            elif user_profile.user_type == 'admin':
                all_hostels = Hostel.objects.all()
                return render(request, 'hDashboard.html',{'all_hostels': all_hostels})
                
    
        else:
            # Password is incorrect
            print("incorrect no user found")

            error_message = "Invalid login credentials. Please try again."
            return render(request, 'login.html', {'error_message': error_message})

    else:
        return render(request, 'login.html')

def eDashboard(request):
    if request.method == 'GET':
        all_hostels = Hostel.objects.all()
        return render(request, 'eDashboard.html',{'all_hostels': all_hostels})
    elif request.methos == 'POST':
        all_hostels = Hostel.objects.all()
        return render(request, 'eDashboard.html',{'all_hostels': all_hostels})

def addHostel(request):
    if request.method == 'POST' and 'user_email' in request.session:
        print("Post is called here in addHostel")
        name = request.POST.get('name')
        price = request.POST.get('price')
        available_slot = request.POST.get('availableSlot')
        desc = request.POST.get('desc')

        # Create a new Hostel object and save it to the database
        hostel = Hostel(
            name=name,
            description=desc,
            price=price,  # You need to decide how to handle the price field
            available_rooms=int(available_slot) if available_slot.isdigit() else 0
        )
        hostel.save()
        image = request.FILES.get('himage')

        print("Image",image)
        # Save the image with a filename based on the hostel name
        if image: # Generate a slug from the hostel name
            fs = FileSystemStorage(location='booking/static/hostels/')
            fs.save(f"{hostel.id}.png", image)
            print("Image is getting saved ...")
           
        all_hostels = Hostel.objects.all()
        return render(request,'addHostel.html', {'all_hostels': all_hostels})
        
    elif request.method == 'GET' and 'user_email' in request.session:
        all_hostels = Hostel.objects.all()
        
        return render(request,'addHostel.html', {'all_hostels': all_hostels})
    else:
        return render(request, 'login.html')

def addHostelMeal(request):
    if request.method == 'POST' and 'user_email' in request.session:
        print("Post is called here in addHostelMeal")
        random_uuid = uuid.uuid4()
        hostel_file_value = request.POST.get('hostel_id')
        hostel_name = hostel_file_value.split('_')[1]
        hostel_id = hostel_file_value.split('_')[0]
        mimage = request.FILES.get('mimage')
        file_path=f"{hostel_file_value + str(random_uuid)}.png"
        if mimage: # Generate a slug from the hostel name
            fs = FileSystemStorage(location='booking/static/meals/')
            fs.save(f"{file_path}", mimage)
            print("Image is getting saved ...")
        
        hostel = get_object_or_404(Hostel, id=hostel_id)
        hostel_meal = HostelMeal(
            name=hostel_name,
            mealFilePath=file_path,
            hostelId= hostel
        )
        hostel_meal.save()
        all_hostel_file = HostelMeal.objects.all()
        all_hostels = Hostel.objects.all()
        return render(request,'addHostelMeal.html', {'all_hostels': all_hostels,'all_hostel_file' : all_hostel_file})
        
    elif request.method == 'GET' and 'user_email' in request.session:
        all_hostels = Hostel.objects.all()
        all_hostel_file = HostelMeal.objects.all()
        
        return render(request,'addHostelMeal.html', {'all_hostels': all_hostels,'all_hostel_file' : all_hostel_file})
    else:
        return render(request, 'login.html')

def manageNoticeBoard(request):
    if request.method == 'POST' and 'user_email' in request.session:
        print("Post is called here in addHostel")
        title = request.POST.get('title')
        notice = request.POST.get('notice')
        

        # Create a new Hostel object and save it to the database
        notice = NoticeBoard(
            title=title,
            notice=notice,
      
        )
        notice.save()

        notices = NoticeBoard.objects.all()
        return render(request,'manageNotices.html', {'notices': notices})
    elif request.method == 'GET' and 'user_email' in request.session:
        notices = NoticeBoard.objects.all()
        return render(request,'manageNotices.html', {'notices': notices})

def manegHomePage(request):
    if request.method == 'GET' and 'user_email' in request.session:
        aboutus = Aboutus.objects.filter(id=1).first()
        contactus = Contactus.objects.filter(id=1).first()
        contactforums = ContactRequest.objects.all()
        return render(request,'manageHome.html', {'aboutus': aboutus, 'contactus':contactus,'contactforums':contactforums})
    elif request.method == 'POST' and 'user_email' in request.session:
        homeType = request.POST.get('homeType')
        if homeType == 'aboutus':

            title = request.POST.get('title')
            aboutus = request.POST.get('aboutus')
            about_us = Aboutus.objects.filter(id=1).first()

            print("Home type is ", about_us.id, title, aboutus)

            # If about_us is None (i.e., no object found with id=1), create a new Aboutus object
            if not about_us:
                print("Not about us?")
                about_us = Aboutus(id=1)
            else:
                # Update the attributes with the new values
                about_us.title = title
                about_us.aboutUs = aboutus

                # Save the changes to the database
                about_us.save()


            aboutus = Aboutus.objects.filter(id=1).first()
            contactus = Contactus.objects.filter(id=1).first()
            contactforums = ContactRequest.objects.all()

            return render(request,'manageHome.html', {'aboutus': aboutus, 'contactus':contactus,'contactforums':contactforums})
    
        elif homeType == "contact":
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
          
            contactus = Contactus.objects.filter(id=1).first()

            # If about_us is None (i.e., no object found with id=1), create a new Aboutus object
            if not contactus:
                contactus = Contactus(id=1)

            # Update the attributes with the new values
            contactus.email = email
            contactus.address = address
            contactus.phone = phone

            # Save the changes to the database
            contactus.save()
            aboutus = Aboutus.objects.filter(id=1).first()
            contactus = Contactus.objects.filter(id=1).first()
            contactforums = ContactRequest.objects.all()

            return render(request,'manageHome.html', {'aboutus': aboutus, 'contactus':contactus,'contactforums':contactforums})
    
def manageEmployee(request):
    if request.method == 'GET':
        all_employee = UserProfile.objects.filter(user_type='employee')
        return render(request, 'manageEmployee.html', {'all_employee': all_employee})
    elif request.method == "POST" and 'user_email' in request.session:
        print("In post emp")
        username = request.POST.get('ename')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        user, created = UserProfile.objects.get_or_create(
            email=email,
            defaults={'username': username, 'password': password, 'user_type': 'employee','phone':phone}
        )

        if created:
            # User was created (does not already exist)
            # You can perform additional actions or redirect to a success page
            all_employee = UserProfile.objects.filter(user_type='employee')
            return render(request, 'manageEmployee.html', {'all_employee': all_employee})
        
def manageStudent(request):
    if request.method == 'GET':
        all_student = UserProfile.objects.filter(user_type='student')
        return render(request, 'manageStudent.html', {'all_student': all_student})
    elif request.method == "POST" and 'user_email' in request.session:
        print("In post Stud")
        username = request.POST.get('sname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        user, created = UserProfile.objects.get_or_create(
            email=email,
            defaults={'username': username, 'password': password, 'user_type': 'student','phone':phone}
        )

        # if created:
            # User was created (does not already exist)
            # You can perform additional actions or redirect to a success page
        all_student = UserProfile.objects.filter(user_type='student')
        return render(request, 'manageStudent.html', {'all_student': all_student})
       
       
def logout(request):
    request.session.clear()
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    # Redirect to the login page or any other desired page
    return response
    

def deleteNotice(request , id):
    if 'user_email' in request.session:
        notice = get_object_or_404(NoticeBoard, id=id)
        # Your logic for deleting a hostel goes here
        notice.delete()
        notices = NoticeBoard.objects.all()
        return render(request,'manageNotices.html', {'notices': notices})

def deleteHostel(request, id):
    if 'user_email' in request.session:
        hostel = get_object_or_404(Hostel, id=id)
        # Your logic for deleting a hostel goes here
        hostel.delete()
        all_hostels = Hostel.objects.all()
        return render(request,'addHostel.html', {'all_hostels': all_hostels})
    
def hostelBookDetails(request):
    if 'user_email' in request.session:
        all_orders = OrderHistory.objects.all()
        return render(request,'hostelBookDetails.html', {'all_orders': all_orders})
    
def approveHostel(request, id):
    if 'user_email' in request.session:
        hostel_order = get_object_or_404(OrderHistory, id=id)

        if hostel_order:
            hostel_order.status = "Approve"
            hostel_id = hostel_order.hostel.id
            hostel_details = Hostel.objects.filter(id=hostel_id).first()
            hostel_details.available_rooms = hostel_details.available_rooms - 1
            hostel_order.save()
            hostel_details.save()
        all_orders = OrderHistory.objects.all()
        return render(request,'hostelBookDetails.html', {'all_orders': all_orders})

def deleteHostelMeal(request, id):
    if 'user_email' in request.session:
        hostelMeal = get_object_or_404(HostelMeal, id=id)
        # Your logic for deleting a hostel goes here
        hostelMeal.delete()
        all_hostels = Hostel.objects.all()
        all_hostel_file = HostelMeal.objects.all()
        return render(request,'addHostelMeal.html', {'all_hostels': all_hostels,'all_hostel_file' : all_hostel_file})

def deleteEmployee(request , id):
    if 'user_email' in request.session:
        employee = get_object_or_404(UserProfile, id=id)
        # Your logic for deleting a hostel goes here
        employee.delete()
        user_type = employee.user_type
        if user_type == "employee":
            all_employee = UserProfile.objects.filter(user_type='employee')
            return render(request, 'manageEmployee.html', {'all_employee': all_employee})
        else:
            all_student = UserProfile.objects.filter(user_type='student')
            return render(request, 'manageStudent.html', {'all_student': all_student})            

def editEmployee(request, id):
    if request.method == 'GET' and 'user_email' in request.session:
        user = UserProfile.objects.filter(id=id)
        print("sa.dnfflsFLZlkdnASLK",user)
        user_type_ = user[0].user_type
        print("sa.dnfflsFLZlkdnASLK",user_type_)
        if user_type_ == "employee": 
            return render(request, 'editEmployee.html',{'user':user})
        else:
            return render(request, 'editStudent.html',{'user':user})

    
    elif request.method == 'POST' and 'user_email' in request.session:
        # user = UserProfile.objects.filter(email=request.session['user_email'])
        # print(len(user))
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        print("User", email,password, username, phone)

        # Retrieve the user profile based on the email
        user = UserProfile.objects.filter(id=id).first()
        user_type = user.user_type
        if user:
            # Update the user profile attributes with the new values
            user.username = username
            user.phone = phone
            if password:
                user.password = password  # Note: This does not hash the password

            # Save the updated user profile
            user.save()
        if user_type == "employee": 
            all_employee = UserProfile.objects.filter(user_type='employee')
            return render(request, 'manageEmployee.html', {'all_employee': all_employee})
        else:
            all_student = UserProfile.objects.filter(user_type='student')
            return render(request, 'manageStudent.html', {'all_student': all_student})

def editHostel(request, id):
    if request.method == 'GET' and 'user_email' in request.session:
        hostel = Hostel.objects.filter(id=id)
        return render(request, 'editHostel.html',{'hostel':hostel})
    
    elif request.method == 'POST' and 'user_email' in request.session:
        name = request.POST.get('name')
        price = request.POST.get('price')
        available_slot = request.POST.get('availableSlot')
        desc = request.POST.get('desc')
        hostel = Hostel.objects.filter(id=id).first()

        if hostel:
            hostel.name = name
            hostel.price = price
            hostel.available_rooms = available_slot
            hostel.description = desc
            hostel.save()
 
        image = request.FILES.get('himage')
    
        print("Image",image)
        # Save the image with a filename based on the hostel name
        if image: # Generate a slug from the hostel name
            fs = FileSystemStorage(location='booking/static/hostels/')
            fs.save(f"{hostel.id}.png", image)
            print("Image is getting saved ...")
           
        all_hostels = Hostel.objects.all()
        return render(request,'addHostel.html', {'all_hostels': all_hostels})

def takeAttendance(request):
    if 'user_email' in request.session and request.method == "GET":
        all_orders = OrderHistory.objects.all()

        return render(request,'takeAttendance.html', {'all_orders': all_orders})
    elif 'user_email' in request.session and request.method == "POST":
        hostelId = request.POST.get('hostelId')
        orderId = request.POST.get('orderId')
        isPresent =  request.POST.get('isPresent')

        if isPresent == 'True':
            isPresent = True
        else:
            isPresent = False
      

        order_history = get_object_or_404(OrderHistory, id=orderId)
        user_profile = get_object_or_404(UserProfile, id=order_history.booked_by.id)

        # Check if attendance has already been taken for today
        # today = timezone.now().date()
        # attendance_exists = Attendance.objects.filter(orderId=order_history, user=user_profile, lastUpdated__date=today).exists()

        # if not attendance_exists:
            # Attendance not taken for today, mark as absent or present (you can modify this logic as needed)
        is_present = request.POST.get('is_present') == 'present'
        Attendance.objects.create(orderId=order_history, user=user_profile, isPresent=is_present)

        # all_orders = OrderHistory.objects.all()
        all_attendance = Attendance.objects.all()
        all_hostels = Hostel.objects.filter(id=hostelId)
        users = OrderHistory.objects.filter(hostel=hostelId)
        print("reacher here!....",hostelId, )
        return render(request,'takeAttendance.html', {'all_attendance': all_attendance,'all_hostels':all_hostels,'users': users,'hostelId':hostelId})

def takeAttendanceE(request):
    if 'user_email' in request.session and request.method == "GET":
        all_orders = OrderHistory.objects.all()

        return render(request,'takeAttendance.html', {'all_orders': all_orders})
    elif 'user_email' in request.session and request.method == "POST":
        hostelId = request.POST.get('hostelId')
        orderId = request.POST.get('orderId')
        isPresent =  request.POST.get('isPresent')

        if isPresent == 'True':
            isPresent = True
        else:
            isPresent = False
      

        order_history = get_object_or_404(OrderHistory, id=orderId)
        user_profile = get_object_or_404(UserProfile, id=order_history.booked_by.id)
        hostel = get_object_or_404(Hostel, id= hostelId)
        # Check if attendance has already been taken for today
            # today = timezone.now().date()
            # attendance_exists = Attendance.objects.filter(orderId=order_history, user=user_profile, lastUpdated__date=today).exists()
            # print(attendance_exists)
            # if not attendance_exists:
            #     print("Attendace will be taken")
            # Attendance not taken for today, mark as absent or present (you can modify this logic as needed)
            # is_present = request.POST.get('is_present') == 'present'
        Attendance.objects.create(orderId=order_history, hostel = hostel, user=user_profile, isPresent=isPresent)

        # all_orders = OrderHistory.objects.all()
        all_attendance = Attendance.objects.filter(hostel = hostel )
        all_hostels = Hostel.objects.filter(id=hostelId)
        users = OrderHistory.objects.filter(hostel=hostelId)
        print("reacher here!....",users, )
        return render(request,'takeAttendance1.html', {'all_attendance': all_attendance,'all_hostels':all_hostels,'users': users,'hostelId':hostelId})


def takeAttendance1(request):
    if 'user_email' in request.session and request.method == "POST":
        id = request.POST.get('id')
        print("hostel id",id)
        users = OrderHistory.objects.filter(hostel=id)
        all_attendance = Attendance.objects.filter(hostel = id )
        return render(request,'takeAttendance1.html', {'all_attendance': all_attendance,'users': users,'hostelId':id})

def hDashboard(request):
    if 'user_email' in request.session and request.method == "GET":
        all_hostels = Hostel.objects.all()
        return render(request,'hDashboard.html',{'all_hostels': all_hostels})
        


#studentds

def sDashboard(request):
    if request.method == 'GET' and 'user_email' in request.session:
        all_hostels = Hostel.objects.all()
        
        return render(request, 'sDashboard.html',  {'all_hostels': all_hostels})
    else:
        return render(request, 'login.html')

def showMeal(request):
    if request.method == 'GET' and 'user_email' in request.session:
        all_hostels = Hostel.objects.all()
        
        return render(request, 'showMeal.html',  {'all_hostels': all_hostels})
    else:
        return render(request, 'login.html')
    
def userQueryDetails(request):
    if request.method == 'GET' and 'user_email' in request.session:
        user_email = request.session['user_email']
        contactforums = ContactRequest.objects.filter(email=user_email)
        return render(request, 'manageStudentQuery.html', {'contactforums': contactforums})
    else:
        return render(request, 'login.html')


def hostelDesc(request,id):
    if request.method == 'GET' and 'user_email' in request.session:
        hostel = get_object_or_404(Hostel, id=id)
        hostel.new_price = hostel.price + (hostel.price *  Decimal('0.10'))
        return render(request,'hostelDesc.html',{'hostel':hostel})
    
def hostelMealPage(request, id):
    if request.method == 'GET' and 'user_email' in request.session:
        try:
            hostel = HostelMeal.objects.get(hostelId=id)
            return render(request, 'hostelMealPage.html', {'hostel': hostel})
        except HostelMeal.DoesNotExist:
            warning_message = "No meal present for this hostel."
            print(warning_message)
            return render(request, 'hostelMealPage.html', {'warning_message': warning_message})
        

def sCheckout(request, id):
    if request.method == 'GET' and 'user_email' in request.session:
        hostel = get_object_or_404(Hostel, id=id)
        return render(request, 'sCheckout.html', {'hostel': hostel})
    elif request.method == 'POST' and 'user_email' in request.session:
        hostel = get_object_or_404(Hostel, id=id)
        user = get_object_or_404(UserProfile,email= request.session['user_email'] )

        
        # Check if an order history already exists for the user and hostel
        existing_order = OrderHistory.objects.filter(booked_by=user).exists()
        room_left = hostel.available_rooms
        if not existing_order and room_left > 0:
            # Create a new OrderHistory entry if it doesn't exist
            order = OrderHistory(
                hostel=hostel,
                hostelName=hostel.name,
                booked_by=user,
                paid_amount=hostel.price,  # You need to decide how to handle the price field
            )
            order.save()
            all_hostels = Hostel.objects.all()
        
            return render(request, 'sDashboard.html',  {'all_hostels': all_hostels})
        else:
            # Handle the case where an order history already exists
            # You can return a response, raise an exception, or perform any other action as needed
            # For example, you can show a message to the user indicating that the order already exists
            print("Order history already exists for this user and hostel.")
            all_hostels = Hostel.objects.all()
            warning_message = f"You've already booked Hostel"
            print("--------",room_left)
            if room_left < 1:
                warning_message = f"Sorry Hostel is Full."
            return render(request, 'sDashboard.html',  {'all_hostels': all_hostels,'warning_message':warning_message})
       
def sHistory(request):
    if request.method == 'GET' and 'user_email' in request.session:
        user = get_object_or_404(UserProfile,email= request.session['user_email'] )
        all_orders = OrderHistory.objects.filter(booked_by=user)
        for i in all_orders:
            i.date_booked = i.date_booked.strftime('%d/%m/%y')
            print("Date booked,",i.date_booked)
        return render(request, 'sHistory.html', {'all_orders': all_orders})

def sNoticeBoard(request):
    if request.method == 'GET' and 'user_email' in request.session:
        notices = NoticeBoard.objects.all()
        return render(request, 'noticeBoard.html',{'notices':notices})
    
def editNoticeBoard(request, id):
    if request.method == 'GET' and 'user_email' in request.session:
        nb = NoticeBoard.objects.filter(id=id)
        return render(request, 'editNoticeBoard.html',{'notice':nb})
    elif request.method == 'POST' and 'user_email' in request.session:
        title = request.POST.get('title')
        notice = request.POST.get('notice')  
        nb = NoticeBoard.objects.filter(id=id).first()
        if nb:
            nb.title = title
            nb.notice = notice
            nb.save()

        notices = NoticeBoard.objects.all()
        return render(request,'manageNotices.html', {'notices': notices})
    
def sEditProfile(request):
    if request.method == 'GET' and 'user_email' in request.session:
        user = UserProfile.objects.filter(email=request.session['user_email'])
        print(len(user))
        return render(request, 'editProfile.html',{'user':user})
    
    elif request.method == 'POST' and 'user_email' in request.session:
        # user = UserProfile.objects.filter(email=request.session['user_email'])
        # print(len(user))
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        print("User", email,password, username, phone)

        # Retrieve the user profile based on the email
        user = UserProfile.objects.filter(email=request.session['user_email']).first()

        if user:
            # Update the user profile attributes with the new values
            user.username = username
            user.phone = phone
            if password:
                user.password = password  # Note: This does not hash the password

            # Save the updated user profile
            user.save()
        user = UserProfile.objects.filter(email=request.session['user_email'])
        
        return render(request, 'editProfile.html',{'user':user})


def contactUsForm(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        email = request.POST.get('email')
        name = request.POST.get('name')
        subject = request.POST.get('subject')

        ContactRequest.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
        return render(request, 'index.html',{'message':'Your message has been submitted'})

def replyMessage(request):
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        reply_text = request.POST.get('reply')
        
        message = ContactRequest.objects.get(id=message_id)
        
        message.admin_message = reply_text
        message.save()
        
    contactforums = ContactRequest.objects.all()
    return  render(request, 'manageHome.html',{'contactforums':contactforums})
