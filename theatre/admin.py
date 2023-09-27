from django.contrib import admin

from theatre.models import (Actor, Genre, Performance, Ticket, TheatreHall, Play, Reservation)

admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Performance)
admin.site.register(TheatreHall)
admin.site.register(Ticket)
admin.site.register(Play)
admin.site.register(Reservation)
