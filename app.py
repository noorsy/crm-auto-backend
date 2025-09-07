from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Add request logging
@app.before_request
def log_request_info():
    print(f"🌐 {request.method} {request.url}")
    if request.method in ['POST', 'PUT', 'PATCH']:
        print(f"📦 Content-Type: {request.content_type}")
        if request.is_json:
            print(f"📋 JSON Data: {request.get_json()}")

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///crm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Configure CORS - Simple setup that allows everything
CORS(app)

# Models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(50), unique=True, nullable=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    email_address = db.Column(db.String(120), nullable=True)
    primary_phone_number = db.Column(db.BigInteger, nullable=True)
    ssn = db.Column(db.Integer, nullable=True)
    dob = db.Column(db.Date, nullable=True)
    address_line_1 = db.Column(db.Text, nullable=True)
    address_line_2 = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zip_code = db.Column(db.Integer, nullable=True)
    customer_number = db.Column(db.Integer, nullable=True)
    record_type = db.Column(db.String(50), nullable=True)
    borrower_first_name = db.Column(db.String(100), nullable=True)
    borrower_last_name = db.Column(db.String(100), nullable=True)
    is_eligible_to_call = db.Column(db.Boolean, default=True, nullable=True)
    transfer_phone_number = db.Column(db.BigInteger, nullable=True)
    transfer_ip_address = db.Column(db.String(45), nullable=True)
    
    # Legacy fields for backward compatibility
    credit_score = db.Column(db.Integer, nullable=True)
    monthly_income = db.Column(db.Float, nullable=True)
    employment_status = db.Column(db.String(50), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    
    # Relationships
    loans = db.relationship('Loan', backref='customer', lazy=True)
    notes = db.relationship('CustomerNote', backref='customer', lazy=True)
    interactions = db.relationship('CustomerInteraction', backref='customer', lazy=True)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vin = db.Column(db.String(17), unique=True, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=True)
    color = db.Column(db.String(30), nullable=True)
    condition = db.Column(db.String(20), nullable=True)
    market_value = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    loans = db.relationship('Loan', backref='vehicle', lazy=True)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)  # Made optional
    
    # Loan details from your specification
    product_name = db.Column(db.String(100), nullable=False)
    due_amount = db.Column(db.Float, nullable=False)
    no_of_missed_installments = db.Column(db.Integer, default=0)
    contractual_installment_amount = db.Column(db.Float, nullable=False)
    interest_late_fee = db.Column(db.Float, nullable=False)
    minimum_amount = db.Column(db.Float, nullable=False)
    acceptable_pay_later_date = db.Column(db.Date, nullable=True)
    acceptable_already_paid_date = db.Column(db.Date, nullable=True)
    grace_period_date = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date, nullable=False)
    
    # Legacy fields for backward compatibility
    loan_amount = db.Column(db.Float, nullable=True)
    interest_rate = db.Column(db.Float, nullable=True)
    term_months = db.Column(db.Integer, nullable=True)
    monthly_payment = db.Column(db.Float, nullable=True)
    balance_remaining = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default='active')  # active, paid_off, defaulted, repo
    next_payment_date = db.Column(db.Date, nullable=True)
    origination_date = db.Column(db.Date, nullable=True)
    days_past_due = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    payments = db.relationship('Payment', backref='loan', lazy=True)
    notes = db.relationship('LoanNote', backref='loan', lazy=True)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # cash, check, card, ach
    reference_number = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CustomerNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    note = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LoanNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)
    note = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CustomerInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    last_updated_date = db.Column(db.Date, nullable=False)
    source = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# API Routes

