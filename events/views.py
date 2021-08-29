from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Venue
from .models import Event
from .models import MyClubUser
from .forms import VenueForm, EventForm
from django.http import HttpResponseRedirect, HttpResponse

from django.core.paginator import Paginator

def venue_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=venues.csv'
	
	writer = csv.writer(response)
	
	venues = Venue.objects.all()
	
	writer.writerow(['Venue Name','Address','Phone','Zip Code','Website','Email Address'])
	
	for venue in venues:
		writer.writerow([venue.name,venue.address,venue.phone,venue.zip_code,venue.web,venue.email_address])
	
	return response

def venue_text(request):
	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=venues.txt'
	
	venues = Venue.objects.all()
	
	lines = []
	
	for venue in venues:
		lines.append(f'Name:- {venue.name}\nAddress:- {venue.address}\nPhone:- {venue.phone}\nZipcode:- {venue.zip_code}\nWebsite Address:- {venue.web}\nEmail Address:- {venue.email_address}\n\n\n')
	
	response.writelines(lines)
	return response

def delete_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	venue.delete()
	return redirect('query_venue')

def delete_event(request,event_id):
	event = Event.objects.get(pk=event_id)
	event.delete()
	return redirect('list-events')

def update_event(request,event_id):
	event = Event.objects.get(pk=event_id)
	form = EventForm(request.POST or None, instance=event)
	if form.is_valid():
			form.save()
			return redirect('list-events')
	return render(request, 'events/update_event.html',{'event':event,
	'form':form})

def add_event(request):
	submitted = False
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/add_event?submitted=True')
	else:
		form = EventForm
		if 'submitted' in request.GET:
			submitted = True
			
	return render(request,'events/add_event.html',{'form':form,'submitted':submitted})

def update_venue(request,venue_id):
	venue = Venue.objects.get(pk=venue_id)
	form = VenueForm(request.POST or None, instance=venue)
	if form.is_valid():
			form.save()
			return redirect('query_venue')
	return render(request, 'events/update_venue.html',{'venue':venue,
	'form':form})

def search_venue(request):
	if request.method == 'POST':
		searched = request.POST['searched']
		venues = Venue.objects.filter(name__contains=searched)
		return render(request, 'events/search_venues.html',{'searched':searched,
		'venues':venues})
	
	else:
		return render(request, 'events/search_venues.html',{})

def show_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	return render(request, 'events/show_venue.html', {'venue':venue})

def query_venue(request):
	venue_list = Venue.objects.all()
	
	p = Paginator(Venue.objects.all(), 10)
	page = request.GET.get('page')
	venues = p.get_page(page)
	nums = 'a' * venues.paginator.num_pages
	return render(request,'events/venue.html',
		{'venue_list':venue_list,
		'venues':venues,
		'nums':nums}
	)

def add_venue(request):
	submitted = False
	if request.method == 'POST':
		form = VenueForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/add_venue?submitted=True')
	else:
		form = VenueForm
		if 'submitted' in request.GET:
			submitted = True
			
	return render(request,'events/add_venue.html',{'form':form,'submitted':submitted})

def all_events(request):
	event_list = Event.objects.all().order_by('event_date')
	
	
	p = Paginator(Event.objects.all(), 10)
	page = request.GET.get('page')
	events = p.get_page(page)
	nums = 'a' * events.paginator.num_pages
	
	return render(request,'events/event_list.html',
		{'event_list':event_list,
		'events':events,
		'nums':nums}
	)

# Create your views here.
def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	name = 'Mokshit'
	month = month.capitalize()
	month_num = list(calendar.month_name).index(month)
	month_num = int(month_num)
	
	cal = HTMLCalendar().formatmonth(
		year,
		month_num
	)
	return render(request, 'events/home.html', 
		{'name':name,
		'year': year,
		'month': month,
		'cal': cal,
		})