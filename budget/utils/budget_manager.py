from budget.models import Budget

class BudgetManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BudgetManager, cls).__new__(cls)
        return cls._instance

    def get_budget_summaries(self, user):

        budgets = Budget.objects.filter(user=user).order_by('timeframe')

        budget_data = []
        for budget in budgets:
            total_spent = budget.total_spent(budget.timeframe)
            remaining_amount = budget.amount - total_spent
            over_budget = total_spent - budget.amount if total_spent > budget.amount else None

            budget.remaining_amount = remaining_amount
            budget.over_budget = over_budget

            budget_data.append({
                'budget': budget,
                'total_spent': total_spent,
            })

        return budget_data