@app.route('/api/customers', methods=['GET', 'POST'])  # type: ignore
def customers():
    if request.method == 'GET':
        customers = Customer.query.all()
        return jsonify([{
            'id': c.id,
            'account_number': c.account_number,
            'first_name': c.first_name,
            'last_name': c.last_name,
            'email_address': c.email_address,
            'primary_phone_number': c.primary_phone_number,
            'customer_number': c.customer_number,
            'record_type': c.record_type,
            'is_eligible_to_call': c.is_eligible_to_call,
            'created_at': c.created_at.isoformat() if c.created_at else None
        } for c in customers])
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # Parse date fields
        dob = None
        if data.get('dob'):
            dob = datetime.strptime(data.get('dob'), '%Y-%m-%d').date()
        
        customer = Customer(  # type: ignore
            account_number=data.get('account_number'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email_address=data.get('email_address'),
            primary_phone_number=data.get('primary_phone_number'),
            ssn=data.get('ssn'),
            dob=dob,
            address_line_1=data.get('address_line_1'),
            address_line_2=data.get('address_line_2'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            customer_number=data.get('customer_number'),
            record_type=data.get('record_type'),
            borrower_first_name=data.get('borrower_first_name'),
            borrower_last_name=data.get('borrower_last_name'),
            is_eligible_to_call=data.get('is_eligible_to_call', True),
            transfer_phone_number=data.get('transfer_phone_number'),
            transfer_ip_address=data.get('transfer_ip_address'),
            # Legacy fields
            credit_score=data.get('credit_score'),
            monthly_income=data.get('monthly_income'),
            employment_status=data.get('employment_status')
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify({'message': 'Customer created successfully', 'id': customer.id}), 201

@app.route('/api/customers/<int:customer_id>', methods=['GET', 'PUT', 'DELETE'])  # type: ignore
def customer_detail(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    if request.method == 'GET':
        return jsonify({
            'id': customer.id,
            'account_number': customer.account_number,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'email_address': customer.email_address,
            'primary_phone_number': customer.primary_phone_number,
            'ssn': customer.ssn,
            'dob': customer.dob.isoformat() if customer.dob else None,
            'address_line_1': customer.address_line_1,
            'address_line_2': customer.address_line_2,
            'city': customer.city,
            'state': customer.state,
            'zip_code': customer.zip_code,
            'customer_number': customer.customer_number,
            'record_type': customer.record_type,
            'borrower_first_name': customer.borrower_first_name,
            'borrower_last_name': customer.borrower_last_name,
            'is_eligible_to_call': customer.is_eligible_to_call,
            'transfer_phone_number': customer.transfer_phone_number,
            'transfer_ip_address': customer.transfer_ip_address,
            'credit_score': customer.credit_score,
            'monthly_income': customer.monthly_income,
            'employment_status': customer.employment_status,
            'created_at': customer.created_at.isoformat() if customer.created_at else None,
            'loans': [{
                'id': loan.id,
                'product_name': loan.product_name,
                'due_amount': loan.due_amount,
                'no_of_missed_installments': loan.no_of_missed_installments,
                'contractual_installment_amount': loan.contractual_installment_amount,
                'interest_late_fee': loan.interest_late_fee,
                'minimum_amount': loan.minimum_amount,
                'due_date': loan.due_date.isoformat() if loan.due_date else None,
                'status': loan.status
            } for loan in customer.loans],
            'interactions': [{
                'id': interaction.id,
                'creation_date': interaction.creation_date.isoformat() if interaction.creation_date else None,
                'last_updated_date': interaction.last_updated_date.isoformat() if interaction.last_updated_date else None,
                'source': interaction.source,
                'status': interaction.status,
                'notes': interaction.notes
            } for interaction in customer.interactions]
        })
    
    elif request.method == 'PUT':
        print(f"🔄 PUT request received for customer ID: {customer_id}")
        print(f"📥 Request headers: {dict(request.headers)}")
        
        data = request.get_json()
        print(f"📋 Request data: {data}")
        print(f"👤 Current customer data: {customer.__dict__}")
        
        if not data:
            print("❌ No JSON data received")
            return jsonify({'error': 'No data provided'}), 400
            
        # Clean up data - convert empty strings to None for date and numeric fields
        if 'dob' in data and data['dob'] == '':
            data['dob'] = None
        if 'ssn' in data and data['ssn'] == '':
            data['ssn'] = None
        if 'zip_code' in data and data['zip_code'] == '':
            data['zip_code'] = None
        if 'customer_number' in data and data['customer_number'] == '':
            data['customer_number'] = None
        if 'transfer_phone_number' in data and data['transfer_phone_number'] == '':
            data['transfer_phone_number'] = None
        if 'credit_score' in data and data['credit_score'] == '':
            data['credit_score'] = None
        if 'monthly_income' in data and data['monthly_income'] == '':
            data['monthly_income'] = None
            
        updated_fields = []
        for key, value in data.items():
            if hasattr(customer, key):
                old_value = getattr(customer, key)
                setattr(customer, key, value)
                updated_fields.append(f"{key}: {old_value} -> {value}")
                print(f"✏️ Updated {key}: {old_value} -> {value}")
            else:
                print(f"⚠️ Field '{key}' not found on customer model")
                
        customer.updated_at = datetime.utcnow()
        print(f"📝 Updated fields: {updated_fields}")
        
        try:
            db.session.commit()
            print(f"✅ Customer {customer_id} updated successfully")
            return jsonify({'message': 'Customer updated successfully'})
        except Exception as e:
            print(f"❌ Database commit failed: {str(e)}")
            db.session.rollback()
            return jsonify({'error': 'Failed to update customer'}), 500
    
    elif request.method == 'DELETE':
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'})

@app.route('/api/loans', methods=['GET', 'POST'])  # type: ignore
def loans():
    if request.method == 'GET':
        loans = Loan.query.all()
        return jsonify([{
            'id': loan.id,
            'customer': f"{loan.customer.first_name} {loan.customer.last_name}",
            'customer_id': loan.customer_id,
            'vehicle': f"{loan.vehicle.year} {loan.vehicle.make} {loan.vehicle.model}" if loan.vehicle else None,
            'product_name': loan.product_name,
            'due_amount': loan.due_amount,
            'no_of_missed_installments': loan.no_of_missed_installments,
            'contractual_installment_amount': loan.contractual_installment_amount,
            'interest_late_fee': loan.interest_late_fee,
            'minimum_amount': loan.minimum_amount,
            'due_date': loan.due_date.isoformat() if loan.due_date else None,
            'acceptable_pay_later_date': loan.acceptable_pay_later_date.isoformat() if loan.acceptable_pay_later_date else None,
            'acceptable_already_paid_date': loan.acceptable_already_paid_date.isoformat() if loan.acceptable_already_paid_date else None,
            'grace_period_date': loan.grace_period_date.isoformat() if loan.grace_period_date else None,
            'status': loan.status
        } for loan in loans])
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # Parse date fields
        due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d').date() if data.get('due_date') else None
        acceptable_pay_later_date = datetime.strptime(data.get('acceptable_pay_later_date'), '%Y-%m-%d').date() if data.get('acceptable_pay_later_date') else None
        acceptable_already_paid_date = datetime.strptime(data.get('acceptable_already_paid_date'), '%Y-%m-%d').date() if data.get('acceptable_already_paid_date') else None
        grace_period_date = datetime.strptime(data.get('grace_period_date'), '%Y-%m-%d').date() if data.get('grace_period_date') else None
        next_payment_date = datetime.strptime(data.get('next_payment_date'), '%Y-%m-%d').date() if data.get('next_payment_date') else None
        origination_date = datetime.strptime(data.get('origination_date'), '%Y-%m-%d').date() if data.get('origination_date') else None
        
        loan = Loan(  # type: ignore
            customer_id=data.get('customer_id'),
            vehicle_id=data.get('vehicle_id'),
            product_name=data.get('product_name'),
            due_amount=data.get('due_amount'),
            no_of_missed_installments=data.get('no_of_missed_installments', 0),
            contractual_installment_amount=data.get('contractual_installment_amount'),
            interest_late_fee=data.get('interest_late_fee'),
            minimum_amount=data.get('minimum_amount'),
            acceptable_pay_later_date=acceptable_pay_later_date,
            acceptable_already_paid_date=acceptable_already_paid_date,
            grace_period_date=grace_period_date,
            due_date=due_date,
            # Legacy fields
            loan_amount=data.get('loan_amount'),
            interest_rate=data.get('interest_rate'),
            term_months=data.get('term_months'),
            monthly_payment=data.get('monthly_payment'),
            balance_remaining=data.get('balance_remaining'),
            next_payment_date=next_payment_date,
            origination_date=origination_date
        )
        db.session.add(loan)
        db.session.commit()
        return jsonify({'message': 'Loan created successfully', 'id': loan.id}), 201

@app.route('/api/loans/<int:loan_id>', methods=['GET', 'PUT', 'DELETE'])  # type: ignore
def loan_detail(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    
    if request.method == 'GET':
        return jsonify({
            'id': loan.id,
            'customer_id': loan.customer_id,
            'customer': f"{loan.customer.first_name} {loan.customer.last_name}",
            'vehicle_id': loan.vehicle_id,
            'vehicle': f"{loan.vehicle.year} {loan.vehicle.make} {loan.vehicle.model}" if loan.vehicle else None,
            'product_name': loan.product_name,
            'due_amount': loan.due_amount,
            'no_of_missed_installments': loan.no_of_missed_installments,
            'contractual_installment_amount': loan.contractual_installment_amount,
            'interest_late_fee': loan.interest_late_fee,
            'minimum_amount': loan.minimum_amount,
            'acceptable_pay_later_date': loan.acceptable_pay_later_date.isoformat() if loan.acceptable_pay_later_date else None,
            'acceptable_already_paid_date': loan.acceptable_already_paid_date.isoformat() if loan.acceptable_already_paid_date else None,
            'grace_period_date': loan.grace_period_date.isoformat() if loan.grace_period_date else None,
            'due_date': loan.due_date.isoformat() if loan.due_date else None,
            'loan_amount': loan.loan_amount,
            'interest_rate': loan.interest_rate,
            'term_months': loan.term_months,
            'monthly_payment': loan.monthly_payment,
            'balance_remaining': loan.balance_remaining,
            'status': loan.status,
            'next_payment_date': loan.next_payment_date.isoformat() if loan.next_payment_date else None,
            'origination_date': loan.origination_date.isoformat() if loan.origination_date else None,
            'days_past_due': loan.days_past_due,
            'created_at': loan.created_at.isoformat() if loan.created_at else None
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        # Parse date fields
        if data.get('due_date'):
            loan.due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d').date()
        if data.get('acceptable_pay_later_date'):
            loan.acceptable_pay_later_date = datetime.strptime(data.get('acceptable_pay_later_date'), '%Y-%m-%d').date()
        if data.get('acceptable_already_paid_date'):
            loan.acceptable_already_paid_date = datetime.strptime(data.get('acceptable_already_paid_date'), '%Y-%m-%d').date()
        if data.get('grace_period_date'):
            loan.grace_period_date = datetime.strptime(data.get('grace_period_date'), '%Y-%m-%d').date()
        if data.get('next_payment_date'):
            loan.next_payment_date = datetime.strptime(data.get('next_payment_date'), '%Y-%m-%d').date()
        if data.get('origination_date'):
            loan.origination_date = datetime.strptime(data.get('origination_date'), '%Y-%m-%d').date()
        
        # Update other fields
        for key, value in data.items():
            if hasattr(loan, key) and key not in ['due_date', 'acceptable_pay_later_date', 'acceptable_already_paid_date', 'grace_period_date', 'next_payment_date', 'origination_date']:
                setattr(loan, key, value)
        
        loan.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'Loan updated successfully'})
    
    elif request.method == 'DELETE':
        db.session.delete(loan)
        db.session.commit()
        return jsonify({'message': 'Loan deleted successfully'})

@app.route('/api/fetch_user_profile_pre_call/', methods=['GET', 'OPTIONS'])
def fetch_user_profile_pre_call():
    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
        return response
    
    # Ensure this is a GET request and ignore any body data
    if request.method != 'GET':
        return jsonify({
            "success": "False",
            "caller_details": [],
            "status": {
                "type": "error",
                "message": "Only GET method is allowed for this endpoint"
            }
        }), 405
    
    # Log request details for debugging (ignore any body content for GET)
    print(f"GET request to fetch_user_profile_pre_call with args: {request.args.to_dict()}")
    
    # IMPORTANT: This endpoint completely ignores any request body data (including '{}')
    # Flask automatically ignores body for GET requests, ensuring success response
    # Get caller_number from query parameters only (ignore any body data)
    caller_number = request.args.get('caller_number')
    
    if not caller_number:
        return jsonify({
            "success": "False",
            "caller_details": [],
            "status": {
                "type": "error",
                "message": "caller_number parameter is required in query string"
            }
        }), 400
    
    # Convert caller_number to integer for database query
    try:
        caller_number_int = int(caller_number)
    except ValueError:
        return jsonify({
            "success": "False",
            "caller_details": [],
            "status": {
                "type": "error",
                "message": "Invalid caller_number format"
            }
        }), 400
    
    # Find customer by primary phone number
    customer = Customer.query.filter_by(primary_phone_number=caller_number_int).first()
    
    if not customer:
        return jsonify({
            "success": "False",
            "caller_details": [],
            "status": {
                "type": "error",
                "message": "Customer not found with the provided caller number"
            }
        }), 404
    
    # Get the most recent loan for the customer
    loan = Loan.query.filter_by(customer_id=customer.id).order_by(Loan.created_at.desc()).first()
    
    # Get the most recent interaction for the customer
    interaction = CustomerInteraction.query.filter_by(customer_id=customer.id).order_by(CustomerInteraction.created_at.desc()).first()
    
    # Build the response
    caller_details = {
        "user_info": {
            "account_number": customer.account_number,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "product_name": loan.product_name if loan else None,
            "address_line_1": customer.address_line_1,
            "address_line_2": customer.address_line_2,
            "zip_code": customer.zip_code,
            "city": customer.city,
            "state": customer.state,
            "ssn": customer.ssn,
            "dob": customer.dob.isoformat() if customer.dob else None,
            "primary_phone_number": customer.primary_phone_number,
            "email_address": customer.email_address,
            "due_amount": loan.due_amount if loan else None,
            "no_of_missed_installments": loan.no_of_missed_installments if loan else None,
            "contractual_installment_amount": loan.contractual_installment_amount if loan else None,
            "interest_late_fee": loan.interest_late_fee if loan else None,
            "minimum_amount": loan.minimum_amount if loan else None,
            "customer_number": customer.customer_number,
            "acceptable_pay_later_date": loan.acceptable_pay_later_date.isoformat() if loan and loan.acceptable_pay_later_date else None,
            "acceptable_already_paid_date": loan.acceptable_already_paid_date.isoformat() if loan and loan.acceptable_already_paid_date else None,
            "grace_period_date": loan.grace_period_date.isoformat() if loan and loan.grace_period_date else None,
            "due_date": loan.due_date.isoformat() if loan and loan.due_date else None,
            "record_type": customer.record_type,
            "borrower_first_name": customer.borrower_first_name,
            "borrower_last_name": customer.borrower_last_name,
            "is_eligible_to_call": customer.is_eligible_to_call,
            "transfer_phone_number": customer.transfer_phone_number,
            "transfer_ip_address": customer.transfer_ip_address
        },
        "metadata": {
            "creation_date": interaction.creation_date.isoformat() if interaction and interaction.creation_date else None,
            "last_updated_date": interaction.last_updated_date.isoformat() if interaction and interaction.last_updated_date else None,
            "source": interaction.source if interaction else None,
            "status": interaction.status if interaction else None,
            "notes": interaction.notes if interaction else None
        }
    }
    
    return jsonify({
        "success": "True",
        "caller_details": [caller_details],
        "status": {
            "type": "success",
            "message": "Successful"
        }
    })

@app.route('/api/customers/<int:customer_id>/interactions', methods=['GET', 'POST'])  # type: ignore
def customer_interactions(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    if request.method == 'GET':
        interactions = CustomerInteraction.query.filter_by(customer_id=customer_id).all()
        return jsonify([{
            'id': interaction.id,
            'customer_id': interaction.customer_id,
            'creation_date': interaction.creation_date.isoformat() if interaction.creation_date else None,
            'last_updated_date': interaction.last_updated_date.isoformat() if interaction.last_updated_date else None,
            'source': interaction.source,
            'status': interaction.status,
            'notes': interaction.notes,
            'created_at': interaction.created_at.isoformat() if interaction.created_at else None
        } for interaction in interactions])
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # Parse date fields
        creation_date = datetime.strptime(data.get('creation_date'), '%Y-%m-%d %H:%M:%S.%f%z') if data.get('creation_date') else datetime.utcnow()
        last_updated_date = datetime.strptime(data.get('last_updated_date'), '%Y-%m-%d').date() if data.get('last_updated_date') else datetime.utcnow().date()
        
        interaction = CustomerInteraction(  # type: ignore
            customer_id=customer_id,
            creation_date=creation_date,
            last_updated_date=last_updated_date,
            source=data.get('source'),
            status=data.get('status'),
            notes=data.get('notes')
        )
        db.session.add(interaction)
        db.session.commit()
        return jsonify({'message': 'Customer interaction created successfully', 'id': interaction.id}), 201

@app.route('/api/customers/<int:customer_id>/interactions/<int:interaction_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_customer_interaction(customer_id, interaction_id):
    """Manage individual customer interactions - get, update, or delete"""
    customer = Customer.query.get_or_404(customer_id)
    interaction = CustomerInteraction.query.filter_by(
        id=interaction_id, 
        customer_id=customer_id
    ).first_or_404()
    
    if request.method == 'GET':
        return jsonify({
            'id': interaction.id,
            'customer_id': interaction.customer_id,
            'creation_date': interaction.creation_date.isoformat() if interaction.creation_date else None,
            'last_updated_date': interaction.last_updated_date.isoformat() if interaction.last_updated_date else None,
            'source': interaction.source,
            'status': interaction.status,
            'notes': interaction.notes,
            'created_at': interaction.created_at.isoformat() if interaction.created_at else None,
            'updated_at': interaction.updated_at.isoformat() if interaction.updated_at else None
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        # Update fields if provided
        if 'source' in data:
            interaction.source = data['source']
        if 'status' in data:
            interaction.status = data['status']
        if 'notes' in data:
            interaction.notes = data['notes']
        
        # Parse date fields if provided
        if data.get('creation_date'):
            try:
                interaction.creation_date = datetime.strptime(data['creation_date'], '%Y-%m-%d %H:%M:%S.%f%z')
            except ValueError:
                try:
                    interaction.creation_date = datetime.strptime(data['creation_date'], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    pass
        
        if data.get('last_updated_date'):
            try:
                interaction.last_updated_date = datetime.strptime(data['last_updated_date'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        interaction.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Customer interaction updated successfully',
            'interaction': {
                'id': interaction.id,
                'customer_id': interaction.customer_id,
                'creation_date': interaction.creation_date.isoformat() if interaction.creation_date else None,
                'last_updated_date': interaction.last_updated_date.isoformat() if interaction.last_updated_date else None,
                'source': interaction.source,
                'status': interaction.status,
                'notes': interaction.notes,
                'created_at': interaction.created_at.isoformat() if interaction.created_at else None,
                'updated_at': interaction.updated_at.isoformat() if interaction.updated_at else None
            }
        })
    
    elif request.method == 'DELETE':
        db.session.delete(interaction)
        db.session.commit()
        return jsonify({
            'message': 'Customer interaction deleted successfully',
            'deleted_interaction_id': interaction_id
        }), 200

@app.route('/api/post_call_outcomes/', methods=['POST'])
def post_call_outcomes():
    """
    Update customer records and create interaction logs based on call outcomes.
    This endpoint handles comprehensive updates to customer, loan, and interaction data.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": "False",
                "message": "No data provided",
                "status": {
                    "type": "error",
                    "message": "Request body is required"
                }
            }), 400
        
        # Extract sections from payload
        user_info = data.get('user_info', {})
        outcome_details = data.get('outcome_details', {})
        metadata = data.get('metadata', {})
        call_outcome_note = data.get('call_outcome_note', '')
        
        # Validate required fields
        account_number = user_info.get('account_number')
        if not account_number:
            return jsonify({
                "success": "False",
                "message": "account_number is required in user_info",
                "status": {
                    "type": "error",
                    "message": "Missing required field: account_number"
                }
            }), 400
        
        # Find customer by account number
        customer = Customer.query.filter_by(account_number=account_number).first()
        if not customer:
            return jsonify({
                "success": "False",
                "message": f"Customer not found with account number: {account_number}",
                "status": {
                    "type": "error",
                    "message": "Customer not found"
                }
            }), 404
        
        # Update customer information if provided
        customer_updated = False
        for field, value in user_info.items():
            if hasattr(customer, field) and value is not None:
                # Handle date fields specially
                if field == 'dob' and isinstance(value, str):
                    try:
                        value = datetime.strptime(value, '%Y-%m-%d').date()
                    except ValueError:
                        continue
                
                current_value = getattr(customer, field)
                if current_value != value:
                    setattr(customer, field, value)
                    customer_updated = True
        
        if customer_updated:
            customer.updated_at = datetime.utcnow()
        
        # Find and update loan information
        loan = Loan.query.filter_by(customer_id=customer.id).order_by(Loan.created_at.desc()).first()
        loan_updated = False
        
        if loan:
            # Update loan fields from user_info
            loan_fields = ['product_name', 'due_amount', 'no_of_missed_installments', 
                          'contractual_installment_amount', 'interest_late_fee', 'minimum_amount']
            
            for field in loan_fields:
                if field in user_info and user_info[field] is not None:
                    current_value = getattr(loan, field)
                    new_value = user_info[field]
                    if current_value != new_value:
                        setattr(loan, field, new_value)
                        loan_updated = True
            
            # Update date fields
            date_fields = ['acceptable_pay_later_date', 'acceptable_already_paid_date', 
                          'grace_period_date', 'due_date']
            
            for field in date_fields:
                if field in user_info and user_info[field]:
                    try:
                        new_date = datetime.strptime(user_info[field], '%Y-%m-%d').date()
                        current_date = getattr(loan, field)
                        if current_date != new_date:
                            setattr(loan, field, new_date)
                            loan_updated = True
                    except ValueError:
                        continue
            
            # Handle outcome-specific updates
            if outcome_details.get('user_agreed_payment_amount'):
                try:
                    agreed_amount = float(outcome_details['user_agreed_payment_amount'])
                    # Update due amount based on agreement
                    if loan.due_amount != agreed_amount:
                        loan.due_amount = agreed_amount
                        loan_updated = True
                except ValueError:
                    pass
            
            if outcome_details.get('pay_later_date'):
                try:
                    pay_later_date = datetime.strptime(outcome_details['pay_later_date'], '%Y-%m-%d').date()
                    if loan.acceptable_pay_later_date != pay_later_date:
                        loan.acceptable_pay_later_date = pay_later_date
                        loan_updated = True
                except ValueError:
                    pass
            
            # Update loan status based on disposition
            final_disposition = outcome_details.get('final_disposition', '').lower()
            if final_disposition in ['resolved', 'paid', 'current']:
                if loan.status != 'current':
                    loan.status = 'current'
                    loan.no_of_missed_installments = 0
                    loan.due_amount = 0.0
                    loan_updated = True
            elif final_disposition in ['promise_to_pay', 'callback_scheduled']:
                if loan.status != 'arranged':
                    loan.status = 'arranged'
                    loan_updated = True
            
            if loan_updated:
                loan.updated_at = datetime.utcnow()
        
        # Create comprehensive interaction record
        interaction_data = {
            'customer_id': customer.id,
            'creation_date': datetime.utcnow(),
            'last_updated_date': datetime.utcnow().date(),
            'source': outcome_details.get('contact_type', 'Phone Call'),
            'status': outcome_details.get('final_disposition', 'Completed'),
            'notes': ''
        }
        
        # Parse creation date if provided in metadata
        if metadata.get('creation_date'):
            try:
                interaction_data['creation_date'] = datetime.strptime(
                    metadata['creation_date'], '%Y-%m-%d %H:%M:%S.%f%z'
                )
            except ValueError:
                try:
                    interaction_data['creation_date'] = datetime.strptime(
                        metadata['creation_date'], '%Y-%m-%d %H:%M:%S.%f-%H:%M'
                    )
                except ValueError:
                    pass
        
        # Build comprehensive notes
        notes_parts = []
        
        # Call details
        if outcome_details.get('call_type'):
            notes_parts.append(f"Call Type: {outcome_details['call_type']}")
        
        if outcome_details.get('call_duration'):
            notes_parts.append(f"Duration: {outcome_details['call_duration']}")
        
        if outcome_details.get('call_identifier'):
            notes_parts.append(f"Call ID: {outcome_details['call_identifier']}")
        
        # Disposition trace
        if outcome_details.get('disposition_trace'):
            trace = ' → '.join(outcome_details['disposition_trace'])
            notes_parts.append(f"Disposition Trace: {trace}")
        
        # Payment details
        if outcome_details.get('user_agreed_payment_amount'):
            notes_parts.append(f"Agreed Payment Amount: ${outcome_details['user_agreed_payment_amount']}")
        
        if outcome_details.get('pay_later_date'):
            notes_parts.append(f"Payment Date Agreed: {outcome_details['pay_later_date']}")
        
        # Call end details
        if outcome_details.get('call_end_status'):
            notes_parts.append(f"Call End: {outcome_details['call_end_status']}")
        
        # Dialing status
        if outcome_details.get('dialing_status'):
            dialing = outcome_details['dialing_status']
            dialing_info = f"{dialing.get('long_code', '')} ({dialing.get('short_code', '')})"
            if dialing.get('details'):
                dialing_info += f" - {dialing['details']}"
            notes_parts.append(f"Dialing Status: {dialing_info}")
        
        # Add call outcome note
        if call_outcome_note:
            notes_parts.append(f"Outcome Note: {call_outcome_note}")
        
        # Add metadata notes
        if metadata.get('notes'):
            notes_parts.append(f"Additional Notes: {metadata['notes']}")
        
        interaction_data['notes'] = '; '.join(notes_parts)
        
        # Create the interaction record
        interaction = CustomerInteraction(**interaction_data)
        db.session.add(interaction)
        
        # Commit all changes
        db.session.commit()
        
        # Prepare response
        response = {
            "success": "True",
            "message": "Call outcome processed successfully",
            "updates": {
                "customer_updated": customer_updated,
                "loan_updated": loan_updated,
                "interaction_created": True,
                "interaction_id": interaction.id
            },
            "status": {
                "type": "success",
                "message": "Call outcome recorded and updates applied"
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        # Rollback any changes in case of error
        db.session.rollback()
        
        return jsonify({
            "success": "False",
            "message": f"Internal server error: {str(e)}",
            "status": {
                "type": "error",
                "message": "Failed to process call outcome"
            }
        }), 500

@app.route('/api/dashboard-stats', methods=['GET'])
def dashboard_stats():
    total_customers = Customer.query.count()
    total_loans = Loan.query.count()
    active_loans = Loan.query.filter_by(status='active').count()
    past_due_loans = Loan.query.filter(Loan.days_past_due > 0).count()
    
    total_portfolio = db.session.query(db.func.sum(Loan.balance_remaining)).scalar() or 0
    
    return jsonify({
        'total_customers': total_customers,
        'total_loans': total_loans,
        'active_loans': active_loans,
        'past_due_loans': past_due_loans,
        'total_portfolio': float(total_portfolio)
    })

# Health check and status endpoints
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Replit and monitoring"""
    try:
        # Test database connection
        customer_count = Customer.query.count()
        
        return jsonify({
            'status': 'healthy',
            'message': 'CRM Auto Backend API is running',
            'database': 'connected',
            'customers': customer_count,
            'timestamp': datetime.utcnow().isoformat(),
            'environment': 'replit' if os.getenv('REPL_SLUG') else 'local'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': f'Database connection failed: {str(e)}',
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/health', methods=['GET'])
def api_health():
    """API health check with more detailed information"""
    try:
        # Comprehensive health check
        customer_count = Customer.query.count()
        loan_count = Loan.query.count()
        interaction_count = CustomerInteraction.query.count()
        
        # Check if sample data exists
        has_sample_data = customer_count >= 5
        
        return jsonify({
            'status': 'healthy',
            'api_version': '1.0.0',
            'database': {
                'status': 'connected',
                'customers': customer_count,
                'loans': loan_count,
                'interactions': interaction_count,
                'has_sample_data': has_sample_data
            },
            'endpoints': {
                'customers': '/api/customers',
                'loans': '/api/loans',
                'pre_call': '/api/fetch_user_profile_pre_call/',
                'post_call': '/api/post_call_outcomes/'
            },
            'environment': {
                'platform': 'replit' if os.getenv('REPL_SLUG') else 'local',
                'repl_slug': os.getenv('REPL_SLUG'),
                'repl_owner': os.getenv('REPL_OWNER')
            },
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'CRM Auto Backend API',
        'description': 'Customer Relationship Management system for loan collection',
        'version': '1.0.0',
        'health_check': '/health',
        'api_health': '/api/health',
        'deploy_webhook': '/deploy',
        'documentation': {
            'customers': 'GET /api/customers',
            'loans': 'GET /api/loans',
            'pre_call_profile': 'GET /api/fetch_user_profile_pre_call/?caller_number=<number>',
            'post_call_outcomes': 'POST /api/post_call_outcomes/'
        },
        'sample_data': 'Database automatically initialized with 5 customers, loans, and interactions',
        'replit_url': f"https://{os.getenv('REPL_SLUG')}.{os.getenv('REPL_OWNER', 'your-username')}.repl.co" if os.getenv('REPL_SLUG') else None
    })

@app.route('/deploy', methods=['POST'])
def deploy_webhook():
    """GitHub webhook for auto-deployment"""
    import subprocess
    
    try:
        # Get the current working directory
        current_dir = os.getcwd()
        
        # Pull latest code from GitHub
        result = subprocess.run(
            ['git', 'pull', 'origin', 'main'], 
            cwd=current_dir,
            capture_output=True, 
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return jsonify({
                'status': 'success',
                'message': 'Deployment successful! Replit will restart automatically.',
                'output': result.stdout,
                'timestamp': datetime.utcnow().isoformat()
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Git pull failed',
                'error': result.stderr,
                'output': result.stdout,
                'timestamp': datetime.utcnow().isoformat()
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'status': 'error',
            'message': 'Git pull timed out',
            'timestamp': datetime.utcnow().isoformat()
        }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Deployment failed: {str(e)}',
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/deploy', methods=['GET'])
def deploy_info():
    """Information about the deployment webhook"""
    return jsonify({
        'message': 'GitHub Deployment Webhook',
        'description': 'POST to this endpoint to trigger auto-deployment from GitHub',
        'usage': {
            'method': 'POST',
            'url': '/deploy',
            'trigger': 'GitHub webhook on push to main branch'
        },
        'setup_instructions': 'See REPLIT_SETUP_GUIDE.md for webhook configuration',
        'manual_alternative': 'Run "git pull origin main" in Replit shell',
        'status': 'Ready for webhooks'
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001) 