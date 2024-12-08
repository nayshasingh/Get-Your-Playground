from datetime import datetime, timedelta
from django.shortcuts import render
from datetime import date
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
import math
from datetime import date, datetime, timedelta
from django.shortcuts import redirect, get_object_or_404
from datetime import datetime
from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.models import User
from pytz import timezone
import time
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from datetime import datetime, timedelta
from datetime import date
from .models import TurfBooked

def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, 'mainpage_index.html', {'username': username})
    return render(request, 'mainpage_index.html')


def book_now(request):
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, 'booking_index.html', {'username': username})
    return render(request, 'booking_index.html')


def turf_details(request):
    currentDate = date.today().strftime("%Y-%m-%d")
    endDate = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
    return render(request, 'turfblog.html', {'currentDate': currentDate, 'endDate': endDate})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('book_now')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'signIn.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['emailid']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email is already Taken')
            return redirect('signup')
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.save()
            return redirect('login')
    else:
        return render(request, 'signUp.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def contactus(request):
    return render(request, 'contactUs.html')


def aboutus(request):
    return render(request, 'aboutus.html')




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import TurfBooked  # Assuming TurfBooked model is imported correctly


@login_required(login_url='login')
@login_required(login_url='login')
def slot_details(request):
    if request.method == 'POST':
        selectedDate = request.POST.get('selectedDate')
        if not selectedDate:
            return render(request, 'turfBooking.html', {
                'currentDate': datetime.now().strftime("%Y-%m-%d"),
                'selectedDate': selectedDate,
                'list': [],
                'available_slots': []
            })

        # Determine the chosen day and other details
        choosenDay = datetime.strptime(selectedDate, "%Y-%m-%d").strftime("%A")
        currentDate = datetime.now().strftime("%Y-%m-%d")
        
        day_index = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6
        }.get(choosenDay)

        if day_index is not None:
            # Query the `TurfBooked` table for bookings on the selected date
            bookings = TurfBooked.objects.filter(selected_date=selectedDate)
            slots = [0] * 19  # 0 indicates available, 1 indicates booked

            # Define a mapping of time slot strings to indices
            time_slot_mapping = {
                "6-7 am": 0, "7-8 am": 1, "8-9 am": 2, "9-10 am": 3, "10-11 am": 4,
                "11-12 am": 5, "12-1 pm": 6, "1-2 pm": 7, "2-3 pm": 8, "3-4 pm": 9,
                "4-5 pm": 10, "5-6 pm": 11, "6-7 pm": 12, "7-8 pm": 13, "8-9 pm": 14,
                "9-10 pm": 15, "10-11 pm": 16, "11-12 pm": 17, "12-1 am": 18
            }

            # Determine the current time for comparison
            current_time = datetime.now()
            selected_date_time = datetime.strptime(selectedDate, "%Y-%m-%d")

            booked_slots = set()  # Store booked slots as a set for quick lookup

            for booking in bookings:
                # Ensure `booking.slots` is iterable and contains slot strings
                for slot_time in booking.slots:
                    if slot_time in time_slot_mapping:
                        slot_index = time_slot_mapping[slot_time]  # Get the index
                        booked_slots.add(slot_index)  # Add to booked slots set

            # Prepare a list of available slots that have not passed and are not booked
            available_slots = []
            for i in range(0, 19):  # Iterate over the slot indices
                hour = i // 2
                minute = (i % 2) * 30
                try:
                    slot_time = selected_date_time.replace(hour=hour, minute=minute)
                    if slot_time > current_time and i not in booked_slots:  # Check if the slot is available and not past
                        available_slots.append(i)
                except ValueError:
                    # Handle the case where hour is out of the valid range (0-23)
                    continue

            return render(request, 'turfBooking.html', {
                'currentDate': currentDate,
                'selectedDate': selectedDate,
                'list': slots,
                'available_slots': available_slots
            })
        else:
            return render(request, 'turfBooking.html', {
                'currentDate': datetime.now().strftime("%Y-%m-%d"),
                'selectedDate': selectedDate,
                'list': [],
                'available_slots': []
            })

    return render(request, 'turfBooking.html', {
        'currentDate': datetime.now().strftime("%Y-%m-%d"),
        'selectedDate': None,
        'list': [],
        'available_slots': []
    })




