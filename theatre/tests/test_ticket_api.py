from django.test import TestCase
from theatre.models import Ticket, Reservation, Performance, TheatreHall, Play
from django.contrib.auth import get_user_model
from datetime import datetime


class TicketModelTest(TestCase):
    def setUp(self):
        # Create a test User
        self.user = get_user_model().objects.create_user("test@test.ua", "test123")

        # Create a test Play, TheatreHall, and Performance
        self.play = Play.objects.create(title="Test Play", description="A test play")
        self.theatre_hall = TheatreHall.objects.create(
            name="Main Hall", rows=10, seats_in_row=12
        )
        self.performance = Performance.objects.create(
            play=self.play, theatre_hall=self.theatre_hall, show_time=datetime.now()
        )

        # Create a test Reservation
        self.reservation = Reservation.objects.create(user=self.user)

        # Create a test Ticket
        self.ticket = Ticket.objects.create(
            reservation=self.reservation, performance=self.performance, seat=1, row=1
        )

    def test_read_ticket(self):
        # Retrieve an existing Ticket object
        ticket = Ticket.objects.get(id=self.ticket.id)
        # Ensure that the associated Reservation, Performance, and user match the expected values
        self.assertEqual(ticket.reservation.user.email, "test@test.ua")
        self.assertEqual(ticket.performance.play.title, "Test Play")
        self.assertEqual(ticket.performance.theatre_hall.name, "Main Hall")
        self.assertEqual(ticket.seat, 1)
        self.assertEqual(ticket.row, 1)

    def test_update_ticket(self):
        # Update the seat number and row number of the Ticket
        self.ticket.seat = 5
        self.ticket.row = 2
        self.ticket.save()
        # Retrieve the updated Ticket
        updated_ticket = Ticket.objects.get(id=self.ticket.id)
        # Check if the seat number and row number have been successfully updated
        self.assertEqual(updated_ticket.seat, 5)
        self.assertEqual(updated_ticket.row, 2)

    def test_delete_ticket(self):
        # Delete the Ticket
        self.ticket.delete()
        # Attempt to retrieve the deleted Ticket (should raise Ticket.DoesNotExist)
        with self.assertRaises(Ticket.DoesNotExist):
            Ticket.objects.get(id=self.ticket.id)

    def test_str_representation(self):
        # Check the __str__ representation of the Ticket
        expected_str = f"Ticket for {self.performance.play.title}, Row {self.ticket.row}, Seat {self.ticket.seat}"
        self.assertEqual(str(self.ticket), expected_str)
