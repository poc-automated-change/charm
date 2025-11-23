"""
Intent handlers for processing different user intents
"""
from typing import Dict, Any
from .models import ConversationContext
from integrations.models import ChangeRequest


class BaseHandler:
    """Base class for all intent handlers"""

    def handle(self, context: ConversationContext, message: str) -> Dict[str, Any]:
        """
        Handle the intent

        Args:
            context: Current conversation context
            message: User's message

        Returns:
            Dictionary with bot_message, is_complete, and optional data
        """
        raise NotImplementedError("Subclasses must implement handle()")


class CreateChangeRequestHandler(BaseHandler):
    """Handler for creating a new change request"""

    REQUIRED_FIELDS = [
        'short_description',
        'description',
        'priority',
        'planned_start_date',
        'planned_end_date'
    ]

    FIELD_PROMPTS = {
        'short_description': "What's a brief summary of the change?",
        'description': "Please provide a detailed description of the change.",
        'priority': "What's the priority? (1-Critical, 2-High, 3-Medium, 4-Low)",
        'planned_start_date': "When do you plan to start? (YYYY-MM-DD)",
        'planned_end_date': "When should this be completed? (YYYY-MM-DD)"
    }

    def handle(self, context: ConversationContext, message: str) -> Dict[str, Any]:
        """Handle create_change_request intent"""

        # Initialize context if new intent
        if not context.intent or context.intent != 'create_change_request':
            context.intent = 'create_change_request'
            context.required_fields = self.REQUIRED_FIELDS.copy()
            context.collected_data = {}
            context.next_field = self.REQUIRED_FIELDS[0]
            context.save()

            return {
                'bot_message': f"I'll help you create a change request. {self.FIELD_PROMPTS[context.next_field]}",
                'is_complete': False
            }

        # Collect current field value
        current_field = context.next_field

        # Validate priority field
        if current_field == 'priority':
            message = message.strip()
            if message not in ['1', '2', '3', '4']:
                return {
                    'bot_message': "Please enter a valid priority: 1 (Critical), 2 (High), 3 (Medium), or 4 (Low)",
                    'is_complete': False
                }

        context.collected_data[current_field] = message
        if current_field in context.required_fields:
            context.required_fields.remove(current_field)

        # Check if more fields needed
        if context.required_fields:
            context.next_field = context.required_fields[0]
            context.save()

            return {
                'bot_message': self.FIELD_PROMPTS[context.next_field],
                'is_complete': False
            }

        # All fields collected - create change request
        try:
            change_request = self._create_change_request(context.collected_data)
            context.change_request = change_request
            context.next_field = None
            context.save()

            return {
                'bot_message': f"✓ Change request {change_request.number} created successfully!\n\n"
                             f"Summary: {change_request.short_description}\n"
                             f"Priority: {change_request.priority}\n"
                             f"Status: {change_request.state}",
                'is_complete': True,
                'change_request': {
                    'number': change_request.number,
                    'sys_id': change_request.servicenow_sys_id,
                    'id': change_request.id
                }
            }
        except Exception as e:
            return {
                'bot_message': f"Sorry, I encountered an error creating the change request: {str(e)}",
                'is_complete': False
            }

    def _create_change_request(self, data: Dict[str, str]) -> ChangeRequest:
        """
        Call ServiceNow API to create change request
        For now, this is a placeholder that creates a local record
        """
        from integrations.services import ServiceNowService

        # Try to use the service, but fall back to creating a local record if not configured
        try:
            service = ServiceNowService()
            snow_response = service.create_change_request(
                short_description=data['short_description'],
                description=data['description'],
                priority=data['priority'],
                planned_start_date=data['planned_start_date'],
                planned_end_date=data['planned_end_date']
            )

            # Create local record from ServiceNow response
            change_request = ChangeRequest.objects.create(
                servicenow_sys_id=snow_response['sys_id'],
                number=snow_response['number'],
                short_description=data['short_description'],
                description=data['description'],
                priority=data['priority'],
                state=snow_response.get('state', 'New')
            )
        except Exception:
            # Fallback: Create a placeholder record locally
            # Generate a mock CHG number
            import uuid
            mock_sys_id = str(uuid.uuid4()).replace('-', '')[:32]
            last_cr = ChangeRequest.objects.all().order_by('-id').first()
            next_number = 1 if not last_cr else int(last_cr.number.replace('CHG', '')) + 1
            mock_number = f"CHG{next_number:07d}"

            change_request = ChangeRequest.objects.create(
                servicenow_sys_id=mock_sys_id,
                number=mock_number,
                short_description=data['short_description'],
                description=data['description'],
                priority=data['priority'],
                state='New'
            )

        return change_request