def turfDateSelection(request):

    if request.method == 'POST':
        selectedDate = request.POST['selectedDate']
        request.session['choosenDate'] = selectedDate
        return redirect('turf_bookings')
    else:
        currentDate = date.today().strftime("%Y-%m-%d")
        # print(currentDate)
        endDate = (date.today() + timedelta(days=6)).strftime("%Y-%m-%d")
        return render(request, 'turfDateSelection.html', {'currentDate': currentDate, 'endDate': endDate})


def turfBilling(request):
    if request.method == 'POST':
        currentDate = date.today().strftime("%Y-%m-%d")
        selectedDate = request.POST['date']
        list_of_input_ids = request.POST.getlist('id')

        # Define the slot mapping for better readability and maintainability
        slot_mapping = {
            '0': '6-7 am',
            '1': '7-8 am',
            '2': '8-9 am',
            '3': '9-10 am',
            '4': '10-11 am',
            '5': '11-12 am',
            '6': '12-1 pm',
            '7': '1-2 pm',
            '8': '2-3 pm',
            '9': '3-4 pm',
            '10': '4-5 pm',
            '11': '5-6 pm',
            '12': '6-7 pm',
            '13': '7-8 pm',
            '14': '8-9 pm',
            '15': '9-10 pm',
            '16': '10-11 pm',
            '17': '11-12 pm',
            '18': '12-1 am',
        }

        # Prepare a list of booked slot labels
        bookedSlots = [slot_mapping[i] for i in list_of_input_ids if i in slot_mapping]

        # Calculate total amount based on number of slots booked
        totalAmount = len(bookedSlots) * 700
        booking_time = datetime.now(timezone("Asia/Kolkata")).strftime('%H:%M:%S')

        # Save booking details directly with slots stored as a list of strings
        turf = TurfBooked(
            name=request.user.username,
            email=request.user.email,
            amount=totalAmount,
            selected_date=selectedDate,
            booking_time=booking_time,
            slots=bookedSlots,  # Simplified list of strings
        )
        turf.save()

        # Prepare booking details for confirmation display
        details = {
            'username': request.user.username,
            'email': request.user.email,
            'selectedDate': selectedDate,
            'currentDate': currentDate,
            'bookedSlots': bookedSlots,
            'totalAmount': totalAmount,
            'list_of_input_ids': list_of_input_ids,
        }
        payment_id = 1  # Placeholder payment ID for testing
        return render(request, 'turfBilling.html', {'payment': payment_id, 'details': details})
    # Return to the form if the request is not a POST
    return render(request, 'turfBilling.html', {'details': None})



@csrf_exempt
def success(request):
    if request.method == "POST":
        total_amount = request.POST.get('total_amount')
        username = request.POST.get('username')
        email = request.POST.get('email')
        selected_date = request.POST.get('selected_date')

        # Generate current date and time internally
        current_date = datetime.now(timezone("Asia/Kolkata")).date()
        booking_time = datetime.now(timezone("Asia/Kolkata")).strftime('%H:%M:%S')

        slots = request.POST.getlist('slots')

        print(slots)

        # Map slot labels to their IDs (or use them as they are)
        slot_mapping = {
            '6-7 am': 1, '7-8 am': 2, '8-9 am': 3, '9-10 am': 4,
            '10-11 am': 5, '11-12 am': 6, '12-1 pm': 7, '1-2 pm': 8,
            '2-3 pm': 9, '3-4 pm': 10, '4-5 pm': 11, '5-6 pm': 12,
            '6-7 pm': 13, '7-8 pm': 14, '8-9 pm': 15, '9-10 pm': 16,
            '10-11 pm': 17, '11-12 pm': 18, '12-1 am': 19
        }

        bookedSlots = [slot_mapping[slot] for slot in slots if slot in slot_mapping]

        # Prepare the data to store in the `TurfBooked` JSON field
        structured_slots = [{"time": slot, "slot_id": slot_id} for slot, slot_id in zip(slots, bookedSlots)]

        # Save booking details directly with slots stored as JSON
        # turf = TurfBooked(
        #     name=request.user.username,
        #     email=request.user.email,
        #     amount=total_amount,
        #     selected_date=selected_date,
        #     booking_date=current_date,
        #     booking_time=booking_time,
        #     slots=structured_slots  # Store slots as structured JSON data
        # )
        # turf.save()

        return redirect('book_now')

    return render(request, 'success.html')




