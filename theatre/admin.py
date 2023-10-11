from django.contrib import admin

from theatre.models import (
    Actor,
    Genre,
    Performance,
    Ticket,
    TheatreHall,
    Play,
    Reservation,
)


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Performance)
admin.site.register(TheatreHall)
admin.site.register(Ticket)
admin.site.register(Play)
