# MONRIDE (Contact Deduplication API)

This is a small project I made to handle contact information (email and phone numbers).  
It checks if a contact already exists and groups related ones together using a primary and secondary contact system.

---

## 🔧 What this does

- You send an email or phone number (or both)
- If the contact is new, it creates it
- If it matches an existing one, it links them
- It returns back all related emails and phone numbers under one main contact

---

##  API Endpoint

### `POST /identify`

Send this:

```json
{
  "email": "john@example.com",
  "phoneNumber": "1234567890"
}

// the result would be this
{
  "contact": {
    "primaryContactId": 1,
    "emails": ["john@example.com"],
    "phoneNumbers": ["1234567890"],
    "secondaryContactIds": []
  }
}

//If the same person signs up again with different info, it will link them under the same primaryContactId,

//🧑‍💻 Tech Used
//Python

//Flask

//SQLite

//SQLAlchemy


//HOW TO RUN
//pip install -r requirement.txt
//python task.py





