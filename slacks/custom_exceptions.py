
class InvalidMessageObjectException(Exception):
    """Raised when message_object is invalid"""
    pass

class NotImplementedException(Exception):
    """Raised when a functionality is not yet implemented"""
    pass

class NoWebhookUrlException(Exception):
    """Raised when no webhook URL was provided"""
    pass

class NoMessageException(Exception):
	"""Rased when no message was provided"""