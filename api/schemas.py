from typing import Dict, Any

def validate_process_request(data: Dict[str, Any]) -> bool:
    """
    Validate the process request data format.
    
    Expected format:
    {
        "query": str,
        "response": str
    }
    """
    if not isinstance(data, dict):
        return False
        
    required_fields = ['query', 'response']
    if not all(field in data for field in required_fields):
        return False
        
    if not all(isinstance(data[field], str) for field in required_fields):
        return False
        
    return True
