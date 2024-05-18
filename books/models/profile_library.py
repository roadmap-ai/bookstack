from django.db import models
from djmoney.models.fields import MoneyField
from statemachine import State, StateMachine
from statemachine.mixins import MachineMixin


class BookReadingWorkflow(StateMachine):
    to_be_read = State("To Be Read", initial=True)
    currently_reading = State("Currently Reading")
    read = State("Read")
    paused_reading = State("Paused Reading")
    archived = State("Archived")

    start = to_be_read.to(currently_reading)
    finish = currently_reading.to(read)
    pause = currently_reading.to(paused_reading)
    archive = read.to(archived) | paused_reading.to(archived)
    restart = read.to(currently_reading)
    resume = paused_reading.to(currently_reading) | archived.to(currently_reading)


class ProfileLibrary(models.Model, MachineMixin):
    class OwnershipType(models.TextChoices):
        e_book = "E-Book"
        audio_book = "Audio Book"
        owned_physical_book = "Owned Physical Book"
        borrowed_book = "Borrowed Book"

    profile = models.ForeignKey("books.Profile", on_delete=models.CASCADE)
    book = models.ForeignKey("books.Book", on_delete=models.PROTECT)
    ownership_type = models.CharField(
        choices=OwnershipType, default=OwnershipType.owned_physical_book, max_length=50
    )
    notes = models.TextField(null=True)
    price = MoneyField(max_digits=14, decimal_places=2, null=True)
    # read_till_chapter = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state_machine_name = "BookReadingWorkflow"
    state_machine_attr = "sm"
    state_field_name = "state"
    state = models.CharField(default=BookReadingWorkflow.to_be_read.value)
