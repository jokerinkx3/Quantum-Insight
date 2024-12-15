from typing import Dict, Any

def validate_process_request(data: Dict[str, Any]) -> bool:
    """
    Validate the process request data format.
    
    Expected format:
    {
        "query": str
    }
    """
    if not isinstance(data, dict):
        return False
        
    if 'query' not in data:
        return False
        
    if not isinstance(data['query'], str):
        return False
        
    return True
