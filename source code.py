import math

class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        return False

    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    def transfer(self, amount, destination):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {destination.name}')
            destination.deposit(amount, f'Transfer from {self.name}')
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = self.name.center(30, '*')
        lines = [title]
        for item in self.ledger:
            desc = item['description'][:23].ljust(23)
            amt = f"{item['amount']:.2f}"[:7].rjust(7)
            lines.append(desc + amt)
        lines.append(f"Total: {self.get_balance():.2f}")
        return '\n'.join(lines)


def create_spend_chart(categories):
    # Calculate total withdrawals per category
    withdrawals = []
    for cat in categories:
        total = sum(-item['amount'] for item in cat.ledger if item['amount'] < 0)
        withdrawals.append(total)

    grand_total = sum(withdrawals)
    percentages = [math.floor((w / grand_total) * 10) * 10 for w in withdrawals]

    # Build chart
    lines = ['Percentage spent by category']

    for level in range(100, -1, -10):
        row = f"{level:>3}|"
        for pct in percentages:
            row += ' o ' if pct >= level else '   '
        row += ' '
        lines.append(row)

    # Horizontal line
    lines.append('    ' + '-' * (len(categories) * 3 + 1))

    # Category names vertically
    max_len = max(len(cat.name) for cat in categories)
    for i in range(max_len):
        row = '    '
        for cat in categories:
            if i < len(cat.name):
                row += ' ' + cat.name[i] + ' '
            else:
                row += '   '
        row += ' '
        lines.append(row)

    return '\n'.join(lines)