class CheckStatusHandler(BaseHandler):
    """Handler for checking change request status"""

    def handle(self, context: ConversationContext, message: str) -> Dict[str, Any]:
        """Handle check_status intent"""

        # Initialize context if new intent
        if not context.intent or context.intent != 'check_status':
            context.intent = 'check_status'
            context.required_fields = ['change_number']
            context.collected_data = {}
            context.next_field = 'change_number'
            context.save()

            return {
                'bot_message': "What's the change request number you want to check? (e.g., CHG0001234)",
                'is_complete': False
            }

        # Extract change number from message
        change_number = message.strip().upper()

        # Try to find the change request
        try:
            change_request = ChangeRequest.objects.filter(number=change_number).first()

            if not change_request:
                return {
                    'bot_message': f"I couldn't find a change request with number {change_number}. "
                                 "Please check the number and try again.",
                    'is_complete': False
                }

            context.change_request = change_request
            context.required_fields = []
            context.next_field = None
            context.save()

            return {
                'bot_message': f"Change Request: {change_request.number}\n\n"
                             f"Summary: {change_request.short_description}\n"
                             f"Description: {change_request.description}\n"
                             f"Status: {change_request.state}\n"
                             f"Priority: {change_request.priority}\n"
                             f"Created: {change_request.created_at.strftime('%Y-%m-%d %H:%M')}",
                'is_complete': True,
                'change_request': {
                    'number': change_request.number,
                    'sys_id': change_request.servicenow_sys_id,
                    'id': change_request.id
                }
            }
        except Exception as e:
            return {
                'bot_message': f"Sorry, I encountered an error: {str(e)}",
                'is_complete': False
            }


class HelpHandler(BaseHandler):
    """Handler for help requests"""

    def handle(self, context: ConversationContext, message: str) -> Dict[str, Any]:
        """Handle help intent"""

        help_text = """I can help you with the following:

• Create a change request - Say "create a change request" or "new change"
• Check status - Say "check status of CHG0001234"
• List changes - Say "show all my changes"

What would you like to do?"""

        return {
            'bot_message': help_text,
            'is_complete': True
        }


class GreetingHandler(BaseHandler):
    """Handler for greetings"""

    def handle(self, context: ConversationContext, message: str) -> Dict[str, Any]:
        """Handle greeting intent"""

        return {
            'bot_message': "Hello! I'm your IT Change Management Assistant. "
                         "I can help you create and manage ServiceNow change requests.\n\n"
                         "Say 'help' to see what I can do!",
            'is_complete': True
        }


class UnknownHandler(BaseHandler):
    """Handler for unknown intents"""

    def handle(self, context: ConversationContext, message: str) -> Dict[str, Any]:
        """Handle unknown intent"""

        return {
            'bot_message': "I'm not sure what you want to do. "
                         "Say 'help' to see what I can assist you with.",
            'is_complete': True
        }


# Handler registry
HANDLERS = {
    'create_change_request': CreateChangeRequestHandler(),
    'check_status': CheckStatusHandler(),
    'help': HelpHandler(),
    'greeting': GreetingHandler(),
    'unknown': UnknownHandler(),
}


def get_handler(intent: str) -> BaseHandler:
    """Get the appropriate handler for an intent"""
    return HANDLERS.get(intent, UnknownHandler())
