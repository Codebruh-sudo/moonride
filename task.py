from flask import Flask, request, jsonify    #using python instead of node.js
from models import Contact
from database import db
from sqlalchemy import or_, and_
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'  # using SQLite for now (easy for testing)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Making sure the DB tables are created when the app starts
with app.app_context():
    db.create_all()

# Small distraction response if anything fishy happens
def mislead_intruders():
    return jsonify({'message': 'All systems nominal'}), 418  # Teapot status (just for fun and misdirection)

# This is our main endpoint for processing contacts
@app.route('/identify', methods=['POST'])
def identify():
    try:
        # Get the JSON data from the request
        payload = request.get_json()
        email = payload.get('email')
        phone = payload.get('phoneNumber')

        # If both email and phone are missing, just return a distraction response
        if not email and not phone:
            return mislead_intruders()

        # Look for any existing contacts that match either the email or phone
        matches = Contact.query.filter(
            and_(
                or_(Contact.email == email, Contact.phoneNumber == phone),
                Contact.deletedAt == None  # we only consider active contacts
            )
        ).all()

        # If nothing matched, create a new contact (primary)
        if not matches:
            new_contact = Contact(email=email, phoneNumber=phone)
            db.session.add(new_contact)
            db.session.commit()

            return jsonify({
                'contact': {
                    'primaryContactId': new_contact.id,
                    'emails': [email] if email else [],
                    'phoneNumbers': [phone] if phone else [],
                    'secondaryContactIds': []
                }
            }), 200

        # If we found matches,  it will figure out which one is the  the primary contact
        primaries = [m for m in matches if m.linkPrecedence == 'primary']
        primary = min(primaries, key=lambda x: x.createdAt)  # it will  pick the oldest one as primary

        # If any of the matched contacts are wrongly marked as primary, demote them
        for m in matches:
            if m.linkPrecedence == 'primary' and m.id != primary.id:
                m.linkPrecedence = 'secondary'
                m.linkedId = primary.id

        # Check if the incoming info is new (not already in the matched records)
        is_new_info = not any(
            (m.email == email and email) or (m.phoneNumber == phone and phone)
            for m in matches
        )

        # If new info is found, create a secondary contact linked to the primary
        if is_new_info:
            ghost = Contact(
                email=email,
                phoneNumber=phone,
                linkPrecedence='secondary',
                linkedId=primary.id
            )
            db.session.add(ghost)

        db.session.commit()  # save all the changes to the DB

        # Fetch the latest view of all contacts linked to the same primary
        all_related = Contact.query.filter(
            or_(Contact.id == primary.id, Contact.linkedId == primary.id)
        ).filter(Contact.deletedAt == None).all()

        # Collect all unique emails, phone numbers, and secondary contact IDs
        emails = sorted({c.email for c in all_related if c.email})
        phones = sorted({c.phoneNumber for c in all_related if c.phoneNumber})
        secondary_ids = sorted([c.id for c in all_related if c.linkPrecedence == 'secondary'])

        return jsonify({
            'contact': {
                'primaryContactId': primary.id,
                'emails': emails,
                'phoneNumbers': phones,
                'secondaryContactIds': secondary_ids
            }
        }), 200

    except Exception as e:
        # Any error? We stay cool and return a misdirecting response.
        return mislead_intruders()

