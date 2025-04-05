from django.shortcuts import render

from transactions.models import Transaction


def home(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'home/home.html', {'transactions': transactions})


def add_transaction(request):
    return render(request, 'transactions/add_transaction.html')