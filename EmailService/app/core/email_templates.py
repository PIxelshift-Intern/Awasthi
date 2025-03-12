from typing import Dict, Any, List, Optional
import json

class EmailTemplate:
    @staticmethod
    def base_template(subject: str, content: str, is_html: bool = True) -> Dict[str, Any]:

        content_type = "text/html" if is_html else "text/plain"
        return {
            "personalizations": [],
            "subject": subject,
            "content": [{"type": content_type, "value": content}],
        }
    
    @staticmethod
    def add_recipients(
        template: Dict[str, Any], 
        to_emails: List[str],
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None,
    ) -> Dict[str, Any]:

        personalization = {
            "to": [{"email": email} for email in to_emails],
        }
        
        if cc_emails:
            personalization["cc"] = [{"email": email} for email in cc_emails]
        
        if bcc_emails:
            personalization["bcc"] = [{"email": email} for email in bcc_emails]
        
        template["personalizations"].append(personalization)
        return template
    
    @staticmethod
    def add_dynamic_data(
        template: Dict[str, Any],
        data: Dict[str, Any],
        personalization_index: int = 0
    ) -> Dict[str, Any]:

        if len(template["personalizations"]) <= personalization_index:
            raise IndexError("Personalization index out of range")
        
        template["personalizations"][personalization_index]["dynamic_template_data"] = data
        return template
    
    @staticmethod
    def add_sender(template: Dict[str, Any], from_email: str, from_name: Optional[str] = None) -> Dict[str, Any]:

        from_data = {"email": from_email}
        if from_name:
            from_data["name"] = from_name
        
        template["from"] = from_data
        return template
    
    @staticmethod
    def add_tracking(template: Dict[str, Any], enable_open_tracking: bool = True, enable_click_tracking: bool = True) -> Dict[str, Any]:

        template["tracking_settings"] = {
            "open_tracking": {"enable": enable_open_tracking},
            "click_tracking": {"enable": enable_click_tracking},
        }
        return template
    
    @staticmethod
    def create_campaign_email(
        subject: str,
        content: str,
        from_email: str,
        from_name: Optional[str] = None,
        is_html: bool = True,
    ) -> Dict[str, Any]:

        template = EmailTemplate.base_template(subject, content, is_html)
        template = EmailTemplate.add_sender(template, from_email, from_name)
        template = EmailTemplate.add_tracking(template)
        return template