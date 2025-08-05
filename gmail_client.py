import os
import json
import base64
import email
from typing import List, Dict, Optional
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

class GmailClient:
    def __init__(self):
        self.service = None
        self.logger = logging.getLogger(__name__)
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        # Load existing token
        if os.path.exists(Config.TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(Config.TOKEN_FILE, Config.SCOPES)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(Config.CREDENTIALS_FILE):
                    raise FileNotFoundError(f"Credentials file not found: {Config.CREDENTIALS_FILE}")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    Config.CREDENTIALS_FILE, Config.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next time
            with open(Config.TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)
        self.logger.info("Gmail authentication successful")
    
    def get_unread_emails(self, max_results: int = None) -> List[Dict]:
        """Get unread emails"""
        try:
            max_results = max_results or Config.MAX_EMAILS_PER_CHECK
            
            # Search for unread emails
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                email_data = self._get_email_details(message['id'])
                if email_data:
                    emails.append(email_data)
            
            self.logger.info(f"Found {len(emails)} unread emails")
            return emails
            
        except HttpError as error:
            self.logger.error(f"An error occurred while fetching emails: {error}")
            return []
    
    def _get_email_details(self, message_id: str) -> Optional[Dict]:
        """Get detailed information about an email"""
        try:
            message = self.service.users().messages().get(
                userId='me', 
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload'].get('headers', [])
            
            # Extract email metadata
            email_data = {
                'id': message_id,
                'thread_id': message.get('threadId'),
                'subject': '',
                'sender': '',
                'date': '',
                'body': ''
            }
            
            # Parse headers
            for header in headers:
                name = header['name'].lower()
                if name == 'subject':
                    email_data['subject'] = header['value']
                elif name == 'from':
                    email_data['sender'] = header['value']
                elif name == 'date':
                    email_data['date'] = header['value']
            
            # Extract email body
            email_data['body'] = self._extract_email_body(message['payload'])
            
            return email_data
            
        except HttpError as error:
            self.logger.error(f"An error occurred while fetching email details: {error}")
            return None
    
    def _extract_email_body(self, payload) -> str:
        """Extract text body from email payload"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
        else:
            if payload['mimeType'] == 'text/plain':
                data = payload['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')
        
        return body
    
    def send_email(self, to_email: str, subject: str, body: str, in_reply_to: str = None) -> bool:
        """Send an email"""
        try:
            message = MIMEText(body)
            message['to'] = to_email
            message['from'] = Config.GMAIL_ADDRESS
            message['subject'] = f"Re: {subject}" if not subject.startswith('Re:') else subject
            
            if in_reply_to:
                message['In-Reply-To'] = in_reply_to
                message['References'] = in_reply_to
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            send_message = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            self.logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except HttpError as error:
            self.logger.error(f"An error occurred while sending email: {error}")
            return False
    
    def mark_as_read(self, message_id: str) -> bool:
        """Mark an email as read"""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            
            self.logger.info(f"Email {message_id} marked as read")
            return True
            
        except HttpError as error:
            self.logger.error(f"An error occurred while marking email as read: {error}")
            return False