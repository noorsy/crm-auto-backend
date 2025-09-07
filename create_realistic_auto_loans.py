from app import app, db
from datetime import datetime, date, timedelta
import random

def create_realistic_auto_loan_customers():
    """Create 5 realistic auto loan customers with car-specific scenarios"""
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        print("🚀 Database tables created successfully!")
        
        from app import Customer, Loan, CustomerInteraction
        
        # Realistic Auto Loan Customer Data
        auto_loan_customers = [
            {
                # Michael Rodriguez - Audi Q5, 5 payments made, 10 days past due
                'account_number': '1001234567',
                'first_name': 'Michael',
                'last_name': 'Rodriguez',
                'email_address': 'michael.rodriguez@email.com',
                'primary_phone_number': '5551234567',
                'ssn': '123456789',
                'dob': date(1985, 3, 22),
                'address_line_1': '1247 Beverly Hills Dr',
                'address_line_2': 'Unit 301',
                'city': 'Los Angeles',
                'state': 'CA',
                'zip_code': '90210',
                'customer_number': '10001',
                'record_type': 'responsible_party',
                'borrower_first_name': 'Michael',
                'borrower_last_name': 'Rodriguez',
                'is_eligible_to_call': True,
                'transfer_phone_number': '5551111111',
                'transfer_ip_address': '192.168.1.100',
                'credit_score': '745',
                'monthly_income': 95000.00,
                'employment_status': 'Full-time'
            },
            {
                # Sarah Chen - BMW X3, current on payments
                'account_number': '2001234567',
                'first_name': 'Sarah',
                'last_name': 'Chen',
                'email_address': 'sarah.chen@email.com',
                'primary_phone_number': '5552345678',
                'ssn': '234567890',
                'dob': date(1988, 7, 14),
                'address_line_1': '2850 Northside Dr',
                'address_line_2': 'Apt 12B',
                'city': 'Atlanta',
                'state': 'GA',
                'zip_code': '30309',
                'customer_number': '10002',
                'record_type': 'responsible_party',
                'borrower_first_name': 'Sarah',
                'borrower_last_name': 'Chen',
                'is_eligible_to_call': True,
                'transfer_phone_number': '5552222222',
                'transfer_ip_address': '192.168.1.101',
                'credit_score': '785',
                'monthly_income': 110000.00,
                'employment_status': 'Full-time'
            },
            {
                # David Thompson - Mercedes C-Class, 3 missed payments, 45 days past due
                'account_number': '3001234567',
                'first_name': 'David',
                'last_name': 'Thompson',
                'email_address': 'david.thompson@email.com',
                'primary_phone_number': '5553456789',
                'ssn': '345678901',
                'dob': date(1979, 11, 8),
                'address_line_1': '3421 Mercedes Blvd',
                'address_line_2': '',
                'city': 'Miami',
                'state': 'FL',
                'zip_code': '33101',
                'customer_number': '10003',
                'record_type': 'responsible_party',
                'borrower_first_name': 'David',
                'borrower_last_name': 'Thompson',
                'is_eligible_to_call': True,
                'transfer_phone_number': '5553333333',
                'transfer_ip_address': '192.168.1.102',
                'credit_score': '695',
                'monthly_income': 85000.00,
                'employment_status': 'Full-time'
            },
            {
                # Jennifer Martinez - Toyota Camry, 1 missed payment, 25 days past due
                'account_number': '4001234567',
                'first_name': 'Jennifer',
                'last_name': 'Martinez',
                'email_address': 'jennifer.martinez@email.com',
                'primary_phone_number': '5554567890',
                'ssn': '456789012',
                'dob': date(1983, 9, 17),
                'address_line_1': '4892 Toyota Ave',
                'address_line_2': 'Building C',
                'city': 'Denver',
                'state': 'CO',
                'zip_code': '80201',
                'customer_number': '10004',
                'record_type': 'responsible_party',
                'borrower_first_name': 'Jennifer',
                'borrower_last_name': 'Martinez',
                'is_eligible_to_call': True,
                'transfer_phone_number': '5554444444',
                'transfer_ip_address': '192.168.1.103',
                'credit_score': '672',
                'monthly_income': 68000.00,
                'employment_status': 'Full-time'
            },
            {
                # James Anderson - Honda Accord, 2 missed payments, 35 days past due
                'account_number': '5001234567',
                'first_name': 'James',
                'last_name': 'Anderson',
                'email_address': 'james.anderson@email.com',
                'primary_phone_number': '5555678901',
                'ssn': '567890123',
                'dob': date(1986, 2, 25),
                'address_line_1': '5678 Honda Street',
                'address_line_2': 'Unit 15',
                'city': 'Portland',
                'state': 'OR',
                'zip_code': '97201',
                'customer_number': '10005',
                'record_type': 'responsible_party',
                'borrower_first_name': 'James',
                'borrower_last_name': 'Anderson',
                'is_eligible_to_call': True,
                'transfer_phone_number': '5555555555',
                'transfer_ip_address': '192.168.1.104',
                'credit_score': '658',
                'monthly_income': 52000.00,
                'employment_status': 'Full-time'
            }
        ]
        
        # Create customers
        customers = []
        for customer_data in auto_loan_customers:
            customer = Customer(**customer_data)
            db.session.add(customer)
            customers.append(customer)
        
        db.session.commit()
        print(f"✅ Created {len(customers)} realistic auto loan customers")
        
        # Realistic Auto Loan Data (product_name = car name)
        auto_loans_data = [
            {
                # Michael Rodriguez - 2023 Audi Q5, 5 payments made, 10 days past due
                'customer_id': customers[0].id,
                'product_name': '2023 Audi Q5',
                'loan_amount': 65000.00,
                'due_amount': 1285.50,  # Current amount due
                'no_of_missed_installments': '1',  # String field
                'contractual_installment_amount': 1285.50,
                'interest_late_fee': 45.00,
                'minimum_amount': 128.55,  # 10% of payment
                'acceptable_pay_later_date': date(2024, 2, 15),
                'acceptable_already_paid_date': date(2024, 1, 31),
                'grace_period_date': date(2024, 2, 10),
                'due_date': date(2024, 1, 31),
                'term_months': '60',  # 5 year loan
                'days_past_due': '10',  # String field
                'interest_rate': 4.2,
                'maturity_date': date(2029, 1, 31),  # 5 years from start
                'next_due_date': date(2024, 2, 28),
                'final_amount': 77130.00,  # Total with interest
                'new_due_date': date(2024, 2, 15),  # Rescheduled
                'insurance_status': 'Active',
                'insurance_expiry_date': date(2024, 12, 31),
                'payoff_effect': 'Standard Payoff',
                'principal_amount': 65000.00,
                'last_payment_amount': 1285.50,
                'next_due_amount': 1285.50
            },
            {
                # Sarah Chen - 2022 BMW X3, current on payments
                'customer_id': customers[1].id,
                'product_name': '2022 BMW X3',
                'loan_amount': 58000.00,
                'due_amount': 0.00,  # Current - no amount due
                'no_of_missed_installments': '0',
                'contractual_installment_amount': 1165.20,
                'interest_late_fee': 0.00,
                'minimum_amount': 116.52,
                'acceptable_pay_later_date': date(2024, 3, 15),
                'acceptable_already_paid_date': date(2024, 2, 28),
                'grace_period_date': date(2024, 3, 10),
                'due_date': date(2024, 2, 28),
                'term_months': '60',
                'days_past_due': '0',
                'interest_rate': 3.9,
                'maturity_date': date(2027, 8, 28),
                'next_due_date': date(2024, 3, 31),
                'final_amount': 69912.00,
                'new_due_date': date(2024, 3, 31),
                'insurance_status': 'Active',
                'insurance_expiry_date': date(2025, 6, 30),
                'payoff_effect': 'Standard Payoff',
                'principal_amount': 58000.00,
                'last_payment_amount': 1165.20,
                'next_due_amount': 1165.20
            },
            {
                # David Thompson - 2021 Mercedes C-Class, 3 missed payments, 45 days past due
                'customer_id': customers[2].id,
                'product_name': '2021 Mercedes C-Class',
                'loan_amount': 72000.00,
                'due_amount': 4275.90,  # 3 payments overdue
                'no_of_missed_installments': '3',
                'contractual_installment_amount': 1425.30,
                'interest_late_fee': 95.50,
                'minimum_amount': 427.59,
                'acceptable_pay_later_date': date(2024, 3, 1),
                'acceptable_already_paid_date': date(2024, 1, 15),
                'grace_period_date': date(2024, 2, 5),
                'due_date': date(2024, 1, 15),
                'term_months': '72',  # 6 year loan
                'days_past_due': '45',
                'interest_rate': 4.8,
                'maturity_date': date(2027, 1, 15),
                'next_due_date': date(2024, 4, 15),
                'final_amount': 102621.60,
                'new_due_date': date(2024, 3, 1),  # Arranged payment date
                'insurance_status': 'Lapsed',  # Insurance lapsed due to non-payment
                'insurance_expiry_date': date(2024, 1, 31),
                'payoff_effect': 'Collection Required',
                'principal_amount': 72000.00,
                'last_payment_amount': 1425.30,
                'next_due_amount': 4275.90  # All overdue payments
            },
            {
                # Jennifer Martinez - 2020 Toyota Camry, 1 missed payment, 25 days past due
                'customer_id': customers[3].id,
                'product_name': '2020 Toyota Camry',
                'loan_amount': 32000.00,
                'due_amount': 578.75,  # 1 payment overdue
                'no_of_missed_installments': '1',
                'contractual_installment_amount': 578.75,
                'interest_late_fee': 28.50,
                'minimum_amount': 57.88,
                'acceptable_pay_later_date': date(2024, 2, 20),
                'acceptable_already_paid_date': date(2024, 1, 20),
                'grace_period_date': date(2024, 2, 5),
                'due_date': date(2024, 1, 20),
                'term_months': '60',
                'days_past_due': '25',
                'interest_rate': 3.5,
                'maturity_date': date(2025, 1, 20),
                'next_due_date': date(2024, 2, 20),
                'final_amount': 34725.00,
                'new_due_date': date(2024, 2, 20),
                'insurance_status': 'Active',
                'insurance_expiry_date': date(2024, 8, 31),
                'payoff_effect': 'Standard Payoff',
                'principal_amount': 32000.00,
                'last_payment_amount': 578.75,
                'next_due_amount': 607.25  # Payment + late fee
            },
            {
                # James Anderson - 2019 Honda Accord, 2 missed payments, 35 days past due
                'customer_id': customers[4].id,
                'product_name': '2019 Honda Accord',
                'loan_amount': 28500.00,
                'due_amount': 1125.60,  # 2 payments overdue
                'no_of_missed_installments': '2',
                'contractual_installment_amount': 562.80,
                'interest_late_fee': 35.00,
                'minimum_amount': 112.56,
                'acceptable_pay_later_date': date(2024, 2, 25),
                'acceptable_already_paid_date': date(2024, 1, 10),
                'grace_period_date': date(2024, 1, 25),
                'due_date': date(2024, 1, 10),
                'term_months': '60',
                'days_past_due': '35',
                'interest_rate': 4.1,
                'maturity_date': date(2024, 10, 10),  # Almost paid off
                'next_due_date': date(2024, 3, 10),
                'final_amount': 33768.00,
                'new_due_date': date(2024, 2, 25),
                'insurance_status': 'Suspended',  # Suspended due to missed payments
                'insurance_expiry_date': date(2024, 3, 31),
                'payoff_effect': 'Early Payoff Available',
                'principal_amount': 28500.00,
                'last_payment_amount': 562.80,
                'next_due_amount': 1160.60  # Both payments + fees
            }
        ]
        
        # Create loans
        loans = []
        for loan_data in auto_loans_data:
            loan = Loan(**loan_data)
            db.session.add(loan)
            loans.append(loan)
        
        db.session.commit()
        print(f"✅ Created {len(loans)} realistic auto loans")
        
        # Create realistic customer interactions
        interactions_data = [
            {
                # Michael Rodriguez - Last call about Audi Q5 overdue payment
                'customer_id': customers[0].id,
                'call_outcome_note': 'Customer acknowledges 10-day overdue payment on 2023 Audi Q5. Promised to pay by Feb 15th.',
                'contact_type': 'Outbound Call',
                'final_disposition': 'Promise_to_Pay',
                'user_agreed_payment_amount': '1285.50',
                'call_duration': '00:08:45',
                'agent_notes': 'Customer experienced temporary cash flow issue. Employment stable, will pay full amount including late fee.',
                'source': 'Phone Call',
                'status': 'Arranged',
                'creation_date': datetime(2024, 2, 5, 14, 30, 0),
                'last_updated_date': date(2024, 2, 5)
            },
            {
                # Sarah Chen - Courtesy call about BMW X3 current status
                'customer_id': customers[1].id,
                'call_outcome_note': 'Account current. Customer satisfied with BMW X3 and payment schedule.',
                'contact_type': 'Courtesy Call',
                'final_disposition': 'Account_Current',
                'user_agreed_payment_amount': '0.00',
                'call_duration': '00:03:20',
                'agent_notes': 'Customer happy with vehicle and service. No concerns raised.',
                'source': 'Phone Call',
                'status': 'Completed',
                'creation_date': datetime(2024, 1, 25, 10, 15, 0),
                'last_updated_date': date(2024, 1, 25)
            },
            {
                # David Thompson - Collection call about Mercedes C-Class
                'customer_id': customers[2].id,
                'call_outcome_note': 'Customer facing financial hardship. Mercedes C-Class loan 45 days past due. Needs payment arrangement.',
                'contact_type': 'Collection Call',
                'final_disposition': 'Payment_Plan_Requested',
                'user_agreed_payment_amount': '1500.00',
                'call_duration': '00:18:30',
                'agent_notes': 'Customer lost overtime hours at work. Willing to pay $1500 by March 1st, needs modified payment plan.',
                'source': 'Phone Call',
                'status': 'Follow_Up_Required',
                'creation_date': datetime(2024, 2, 3, 16, 45, 0),
                'last_updated_date': date(2024, 2, 3)
            },
            {
                # Jennifer Martinez - Follow-up call about Toyota Camry
                'customer_id': customers[3].id,
                'call_outcome_note': 'Toyota Camry payment 25 days overdue. Customer will pay by end of week.',
                'contact_type': 'Follow_Up_Call',
                'final_disposition': 'Promise_to_Pay',
                'user_agreed_payment_amount': '607.25',
                'call_duration': '00:06:12',
                'agent_notes': 'Customer apologetic about missed payment. Had medical expenses. Will pay full amount including late fee.',
                'source': 'Phone Call',
                'status': 'Arranged',
                'creation_date': datetime(2024, 2, 1, 11, 30, 0),
                'last_updated_date': date(2024, 2, 1)
            },
            {
                # James Anderson - Collection call about Honda Accord
                'customer_id': customers[4].id,
                'call_outcome_note': 'Honda Accord loan 35 days past due. Customer considering early payoff option.',
                'contact_type': 'Collection Call',
                'final_disposition': 'Considering_Payoff',
                'user_agreed_payment_amount': '1160.60',
                'call_duration': '00:12:45',
                'agent_notes': 'Customer interested in early payoff discount. Will call back after reviewing finances. Agreed to current payment to stop late fees.',
                'source': 'Phone Call',
                'status': 'Pending_Decision',
                'creation_date': datetime(2024, 1, 30, 13, 20, 0),
                'last_updated_date': date(2024, 1, 30)
            }
        ]
        
        # Create interactions
        interactions = []
        for interaction_data in interactions_data:
            interaction = CustomerInteraction(**interaction_data)
            db.session.add(interaction)
            interactions.append(interaction)
        
        db.session.commit()
        print(f"✅ Created {len(interactions)} realistic customer interactions")
        
        # Print summary
        print("\n🎯 REALISTIC AUTO LOAN CUSTOMER SUMMARY:")
        print("="*60)
        
        for i, customer in enumerate(customers):
            loan = loans[i]
            interaction = interactions[i]
            
            status = "CURRENT" if loan.days_past_due == '0' else f"{loan.days_past_due} DAYS PAST DUE"
            print(f"📋 {customer.first_name} {customer.last_name}")
            print(f"   🚗 Vehicle: {loan.product_name}")
            print(f"   📞 Phone: {customer.primary_phone_number}")
            print(f"   💰 Due Amount: ${loan.due_amount:,.2f}")
            print(f"   📅 Status: {status}")
            print(f"   🏦 Last Contact: {interaction.final_disposition}")
            print("-" * 40)
        
        print(f"\n✅ Database initialized with {len(customers)} realistic auto loan customers!")
        print("🚀 Ready for API testing!")

if __name__ == "__main__":
    create_realistic_auto_loan_customers()