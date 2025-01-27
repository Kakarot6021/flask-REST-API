import os
import sib_api_v3_sdk
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

# Load the Brevo API Key from environment variables
API_KEY = os.getenv("BREVO_API_KEY")
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = API_KEY

# Instantiate the Brevo API client
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def send_simple_message(to, subject, body):
    # Create the email content
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to}],
        subject=subject,
        html_content=body
    )
    
    try:
        # Send the email via Brevo API
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)  # Print the response to the console (for debugging)
    except sib_api_v3_sdk.ApiException as e:
        print(f"Exception when sending email: {e}")

def send_user_registration_email(email, username):
    body = f"Hi {username}! You have successfully signed up to the Stores REST API."
    return send_simple_message(email, "Successfully signed up", body)
