# CRM API Examples

This document provides comprehensive examples for both GET and POST endpoints in the CRM system.

## 🔍 GET Endpoint: Fetch User Profile Pre-Call

### **Endpoint**: `GET /api/fetch_user_profile_pre_call/`

**Purpose**: Retrieve customer profile, loan details, and latest interaction by phone number.

### **URL Structure**:
```
http://localhost:5000/api/fetch_user_profile_pre_call/?caller_number={phone_number}
```

### **Important Notes**:
- This is a GET request that accepts parameters only via query string
- Any request body or empty headers (like `--header '{}'` or `--data '{}'`) are safely ignored
- The endpoint handles CORS preflight requests automatically

### **Example Curl Commands**:

#### 1. **John Doe** (Current Customer - Auto Loan)
```bash
curl "http://localhost:5000/api/fetch_user_profile_pre_call/?caller_number=5551234567"
```

#### 2. **Sarah Johnson** (Past Due - Payment Arrangement)
```bash
curl "http://localhost:5000/api/fetch_user_profile_pre_call/?caller_number=5552345678"
```

#### 3. **Michael Brown** (Delinquent - Collections)
```bash
curl "http://localhost:5000/api/fetch_user_profile_pre_call/?caller_number=5553456789"
```

#### 4. **Emily Davis** (Current - Dispute Resolved)
```bash
curl "http://localhost:5000/api/fetch_user_profile_pre_call/?caller_number=5554567890"
```

#### 5. **Robert Wilson** (Default - Collections Agency)
```bash
curl "http://localhost:5000/api/fetch_user_profile_pre_call/?caller_number=5555678901"
```

### **Example Response**:
```json
{
  "success": "True",
  "caller_details": [
    {
      "user_info": {
        "account_number": "1234567890",
        "first_name": "John",
        "last_name": "Doe",
        "product_name": "Auto Loan Premium",
        "address_line_1": "123 Main Street",
        "address_line_2": "Apt 4B",
        "zip_code": 10001,
        "city": "New York",
        "state": "NY",
        "ssn": 123456789,
        "dob": "1980-01-15",
        "primary_phone_number": 5551234567,
        "email_address": "john.doe@email.com",
        "due_amount": 1250.0,
        "no_of_missed_installments": 0,
        "contractual_installment_amount": 425.5,
        "interest_late_fee": 25.0,
        "minimum_amount": 50.0,
        "customer_number": 10001,
        "acceptable_pay_later_date": "2024-02-15",
        "acceptable_already_paid_date": "2024-01-31",
        "grace_period_date": "2024-02-10",
        "due_date": "2024-01-31",
        "record_type": "responsible_party",
        "borrower_first_name": "John",
        "borrower_last_name": "Doe",
        "is_eligible_to_call": true,
        "transfer_phone_number": 5551111111,
        "transfer_ip_address": "192.168.1.100"
      },
      "metadata": {
        "creation_date": "2024-02-01T10:00:00",
        "last_updated_date": "2024-02-01",
        "source": "System Generated",
        "status": "Sent",
        "notes": "Payment confirmation email sent to customer."
      }
    }
  ],
  "status": {
    "type": "success",
    "message": "Successful"
  }
}
```

### **Error Examples**:

#### Missing caller_number:
```bash
curl "http://localhost:5000/api/fetch_user_profile_pre_call/"
```
**Response**:
```json
{
  "success": "False",
  "caller_details": [],
  "status": {
    "type": "error",
    "message": "caller_number parameter is required"
  }
}
```

#### Customer not found:
```bash
curl "http://localhost:5000/api/fetch_user_profile_pre_call/?caller_number=9999999999"
```
**Response**:
```json
{
  "success": "False",
  "caller_details": [],
  "status": {
    "type": "error",
    "message": "Customer not found with the provided caller number"
  }
}
```

---

## 📝 POST Endpoint: Post Call Outcomes

### **Endpoint**: `POST /api/post_call_outcomes/`

**Purpose**: Update customer records and create interaction logs based on call outcomes.

### **URL**: 
```
http://localhost:5000/api/post_call_outcomes/
```

### **Example Curl Commands**:

#### 1. **Promise to Pay Scenario**
```bash
curl -X POST "http://localhost:5000/api/post_call_outcomes/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_info": {
      "account_number": "1234567890",
      "first_name": "John",
      "last_name": "Doe",
      "due_amount": 500,
      "acceptable_pay_later_date": "2024-03-15"
    },
    "outcome_details": {
      "user_agreed_payment_amount": "500",
      "pay_later_date": "2024-03-15",
      "contact_type": "Phone",
      "final_disposition": "Promise_to_Pay",
      "disposition_trace": [
        "Connected",
        "Discussed Payment",
        "Promise_to_Pay"
      ],
      "call_duration": "00:08:45",
      "call_identifier": "CALL123456789",
      "call_type": "OUTBOUND",
      "call_end_status": "CUSTOMER HANGUP",
      "dialing_status": {
        "long_code": "Dialed - Answered",
        "short_code": "DAN",
        "details": "Customer answered on second ring"
      }
    },
    "call_outcome_note": "Customer agreed to pay $500 by 3/15. Acknowledged financial hardship but committed to payment.",
    "metadata": {
      "creation_date": "2024-02-01 10:30:00.000-05:00",
      "source": "Outbound Call",
      "status": "Arranged",
      "notes": "Customer responsive and cooperative"
    }
  }'
```

