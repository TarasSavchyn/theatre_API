from django.contrib import admin

from theatre.models import (
    Actor,
    Genre,
    Performance,
    Ticket,
    TheatreHall,
    Play,
    Reservation, Rating,
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


class PlayAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'average_rating')

    readonly_fields = ('average_rating',)  # Make the 'average_rating' field read-only

admin.site.register(Play, PlayAdmin)


class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "play", "mark")

admin.site.register(Rating, RatingAdmin)