# def deleteRecord(dayTobeDeleated):
#     # Get all TurfBooked records for the specific date range or day
#     bookings = TurfBooked.objects.filter(selected_date__icontains=dayTobeDeleated)

#     for booking in bookings:
#         updated_slots = [slot for slot in booking.slots if slot['time'] != dayTobeDeleated]

#         # Update the booking entry with the modified slot list
#         booking.slots = updated_slots
#         booking.save()

    # Optionally, if you need to handle clearing slots for a specific day in a more complex way,
    # you can create logic to check for slot availability or handle edge cases.






def orderHistory(request):
    my_bookings = TurfBooked.objects.filter(email=request.user.email)
    slot_time_map = {
        1: '6-7 am', 2: '7-8 am', 3: '8-9 am', 4: '9-10 am', 5: '10-11 am',
        6: '11-12 am', 7: '12-1 pm', 8: '1-2 pm', 9: '2-3 pm', 10: '3-4 pm',
        11: '4-5 pm', 12: '5-6 pm', 13: '6-7 pm', 14: '7-8 pm', 15: '8-9 pm',
        16: '9-10 pm', 17: '10-11 pm', 18: '11-12 pm', 19: '12-1 am'
    }

    bookings_data = []
    for booking in my_bookings:
        print(f"Booking ID: {booking.id}, Selected Date: {booking.selected_date}, Current Date: {datetime.now().strftime('%Y-%m-%d')}")
        formatted_slots = [slot for slot in booking.slots]
        bookings_data.append({
            'booking_id': booking.id,
            'selected_date': booking.selected_date,
            'booking_date': booking.booking_date,
            'booking_time': booking.booking_time,
            'slots': [slot for slot in formatted_slots if slot],  # Filter out empty strings if any
            'amount': booking.amount,
        })

    currentDate = datetime.now().strftime("%Y-%m-%d")
    return render(request, 'orderHistory.html', {'bookings': bookings_data, 'currentDate': currentDate})





@login_required(login_url='login')
def delete_booking(request, id):
    if request.method == 'POST':
        # Get the booking object, return an error if not found
        booking = get_object_or_404(TurfBooked, id=id)

        # Log for debugging
        print(f"Deleting booking for {booking.name} on {booking.selected_date} at {booking.booking_time}")

        # Delete the booking from the TurfBooked table
        booking.delete()

        return redirect('orderHistory')  # Redirect to the order history page after deletion



@login_required(login_url='login')
def allBookings(request):
    # Get the currently logged-in user
    user = request.user

    # Filter bookings by the logged-in user and order by selected date and booking time
    bookings = TurfBooked.objects.filter(email=user.email).order_by('selected_date', 'booking_time')

    # Debug print to verify data structure in the terminal/logs (remove in production)
    for booking in bookings:
        print("Booking ID:", booking.id)
        print("Name:", booking.name)
        print("Booking Date:", booking.booking_date)
        print("Selected Date:", booking.selected_date)
        print("Booking Time:", booking.booking_time)
        print("Slots:", booking.slots)
        print("Amount:", booking.amount)

    # Get the current date for comparison
    currentDate = date.today().strftime("%Y-%m-%d")

    # Render the template and pass context
    return render(request, 'allBookings.html', {'bookings': bookings, 'currentDate': currentDate})






