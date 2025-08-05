import time
import logging
import sys
from datetime import datetime
from colorama import init, Fore, Style
from config import Config
from gmail_client import GmailClient
from ai_responder import AIResponder

# Initialize colorama for colored output
init()

class EmailAISystem:
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Validate configuration
        try:
            Config.validate()
        except ValueError as e:
            self.logger.error(f"Configuration error: {e}")
            sys.exit(1)
        
        # Initialize components
        try:
            self.gmail_client = GmailClient()
            self.ai_responder = AIResponder()
            self.logger.info("Email AI System initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize system: {e}")
            sys.exit(1)
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('email_ai.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def process_emails(self):
        """Process unread emails and generate responses"""
        self.logger.info("Checking for unread emails...")
        
        # Get unread emails
        emails = self.gmail_client.get_unread_emails()
        
        if not emails:
            self.logger.info("No unread emails found")
            return
        
        print(f"\n{Fore.CYAN}Found {len(emails)} unread email(s){Style.RESET_ALL}")
        
        for email_data in emails:
            try:
                self.process_single_email(email_data)
            except Exception as e:
                self.logger.error(f"Error processing email {email_data['id']}: {e}")
    
    def process_single_email(self, email_data):
        """Process a single email"""
        sender = email_data['sender']
        subject = email_data['subject']
        
        print(f"\n{Fore.YELLOW}Processing email:{Style.RESET_ALL}")
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        
        # Check if we should respond to this email
        if not self.ai_responder.should_respond(email_data):
            print(f"{Fore.RED}Skipping automated/invalid email{Style.RESET_ALL}")
            self.gmail_client.mark_as_read(email_data['id'])
            return
        
        # Analyze sentiment
        sentiment = self.ai_responder.analyze_email_sentiment(email_data)
        print(f"Sentiment: {sentiment}")
        
        # Generate AI response
        print(f"{Fore.BLUE}Generating AI response...{Style.RESET_ALL}")
        response = self.ai_responder.generate_response(email_data)
        
        if response:
            print(f"\n{Fore.GREEN}Generated Response:{Style.RESET_ALL}")
            print("-" * 50)
            print(response)
            print("-" * 50)
            
            # Ask user for confirmation
            while True:
                choice = input(f"\n{Fore.CYAN}Send this response? (y/n/e/s): {Style.RESET_ALL}").lower().strip()
                
                if choice == 'y':
                    # Send the response
                    success = self.send_response(email_data, response)
                    if success:
                        self.gmail_client.mark_as_read(email_data['id'])
                    break
                elif choice == 'n':
                    print(f"{Fore.RED}Response not sent{Style.RESET_ALL}")
                    self.gmail_client.mark_as_read(email_data['id'])
                    break
                elif choice == 'e':
                    # Edit response
                    print("Enter your custom response (press Ctrl+D when done):")
                    try:
                        lines = []
                        while True:
                            line = input()
                            lines.append(line)
                    except EOFError:
                        response = '\n'.join(lines)
                        continue
                elif choice == 's':
                    print(f"{Fore.YELLOW}Email skipped{Style.RESET_ALL}")
                    break
                else:
                    print("Please enter 'y' (yes), 'n' (no), 'e' (edit), or 's' (skip)")
        else:
            print(f"{Fore.RED}Failed to generate response{Style.RESET_ALL}")
            self.gmail_client.mark_as_read(email_data['id'])
    
    def send_response(self, email_data, response):
        """Send the AI-generated response"""
        # Extract sender email from the 'From' field
        sender_email = self.extract_email_address(email_data['sender'])
        
        if sender_email:
            success = self.gmail_client.send_email(
                to_email=sender_email,
                subject=email_data['subject'],
                body=response,
                in_reply_to=email_data['id']
            )
            
            if success:
                print(f"{Fore.GREEN}Response sent successfully!{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}Failed to send response{Style.RESET_ALL}")
                return False
        else:
            print(f"{Fore.RED}Could not extract sender email address{Style.RESET_ALL}")
            return False
    
    def extract_email_address(self, from_field):
        """Extract email address from 'From' field"""
        import re
        
        # Pattern to match email addresses
        email_pattern = r'<([^>]+)>|([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        
        match = re.search(email_pattern, from_field)
        if match:
            return match.group(1) or match.group(2)
        return None
    
    def run_continuous(self):
        """Run the system continuously"""
        print(f"{Fore.GREEN}Email AI Response System Started{Style.RESET_ALL}")
        print(f"Monitoring: {Config.GMAIL_ADDRESS}")
        print(f"Check interval: {Config.CHECK_INTERVAL} seconds")
        print(f"Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.process_emails()
                
                print(f"\n{Fore.CYAN}Waiting {Config.CHECK_INTERVAL} seconds until next check...{Style.RESET_ALL}")
                time.sleep(Config.CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}System stopped by user{Style.RESET_ALL}")
            self.logger.info("Email AI system stopped by user")

def main():
    """Main function"""
    print(f"{Fore.BLUE}{'='*60}")
    print(f"    EMAIL AI RESPONSE SYSTEM")
    print(f"    Powered by Google Gemini 2.0 Flash")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    try:
        system = EmailAISystem()
        system.run_continuous()
    except Exception as e:
        print(f"{Fore.RED}System error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
