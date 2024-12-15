import logging
from flask import Blueprint, jsonify, request
from api.extractor import extractor
from api.quantum_prompt import prompt_generator
from api.schemas import validate_process_request

logger = logging.getLogger(__name__)
api_bp = Blueprint('api', __name__)

@api_bp.route('/prompt', methods=['GET'])
def get_prompt():
    """Endpoint to retrieve the quantum analysis prompt."""
    try:
        prompt = prompt_generator.get_quantum_prompt()
        return jsonify({'prompt': prompt}), 200
    except Exception as e:
        logger.error(f"Error getting prompt: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/process', methods=['POST'])
def process_response():
    """Endpoint to process LLM responses with quantum analysis."""
    try:
        # Validate request
        data = request.get_json()
        if not validate_process_request(data):
            return jsonify({'error': 'Invalid request format'}), 400

        query = data.get('query', '')
        response = data.get('response', '')

        if not response:
            return jsonify({'error': 'Response text is required'}), 400

        # Extract quantum states and entanglements
        quantum_states = extractor.extract_states(response)
        entanglements = extractor.extract_entanglements(response)

        # Prepare response
        analysis_result = {
            'original_query': query,
            'quantum_analysis': {
                'states': quantum_states,
                'entanglements': entanglements
            }
        }

        return jsonify(analysis_result), 200

    except Exception as e:
        logger.error(f"Error processing response: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@api_bp.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500
