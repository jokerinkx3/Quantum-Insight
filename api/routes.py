from flask import Blueprint, jsonify, request, render_template
import logging
from api.quantum_prompt import prompt_generator
from api.extractor import extractor
from api.llm_service import llm_service

logger = logging.getLogger(__name__)
api_bp = Blueprint('api', __name__)

@api_bp.route('/test')
def test_interface():
    """Serve the test interface."""
    try:
        return render_template('test.html')
    except Exception as e:
        logger.error(f"Error rendering template: {str(e)}")
        return jsonify({'error': 'Template rendering failed'}), 500

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
    """Endpoint to process queries through LLM and perform quantum analysis."""
    try:
        # Log incoming request
        logger.debug("Received process request")
        
        # Validate request
        data = request.get_json()
        if not isinstance(data, dict) or 'query' not in data:
            logger.warning("Invalid request format")
            return jsonify({'error': 'Query is required'}), 400

        query = data.get('query', '')
        if not query:
            logger.warning("Empty query received")
            return jsonify({'error': 'Query cannot be empty'}), 400

        # Get quantum prompt
        quantum_prompt = prompt_generator.get_quantum_prompt()
        logger.debug("Retrieved quantum prompt")
        
        try:
            # Process through LLM
            logger.debug("Processing query through LLM")
            llm_result = llm_service.process_query(query, quantum_prompt)
            
            # Extract quantum states and entanglements
            logger.debug("Extracting quantum states and entanglements")
            quantum_states = extractor.extract_states(llm_result['full_response'])
            entanglements = extractor.extract_entanglements(llm_result['full_response'])

            # Prepare response
            analysis_result = {
                'original_query': query,
                'quantum_analysis': {
                    'states': quantum_states,
                    'entanglements': entanglements
                }
            }
            
            logger.debug("Successfully processed query")
            return jsonify(analysis_result), 200
            
        except ValueError as e:
            logger.error(f"API key error: {str(e)}")
            return jsonify({'error': str(e)}), 503  # Service Unavailable
        except Exception as e:
            logger.error(f"LLM processing error: {str(e)}")
            return jsonify({'error': 'Error processing query through LLM'}), 500

    except Exception as e:
        logger.error(f"Error processing response: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@api_bp.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500
