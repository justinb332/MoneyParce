from django.shortcuts import redirect, render

from .forms import TransactionForm
from .models import Transaction


def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TransactionForm()

    return render(request, 'transactions/add_transaction.html', {'form': form})

def home(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'home/home.html', {'transactions': transactions})