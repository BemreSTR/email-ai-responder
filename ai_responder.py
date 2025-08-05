import google.generativeai as genai
import logging
from typing import Dict, Optional
from config import Config

class AIResponder:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._configure_gemini()
        
    def _configure_gemini(self):
        """Configure Gemini AI"""
        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            self.logger.info("Gemini AI configured successfully")
        except Exception as e:
            self.logger.error(f"Failed to configure Gemini AI: {e}")
            raise
    
    def generate_response(self, email_data: Dict) -> Optional[str]:
        """Generate AI response for an email"""
        try:
            # Create a detailed prompt for the AI
            prompt = self._create_prompt(email_data)
            
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            
            if response.text:
                self.logger.info(f"AI response generated for email from {email_data['sender']}")
                return response.text.strip()
            else:
                self.logger.warning("Empty response from AI")
                return None
                
        except Exception as e:
            self.logger.error(f"Error generating AI response: {e}")
            return None
    
    def _create_prompt(self, email_data: Dict) -> str:
        """Create a detailed prompt for AI response generation"""
        
        sender = email_data.get('sender', 'Unknown')
        subject = email_data.get('subject', 'No Subject')
        body = email_data.get('body', '')
        
        prompt = f"""
Sen bir profesyonel e-posta asistanısın. Aşağıdaki e-postaya uygun, dostça ve profesyonel bir yanıt oluştur.

GELEN E-POSTA BİLGİLERİ:
Gönderen: {sender}
Konu: {subject}
İçerik: {body}

YANIT KURALLARI:
1. Türkçe yanıt ver
2. Dostça ve profesyonel bir ton kullan
3. E-postanın içeriğine uygun cevap ver
4. Kısa ve öz olsun (maksimum 200 kelime)
5. Gerekirse sorular sor veya ek bilgi iste
6. İmza ekleme, sadece e-posta içeriği oluştur
7. Eğer e-posta bir soru içeriyorsa, mümkün olduğunca cevapla
8. Eğer e-posta bir istek içeriyorsa, nasıl yardımcı olabileceğini belirt

YANIT:
"""
        
        return prompt
    
    def should_respond(self, email_data: Dict) -> bool:
        """Determine if the email should receive an automated response"""
        
        # Skip if it's from our own email
        sender = email_data.get('sender', '').lower()
        if Config.GMAIL_ADDRESS.lower() in sender:
            return False
        
        # Skip common automated emails
        subject = email_data.get('subject', '').lower()
        automated_keywords = [
            'noreply', 'no-reply', 'donotreply', 'automated',
            'auto-reply', 'autoreply', 'notification',
            'unsubscribe', 'bounce', 'delivery failure'
        ]
        
        for keyword in automated_keywords:
            if keyword in sender or keyword in subject:
                return False
        
        # Skip if body is too short (likely spam or automated)
        body = email_data.get('body', '').strip()
        if len(body) < 10:
            return False
        
        return True
    
    def analyze_email_sentiment(self, email_data: Dict) -> str:
        """Analyze the sentiment of the email"""
        try:
            body = email_data.get('body', '')
            
            prompt = f"""
Aşağıdaki e-postanın duygusal tonunu analiz et ve tek kelime ile yanıtla:
- positive (olumlu)
- negative (olumsuz)  
- neutral (nötr)
- urgent (acil)

E-posta içeriği: {body}

Yanıt (sadece tek kelime):
"""
            
            response = self.model.generate_content(prompt)
            sentiment = response.text.strip().lower()
            
            if sentiment in ['positive', 'negative', 'neutral', 'urgent']:
                return sentiment
            else:
                return 'neutral'
                
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {e}")
            return 'neutral'