#### 2. **Payment Resolved Scenario**
```bash
curl -X POST "http://localhost:5000/api/post_call_outcomes/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_info": {
      "account_number": "2345678901",
      "due_amount": 0
    },
    "outcome_details": {
      "user_agreed_payment_amount": "875",
      "contact_type": "Phone",
      "final_disposition": "Resolved",
      "disposition_trace": [
        "Connected",
        "Payment Made",
        "Resolved"
      ],
      "call_duration": "00:05:15",
      "call_identifier": "CALL987654321",
      "call_type": "INBOUND",
      "call_end_status": "AGENT HANGUP"
    },
    "call_outcome_note": "Customer made payment during call. Account now current."
  }'
```

#### 3. **No Contact Made**
```bash
curl -X POST "http://localhost:5000/api/post_call_outcomes/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_info": {
      "account_number": "3456789012"
    },
    "outcome_details": {
      "contact_type": "Phone",
      "final_disposition": "No_Answer",
      "call_duration": "00:00:30",
      "call_identifier": "CALL555666777",
      "call_type": "OUTBOUND",
      "call_end_status": "NO ANSWER",
      "dialing_status": {
        "long_code": "Dialed - No Answer",
        "short_code": "DNA",
        "details": "Phone rang but no answer"
      }
    },
    "call_outcome_note": "Attempted contact - no answer. Will retry tomorrow."
  }'
```

#### 4. **Callback Scheduled**
```bash
curl -X POST "http://localhost:5000/api/post_call_outcomes/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_info": {
      "account_number": "4567890123"
    },
    "outcome_details": {
      "contact_type": "Phone",
      "final_disposition": "Callback_Scheduled",
      "disposition_trace": [
        "Connected",
        "Callback_Scheduled"
      ],
      "call_duration": "00:03:20",
      "call_identifier": "CALL888999000",
      "call_type": "OUTBOUND",
      "call_end_status": "CUSTOMER HANGUP"
    },
    "call_outcome_note": "Customer requested callback tomorrow at 2 PM.",
    "metadata": {
      "notes": "Customer prefers afternoon calls"
    }
  }'
```

### **Success Response Example**:
```json
{
  "success": "True",
  "message": "Call outcome processed successfully",
  "updates": {
    "customer_updated": true,
    "loan_updated": true,
    "interaction_created": true,
    "interaction_id": 25
  },
  "status": {
    "type": "success",
    "message": "Call outcome recorded and updates applied"
  }
}
```

### **Error Examples**:

#### Missing account_number:
```bash
curl -X POST "http://localhost:5000/api/post_call_outcomes/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_info": {},
    "outcome_details": {}
  }'
```
**Response**:
```json
{
  "success": "False",
  "message": "account_number is required in user_info",
  "status": {
    "type": "error",
    "message": "Missing required field: account_number"
  }
}
```

#### Customer not found:
```bash
curl -X POST "http://localhost:5000/api/post_call_outcomes/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_info": {
      "account_number": "9999999999"
    },
    "outcome_details": {}
  }'
```
**Response**:
```json
{
  "success": "False",
  "message": "Customer not found with account number: 9999999999",
  "status": {
    "type": "error",
    "message": "Customer not found"
  }
}
```

---

## 📋 Available Test Data

The system includes 5 customers with different scenarios:

| Customer | Phone | Account | Status | Scenario |
|----------|-------|---------|---------|----------|
| John Doe | 5551234567 | 1234567890 | Active | Good customer, current |
| Sarah Johnson | 5552345678 | 2345678901 | Past Due | Payment arrangement |
| Michael Brown | 5553456789 | 3456789012 | Delinquent | Collections activity |
| Emily Davis | 5554567890 | 4567890123 | Current | Dispute resolved |
| Robert Wilson | 5555678901 | 5678901234 | Default | Collections agency |

---

## 🔧 Testing Tips

1. **Start Flask Server**:
   ```bash
   cd /Users/nooruzzaman/fp/crm-auto/backend
   source venv/bin/activate
   python app.py
   ```

2. **Pretty Print JSON Response**:
   ```bash
   curl "http://localhost:5000/api/fetch_user_profile_pre_call/?caller_number=5551234567" | python -m json.tool
   ```

3. **Save Response to File**:
   ```bash
   curl "http://localhost:5000/api/fetch_user_profile_pre_call/?caller_number=5551234567" > response.json
   ```

4. **Check Response Headers**:
   ```bash
   curl -I "http://localhost:5000/api/fetch_user_profile_pre_call/?caller_number=5551234567"
   ```

5. **Verbose Output for Debugging**:
   ```bash
   curl -v "http://localhost:5000/api/fetch_user_profile_pre_call/?caller_number=5551234567"
   ``` 