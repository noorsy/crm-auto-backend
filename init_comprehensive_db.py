from app import app, db
from datetime import datetime, date, timedelta
import random

def init_comprehensive_database():
    """Initialize the database with comprehensive dummy data"""
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        print("Database tables created successfully!")
        
        from app import Customer, Loan, CustomerInteraction
        
        # Customer data with diverse profiles
        customers_data = [
            {
                "account_number": "1234567890",
                "first_name": "John",
                "last_name": "Doe",
                "email_address": "john.doe@email.com",
                "primary_phone_number": 5551234567,
                "ssn": 123456789,
                "dob": date(1980, 1, 15),
                "address_line_1": "123 Main Street",
                "address_line_2": "Apt 4B",
                "city": "New York",
                "state": "NY",
                "zip_code": 10001,
                "customer_number": 10001,
                "record_type": "responsible_party",
                "borrower_first_name": "John",
                "borrower_last_name": "Doe",
                "is_eligible_to_call": True,
                "transfer_phone_number": 5551111111,
                "transfer_ip_address": "192.168.1.100"
            },
            {
                "account_number": "2345678901",
                "first_name": "Sarah",
                "last_name": "Johnson",
                "email_address": "sarah.johnson@email.com",
                "primary_phone_number": 5552345678,
                "ssn": 234567890,
                "dob": date(1985, 6, 22),
                "address_line_1": "456 Oak Avenue",
                "address_line_2": None,
                "city": "Los Angeles",
                "state": "CA",
                "zip_code": 90210,
                "customer_number": 10002,
                "record_type": "responsible_party",
                "borrower_first_name": "Sarah",
                "borrower_last_name": "Johnson",
                "is_eligible_to_call": True,
                "transfer_phone_number": 5552222222,
                "transfer_ip_address": "192.168.1.101"
            },
            {
                "account_number": "3456789012",
                "first_name": "Michael",
                "last_name": "Brown",
                "email_address": "michael.brown@email.com",
                "primary_phone_number": 5553456789,
                "ssn": 345678901,
                "dob": date(1978, 11, 8),
                "address_line_1": "789 Pine Street",
                "address_line_2": "Unit 12",
                "city": "Chicago",
                "state": "IL",
                "zip_code": 60601,
                "customer_number": 10003,
                "record_type": "co_signer",
                "borrower_first_name": "Lisa",
                "borrower_last_name": "Brown",
                "is_eligible_to_call": True,
                "transfer_phone_number": 5553333333,
                "transfer_ip_address": "192.168.1.102"
            },
            {
                "account_number": "4567890123",
                "first_name": "Emily",
                "last_name": "Davis",
                "email_address": "emily.davis@email.com",
                "primary_phone_number": 5554567890,
                "ssn": 456789012,
                "dob": date(1992, 3, 14),
                "address_line_1": "321 Elm Drive",
                "address_line_2": "Apt 5A",
                "city": "Houston",
                "state": "TX",
                "zip_code": 77001,
                "customer_number": 10004,
                "record_type": "responsible_party",
                "borrower_first_name": "Emily",
                "borrower_last_name": "Davis",
                "is_eligible_to_call": False,
                "transfer_phone_number": 5554444444,
                "transfer_ip_address": "192.168.1.103"
            },
            {
                "account_number": "5678901234",
                "first_name": "Robert",
                "last_name": "Wilson",
                "email_address": "robert.wilson@email.com",
                "primary_phone_number": 5555678901,
                "ssn": 567890123,
                "dob": date(1975, 9, 30),
                "address_line_1": "654 Maple Lane",
                "address_line_2": None,
                "city": "Phoenix",
                "state": "AZ",
                "zip_code": 85001,
                "customer_number": 10005,
                "record_type": "responsible_party",
                "borrower_first_name": "Robert",
                "borrower_last_name": "Wilson",
                "is_eligible_to_call": True,
                "transfer_phone_number": 5555555555,
                "transfer_ip_address": "192.168.1.104"
            }
        ]
        
        # Create customers
        customers = []
        for customer_data in customers_data:
            customer = Customer(**customer_data)
            db.session.add(customer)
            customers.append(customer)
        
        db.session.commit()
        print(f"Created {len(customers)} customers")
        
        # Loan data with different scenarios
        loans_data = [
            {
                "product_name": "Auto Loan Premium",
                "due_amount": 1250.00,
                "no_of_missed_installments": 0,
                "contractual_installment_amount": 425.50,
                "interest_late_fee": 25.00,
                "minimum_amount": 50.00,
                "acceptable_pay_later_date": date(2024, 2, 15),
                "acceptable_already_paid_date": date(2024, 1, 31),
                "grace_period_date": date(2024, 2, 10),
                "due_date": date(2024, 1, 31),
                "status": "active"
            },
            {
                "product_name": "Personal Loan Standard",
                "due_amount": 875.00,
                "no_of_missed_installments": 1,
                "contractual_installment_amount": 350.00,
                "interest_late_fee": 45.00,
                "minimum_amount": 75.00,
                "acceptable_pay_later_date": date(2024, 2, 20),
                "acceptable_already_paid_date": date(2024, 1, 25),
                "grace_period_date": date(2024, 2, 5),
                "due_date": date(2024, 1, 25),
                "status": "past_due"
            },
            {
                "product_name": "Auto Loan Standard",
                "due_amount": 2100.00,
                "no_of_missed_installments": 2,
                "contractual_installment_amount": 525.00,
                "interest_late_fee": 85.00,
                "minimum_amount": 100.00,
                "acceptable_pay_later_date": date(2024, 2, 25),
                "acceptable_already_paid_date": date(2024, 1, 20),
                "grace_period_date": date(2024, 1, 30),
                "due_date": date(2024, 1, 20),
                "status": "delinquent"
            },
            {
                "product_name": "Personal Loan Plus",
                "due_amount": 0.00,
                "no_of_missed_installments": 0,
                "contractual_installment_amount": 275.00,
                "interest_late_fee": 0.00,
                "minimum_amount": 25.00,
                "acceptable_pay_later_date": date(2024, 2, 28),
                "acceptable_already_paid_date": date(2024, 2, 1),
                "grace_period_date": date(2024, 2, 15),
                "due_date": date(2024, 2, 1),
                "status": "current"
            },
            {
                "product_name": "Auto Loan Deluxe",
                "due_amount": 3150.00,
                "no_of_missed_installments": 3,
                "contractual_installment_amount": 650.00,
                "interest_late_fee": 125.00,
                "minimum_amount": 150.00,
                "acceptable_pay_later_date": date(2024, 3, 1),
                "acceptable_already_paid_date": date(2024, 1, 15),
                "grace_period_date": date(2024, 1, 25),
                "due_date": date(2024, 1, 15),
                "status": "default"
            }
        ]
        
        # Create loans
        loans = []
        for i, loan_data in enumerate(loans_data):
            loan_data["customer_id"] = customers[i].id
            loan = Loan(**loan_data)
            db.session.add(loan)
            loans.append(loan)
        
        db.session.commit()
        print(f"Created {len(loans)} loans")
        
        # Comprehensive interaction scenarios
        interaction_scenarios = [
            # Customer 1: John Doe - Recent successful payment
            [
                {
                    "creation_date": datetime(2024, 1, 28, 14, 30, 0),
                    "last_updated_date": date(2024, 1, 28),
                    "source": "Inbound Call",
                    "status": "Completed",
                    "notes": "Customer called to confirm payment due date. Provided payment information and confirmed auto-pay setup."
                },
                {
                    "creation_date": datetime(2024, 1, 30, 9, 15, 0),
                    "last_updated_date": date(2024, 1, 30),
                    "source": "Payment System",
                    "status": "Processed",
                    "notes": "Payment of $425.50 successfully processed via auto-pay. Account current."
                },
                {
                    "creation_date": datetime(2024, 2, 1, 10, 0, 0),
                    "last_updated_date": date(2024, 2, 1),
                    "source": "System Generated",
                    "status": "Sent",
                    "notes": "Payment confirmation email sent to customer."
                }
            ],
            # Customer 2: Sarah Johnson - Late payment with arrangement
            [
                {
                    "creation_date": datetime(2024, 1, 26, 16, 45, 0),
                    "last_updated_date": date(2024, 1, 26),
                    "source": "Outbound Call",
                    "status": "No Answer",
                    "notes": "Attempted to contact customer regarding upcoming payment due 1/25. Left voicemail."
                },
                {
                    "creation_date": datetime(2024, 1, 27, 11, 20, 0),
                    "last_updated_date": date(2024, 1, 27),
                    "source": "Inbound Call",
                    "status": "Completed",
                    "notes": "Customer returned call. Explained temporary financial hardship. Arranged payment extension to 2/20."
                },
                {
                    "creation_date": datetime(2024, 1, 28, 13, 10, 0),
                    "last_updated_date": date(2024, 1, 28),
                    "source": "Email",
                    "status": "Sent",
                    "notes": "Payment arrangement confirmation sent via email. Customer agreed to pay $350 + $45 late fee by 2/20."
                },
                {
                    "creation_date": datetime(2024, 2, 1, 8, 30, 0),
                    "last_updated_date": date(2024, 2, 1),
                    "source": "System Generated",
                    "status": "Active",
                    "notes": "Payment reminder sent. Account shows 1 missed installment. Extension in effect until 2/20."
                }
            ],
            # Customer 3: Michael Brown - Multiple missed payments, collections
            [
                {
                    "creation_date": datetime(2024, 1, 21, 9, 0, 0),
                    "last_updated_date": date(2024, 1, 21),
                    "source": "Outbound Call",
                    "status": "No Answer",
                    "notes": "First attempt to contact regarding missed payment due 1/20. No answer, no voicemail option."
                },
                {
                    "creation_date": datetime(2024, 1, 22, 14, 30, 0),
                    "last_updated_date": date(2024, 1, 22),
                    "source": "Outbound Call",
                    "status": "Busy",
                    "notes": "Second attempt - line busy. Will retry tomorrow."
                },
                {
                    "creation_date": datetime(2024, 1, 23, 10, 15, 0),
                    "last_updated_date": date(2024, 1, 23),
                    "source": "Outbound Call",
                    "status": "Completed",
                    "notes": "Connected with customer. Acknowledged missed payments. Promised to pay by end of week. Customer seems cooperative."
                },
                {
                    "creation_date": datetime(2024, 1, 29, 15, 45, 0),
                    "last_updated_date": date(2024, 1, 29),
                    "source": "Outbound Call",
                    "status": "Completed",
                    "notes": "Follow-up call. Customer failed to make promised payment. Now 2 payments behind. Discussed payment plan options."
                },
                {
                    "creation_date": datetime(2024, 2, 2, 11, 0, 0),
                    "last_updated_date": date(2024, 2, 2),
                    "source": "Collections Notice",
                    "status": "Sent",
                    "notes": "Formal collections notice mailed. Account seriously delinquent with 2 missed payments totaling $1,050."
                }
            ],
            # Customer 4: Emily Davis - Payment dispute resolution
            [
                {
                    "creation_date": datetime(2024, 1, 25, 12, 0, 0),
                    "last_updated_date": date(2024, 1, 25),
                    "source": "Inbound Call",
                    "status": "Completed",
                    "notes": "Customer disputes payment amount. Claims payment was made but not reflected. Initiated payment investigation."
                },
                {
                    "creation_date": datetime(2024, 1, 26, 9, 30, 0),
                    "last_updated_date": date(2024, 1, 26),
                    "source": "Internal System",
                    "status": "In Progress",
                    "notes": "Payment research initiated. Checking with bank for payment posting delays. Case #PR-2024-0156 opened."
                },
                {
                    "creation_date": datetime(2024, 1, 28, 16, 20, 0),
                    "last_updated_date": date(2024, 1, 28),
                    "source": "Bank Verification",
                    "status": "Resolved",
                    "notes": "Payment confirmed - posting delay due to bank processing. Payment of $275 applied retroactively. Account current."
                },
                {
                    "creation_date": datetime(2024, 1, 29, 10, 45, 0),
                    "last_updated_date": date(2024, 1, 29),
                    "source": "Outbound Call",
                    "status": "Completed",
                    "notes": "Called customer to confirm resolution. Payment posted correctly. Apologized for inconvenience. Customer satisfied."
                }
            ],
            # Customer 5: Robert Wilson - Severe delinquency, default procedures
            [
                {
                    "creation_date": datetime(2024, 1, 16, 8, 0, 0),
                    "last_updated_date": date(2024, 1, 16),
                    "source": "System Generated",
                    "status": "Sent",
                    "notes": "First missed payment notice sent for payment due 1/15. Amount due: $650."
                },
                {
                    "creation_date": datetime(2024, 1, 18, 13, 30, 0),
                    "last_updated_date": date(2024, 1, 18),
                    "source": "Outbound Call",
                    "status": "No Answer",
                    "notes": "Attempted contact - no answer. Left urgent voicemail requesting immediate callback."
                },
                {
                    "creation_date": datetime(2024, 1, 22, 10, 0, 0),
                    "last_updated_date": date(2024, 1, 22),
                    "source": "Certified Mail",
                    "status": "Sent",
                    "notes": "Certified demand letter sent. Customer has 10 days to respond or account will proceed to default."
                },
                {
                    "creation_date": datetime(2024, 1, 30, 14, 15, 0),
                    "last_updated_date": date(2024, 1, 30),
                    "source": "Legal Department",
                    "status": "Initiated",
                    "notes": "No response to certified letter. Account transferred to legal for default proceedings. 3 payments missed."
                },
                {
                    "creation_date": datetime(2024, 2, 1, 16, 0, 0),
                    "last_updated_date": date(2024, 2, 1),
                    "source": "Collections Agency",
                    "status": "Transferred",
                    "notes": "Account transferred to external collections agency. Total amount due: $3,150 including fees."
                }
            ]
        ]
        
        # Create interactions
        total_interactions = 0
        for i, customer_interactions in enumerate(interaction_scenarios):
            for interaction_data in customer_interactions:
                interaction_data["customer_id"] = customers[i].id
                interaction = CustomerInteraction(**interaction_data)
                db.session.add(interaction)
                total_interactions += 1
        
        db.session.commit()
        print(f"Created {total_interactions} customer interactions")
        
        # Print summary
        print("\n" + "="*50)
        print("DATABASE INITIALIZATION COMPLETE")
        print("="*50)
        
        for i, customer in enumerate(customers):
            loan = loans[i]
            interaction_count = len(interaction_scenarios[i])
            print(f"\nCustomer {i+1}: {customer.first_name} {customer.last_name}")
            print(f"  Phone: {customer.primary_phone_number}")
            print(f"  Account: {customer.account_number}")
            print(f"  Loan: {loan.product_name} - {loan.status}")
            print(f"  Due Amount: ${loan.due_amount}")
            print(f"  Missed Payments: {loan.no_of_missed_installments}")
            print(f"  Interactions: {interaction_count}")
        
        print(f"\nTotal Records Created:")
        print(f"  Customers: {len(customers)}")
        print(f"  Loans: {len(loans)}")
        print(f"  Interactions: {total_interactions}")
        print("\nReady for testing!")

if __name__ == '__main__':
    init_comprehensive_database() 