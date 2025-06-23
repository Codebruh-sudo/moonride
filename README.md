# MONRIDE (Contact Deduplication API)

This is a small project I made to handle contact information (email and phone numbers).  
It checks if a contact already exists and groups related ones together using a primary and secondary contact system.

---

## 🔧 What this does

- You send an email or phone number (or both)
- If the contact is new, it creates it
- If it matches an existing one, it links them
- It returns back all related emails and phone numbers under one main contact.




### PHTOS 
1) https://drive.google.com/file/d/1_NvQjTwS5rq8oZa-Of9WiGbmc1pUKs4t/view?usp=drivesdk ( LINK THAT SHOWS THE CODE IS SUCCESSFULLY DEPLOYED )

2) https://drive.google.com/file/d/1_UHhkZ4egToJKcoSum_sTUfJfVxzUbzD/view?usp=drivesdk. ( RUNNING THE setup.sh that run the whole code ) .
  ### you can check the code is well written with zero amount of error


---

##  API Endpoint

### `POST /identify`

Send this:

```json
{
  "email": "john@example.com",
  "phoneNumber": "1234567890"
}


{
  "contact": {
    "primaryContactId": 1,
    "emails": ["john@example.com"],
    "phoneNumbers": ["1234567890"],
    "secondaryContactIds": []
  }
}






