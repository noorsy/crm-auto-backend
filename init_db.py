from app import app, db
from datetime import datetime, date

def init_database():
    """Initialize the database with the new schema"""
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        print("Database tables created successfully!")
        
        # Add sample data based on your specification
        from app import Customer, Loan, CustomerInteraction
        
        # Sample customer data
        sample_customer = Customer(
            account_number="1234567890",
            first_name="John",
            last_name="Doe",
            email_address="test@example.com",
            primary_phone_number=5551234567,
            ssn=6789,
            dob=date(1980, 1, 1),
            address_line_1="123 Main Street",
            address_line_2="Apt 4B",
            city="New York",
            state="NY",
            zip_code=12345,
            customer_number=10,
            record_type="responsible_party",
            borrower_first_name="John",
            borrower_last_name="Doe",
            is_eligible_to_call=True,
            transfer_phone_number=0,
            transfer_ip_address="0000:0000:0000:0000"
        )
        
        db.session.add(sample_customer)
        db.session.commit()
        
        # Sample loan data
        sample_loan = Loan(
            customer_id=sample_customer.id,
            product_name="Doe",
            due_amount=1000,
            no_of_missed_installments=1,
            contractual_installment_amount=100,
            interest_late_fee=4,
            minimum_amount=10,
            acceptable_pay_later_date=date(2023, 6, 30),
            acceptable_already_paid_date=date(2023, 6, 30),
            grace_period_date=date(2023, 6, 30),
            due_date=date(2023, 6, 30),
            status="Active"
        )
        
        db.session.add(sample_loan)
        db.session.commit()
        
        # Sample interaction data
        sample_interaction = CustomerInteraction(
            customer_id=sample_customer.id,
            creation_date=datetime(2023, 6, 30, 15, 0, 0),
            last_updated_date=date(2023, 6, 11),
            source="Internal System",
            status="Active",
            notes="Customer requested payment extension"
        )
        
        db.session.add(sample_interaction)
        db.session.commit()
        
        print("Sample data inserted successfully!")
        print(f"Created customer: {sample_customer.first_name} {sample_customer.last_name}")
        print(f"Created loan with ID: {sample_loan.id}")
        print(f"Created interaction with ID: {sample_interaction.id}")

if __name__ == '__main__':
    init_database() 