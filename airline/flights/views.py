from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Flight, Passenger

# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers" : flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })

def book(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    if request.method == "POST":
        passenger = get_object_or_404(Passenger, pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flights:flight", args=(flight.id,)))
