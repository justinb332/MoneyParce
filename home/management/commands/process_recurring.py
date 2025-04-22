import datetime
from calendar import monthrange

from django.core.management.base import BaseCommand
from django.utils.timezone import now, make_aware
from expense.models import Expense
from income.models import Income

def start_of_day(dt):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

def calculate_next_occurrence(current, period, day_of_week=None, day_of_month=None):
    current = start_of_day(current)

    if period == 'daily':
        return current + datetime.timedelta(days=1)

    elif period == 'weekly' and day_of_week:
        weekdays = {
            'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6,
        }
        target = weekdays.get(day_of_week.lower(), 0)
        days_ahead = (target - current.weekday() + 7) % 7
        if days_ahead == 0:
            days_ahead = 7
        return current + datetime.timedelta(days=days_ahead)

    elif period == 'monthly' and day_of_month:
        year = current.year
        month = current.month + 1
        if month > 12:
            month = 1
            year += 1
        day = min(day_of_month, monthrange(year, month)[1])
        return datetime.datetime(year, month, day)

    return None

class Command(BaseCommand):
    help = 'Processes recurring expenses and incomes at the start of each day.'

    def handle(self, *args, **kwargs):
        today = start_of_day(now())

        for e in Expense.objects.filter(is_recurring=True, next_occurrence__lte=today):
            while e.next_occurrence and start_of_day(e.next_occurrence) <= today:
                current = start_of_day(e.next_occurrence)

                Expense.objects.create(
                    name=e.name,
                    amount=e.amount,
                    category=e.category,
                    notes=e.notes,
                    is_recurring=e.is_recurring,
                    recurrence_period=e.recurrence_period,
                    recurrence_day_of_week=e.recurrence_day_of_week,
                    recurrence_day_of_month=e.recurrence_day_of_month,
                    next_occurrence=None,
                    date=current
                )

                e.next_occurrence = calculate_next_occurrence(
                    current,
                    e.recurrence_period,
                    e.recurrence_day_of_week,
                    e.recurrence_day_of_month
                )
            e.save()

        for i in Income.objects.filter(is_recurring=True, next_occurrence__lte=today):
            while i.next_occurrence and start_of_day(i.next_occurrence) <= today:
                current = start_of_day(i.next_occurrence)

                Income.objects.create(
                    name=i.name,
                    amount=i.amount,
                    category=i.category,
                    notes=i.notes,
                    is_recurring=i.is_recurring,
                    recurrence_period=i.recurrence_period,
                    recurrence_day_of_week=i.recurrence_day_of_week,
                    recurrence_day_of_month=i.recurrence_day_of_month,
                    next_occurrence=None,
                    date=current
                )

                i.next_occurrence = calculate_next_occurrence(
                    current,
                    i.recurrence_period,
                    i.recurrence_day_of_week,
                    i.recurrence_day_of_month
                )
            i.save()

        self.stdout.write(self.style.SUCCESS("Recurring transactions processed for start of day."))

