import http.server
import logging
import requests
import urllib.parse
from django.contrib.auth import get_user_model

from app.models import Contact, SalesOrder, Invoice, CreditNote
from ..serializer import ContactSerializer, ExpensesOrderSerializer, SalesOrderSerializer, InvoiceSerializer, CreditNoteSerializer

User = get_user_model()

class MyHandler(http.server.BaseHTTPRequestHandler):
    client_id = ""
    client_secret = ""
    redirect_uri = ""
    organization_id = ""
    token_url = ""
    apis_to_handle = []
    user = None
    successful_operations = True

    def do_GET(self):
        logging.info("Received GET request at: %s", self.path)
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        code = query_components.get("code", [None])[0]

        if code:
            token_info = self.fetch_token(code)
            if not token_info:
                self.send_error(500, "Failed to fetch token")
                self.server.shutdown()
                return

            headers = {"Authorization": f"Zoho-oauthtoken {token_info.get('access_token')}"}
            for api in self.apis_to_handle:
                try:
                    self.fetch_and_save_data(api['url'], headers, api['name'])
                except Exception as e:
                    logging.error(f"Error handling {api['name']} API: {str(e)}")
                    self.successful_operations = False
                    break
            
            if self.successful_operations:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Authorization and data import completed successfully.")
                self.server.shutdown()
            else:
                self.send_error(500, "Some operations failed. Check logs for details.")
                self.server.shutdown()
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Error: No code provided or invalid request.")
    
    def fetch_token(self, code):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
            "prompt": "consent",
            "access_type": "offline"
        }
        try:
            response = requests.post(self.token_url, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during token retrieval: {str(e)}")
            raise  # Raise the exception to signal failure
    
    def fetch_and_save_data(self, api_url, headers, name):
        try:
            response = requests.get(api_url, headers=headers, params={"organization_id": self.organization_id})
            response.raise_for_status()
            data = response.json().get(name, [])
            print(data)
            for item in data:
                item['user'] = self.user.id
                serializer = self.get_serializer(name, data=item)
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    logging.error(f"Validation error for {name}: {serializer.errors}")
                    self.successful_operations = False

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {name} data: {str(e)}")
            self.successful_operations = False
            raise  # Raise the exception to signal failure

    def get_serializer(self, name, data):
        if name == 'contacts':
            return ContactSerializer(data=data)
        elif name == 'salesorders':
            return SalesOrderSerializer(data=data)
        elif name == 'invoices':
            return InvoiceSerializer(data=data)
        elif name == 'creditnotes':
            return CreditNoteSerializer(data=data)
        elif name == 'expenses':
            return ExpensesOrderSerializer(data=data)
        else:
            logging.error(f"No serializer found for {name}")
            return None
