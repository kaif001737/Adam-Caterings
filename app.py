from flask import Flask, jsonify, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# SMTP mail configuration (integrated directly in code as requested)
ADMIN_EMAIL = 'enmettsample@gmail.com'
GMAIL_APP_PASSWORD = 'cxdh phod iykr hsks'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = ADMIN_EMAIL
app.config['MAIL_PASSWORD'] = GMAIL_APP_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = ADMIN_EMAIL
app.config['ADMIN_EMAIL'] = ADMIN_EMAIL

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json() or {}
    name = data.get('name', '')
    phone = data.get('phone', '')
    email = data.get('email', '')
    event_date = data.get('event_date', '')
    message = data.get('message', '')
    service = data.get('service', '')
    catering_type = data.get('catering_type', '')

    if not name or not phone or not email or not service:
        return jsonify({'success': False, 'message': 'Please fill in all required fields.'}), 400

    service_label = {
        'adam-catering': 'Adam Catering',
        'adam-kitchen': 'Adam Kitchen'
    }.get(service, service)
    catering_type_label = catering_type.replace('-', ' ').title() if catering_type else 'Not specified'

    admin_subject = f"New Website Enquiry - {name} ({service_label})"
    admin_body = (
        "A new enquiry has been submitted from the website.\n\n"
        f"Name: {name}\n"
        f"Phone: {phone}\n"
        f"Email: {email}\n"
        f"Service: {service_label}\n"
        f"Catering Type: {catering_type_label}\n"
        f"Event Date: {event_date or 'Not provided'}\n"
        f"Message: {message or 'No additional message'}\n"
    )

    user_subject = "Thank you for contacting Adam Group"
    user_body = (
        f"Dear {name},\n\n"
        "Thank you for contacting Adam Group of Catering & Kitchen.\n"
        "We have received your enquiry and our team will get in touch with you shortly.\n\n"
        "Your enquiry details:\n"
        f"- Service: {service_label}\n"
        f"- Catering Type: {catering_type_label}\n"
        f"- Event Date: {event_date or 'Not provided'}\n\n"
        "Warm regards,\n"
        "Adam Group of Catering & Kitchen\n"
        "Chennai\n"
    )

    try:
        admin_msg = Message(
            subject=admin_subject,
            recipients=[app.config['ADMIN_EMAIL']],
            body=admin_body
        )
        user_msg = Message(
            subject=user_subject,
            recipients=[email],
            body=user_body
        )
        mail.send(admin_msg)
        mail.send(user_msg)
    except Exception:
        return jsonify({
            'success': False,
            'message': 'We could not send your enquiry right now. Please try again shortly.'
        }), 500

    return jsonify({
        'success': True,
        'message': 'Thank you for your enquiry. A confirmation email has been sent, and our team will contact you soon.'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)