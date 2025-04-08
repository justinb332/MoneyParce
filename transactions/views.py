from django.shortcuts import redirect, render, get_object_or_404

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

def edit_transaction(request, name):
    transaction = get_object_or_404(Transaction, name=name)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('home')  # Adjust the redirect as necessary
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transactions/edit_transaction.html', {'form': form})

def home(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'home/home.html', {'transactions': transactions})