
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),

    # Auth
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('aboutus/', aboutus, name='aboutus'),

    # path('logout/', logout, name='logout'),


    # Admin access
    path('addHostel/', addHostel, name='addHostel'),
    path('addHostelMeal/', addHostelMeal, name='addHostelMeal'),
    path('editHostel/<int:id>/', editHostel, name='editHostel'),
    path('deleteHostel/<int:id>/', deleteHostel, name='deleteHostel'),
    path('approveHostel/<int:id>/', approveHostel, name='approveHostel'),
    path('hostelBookDetails/', hostelBookDetails, name='hostelBookDetails'),
    path('takeAttendance/', takeAttendance, name='takeAttendance'),
    path('takeAttendance1/', takeAttendance1, name='takeAttendance1'),
    path('takeAttendanceE/', takeAttendanceE, name='takeAttendanceE'),
    path('manegHomePage/', manegHomePage, name='manegHomePage'),
    
    


    path('hDashboard/', hDashboard, name='hDashboard'),
    path('manageEmployee/', manageEmployee, name='manageEmployee'),
    path('manageStudent/', manageStudent, name='manageStudent'),
    path('manageNoticeBoard/', manageNoticeBoard, name='manageNoticeBoard'),
    path('deleteNotice/<int:id>/', deleteNotice, name='deleteNotice'),
    
    # Student access
    path('sDashboard/', sDashboard, name='sDashboard'),
    path('showMeal/', showMeal, name='showMeal'),
    path('userQueryDetails/', userQueryDetails, name='userQueryDetails'),
    path('hostelDesc/<int:id>/', hostelDesc, name='hostelDesc'),
    path('hostelMealPage/<int:id>/', hostelMealPage, name='hostelMealPage'),
    path('deleteHostelMeal/<int:id>/', deleteHostelMeal, name='deleteHostelMeal'),
    path('sCheckout/<int:id>/', sCheckout, name='sCheckout'),
    path('sHistory/', sHistory, name='sHistory'),
    path('sNoticeBoard/', sNoticeBoard, name='sNoticeBoard'),
    path('editNoticeBoard/<int:id>/', editNoticeBoard, name='editNoticeBoard'),
    path('sEditProfile/', sEditProfile, name='sEditProfile'),
    path('replyMessage/', replyMessage, name='replyMessage'),

    


    #employee access
    path('eDashboard/', eDashboard, name='eDashboard'),
    path('deleteEmployee/<int:id>/', deleteEmployee, name='deleteEmployee'),
    path('editEmployee/<int:id>/', editEmployee, name='editEmployee'),

    #public access 
    path('contactUsForm', contactUsForm, name='contactUsForm' )
    


     
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)