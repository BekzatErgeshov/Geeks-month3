from database.db import SessionLocal
from database.models import Transaction, Category

def create_transaction(amount, type_, category_id, description):
    session = SessionLocal()
    try:
        transaction = Transaction(
            amount=amount,
            type=type_,
            category_id=category_id,
            description=description
        )
        session.add(transaction)
        session.commit()
    finally:
        session.close()


def delete_transaction(transaction_id):
    session = SessionLocal()
    try:
        transaction = session.get(Transaction, transaction_id)
        if transaction:
            session.delete(transaction)
            session.commit()
    finally:
        session.close()


def get_all_transactions():
    session = SessionLocal()
    try:
        data = session.query(Transaction).all()
        # Загружаем категории для каждой транзакции перед закрытием сессии
        for t in data:
            if t.category:
                _ = t.category.name
        return data
    finally:
        session.close()


def get_transactions_by_type(type_):
    session = SessionLocal()
    try:
        data = session.query(Transaction).filter(Transaction.type == type_).all()
        for t in data:
            if t.category:
                _ = t.category.name
        return data
    finally:
        session.close()


def get_transactions_by_category(category_id):
    session = SessionLocal()
    try:
        data = session.query(Transaction).filter(Transaction.category_id == category_id).all()
        for t in data:
            if t.category:
                _ = t.category.name
        return data
    finally:
        session.close()


def get_categories():
    session = SessionLocal()
    try:
        categories = session.query(Category).all()
        return categories
    finally:
        session.close()


def calculate_balance():
    session = SessionLocal()
    try:
        transactions = session.query(Transaction).all()
        balance = 0
        for t in transactions:
            if t.type == "income":
                balance += t.amount
            else:
                balance -= t.amount
        return balance
    finally:
        session.close()