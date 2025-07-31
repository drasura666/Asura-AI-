import json
import os
import re
import logging
from typing import Dict, List, Any
from difflib import SequenceMatcher

class AsuraAI:
    def __init__(self):
        self.knowledge_base = {}
        self.topics = []
        self.load_knowledge_base()
        
    def load_knowledge_base(self):
        """Load all knowledge files from the knowledge directory"""
        knowledge_dir = 'knowledge'
        
        if not os.path.exists(knowledge_dir):
            logging.error(f"Knowledge directory '{knowledge_dir}' not found")
            return
            
        knowledge_files = [f for f in os.listdir(knowledge_dir) if f.endswith('.json')]
        
        for file_name in knowledge_files:
            file_path = os.path.join(knowledge_dir, file_name)
            topic = file_name.replace('.json', '')
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.knowledge_base[topic] = data
                    self.topics.append(topic)
                    logging.info(f"Loaded knowledge for topic: {topic}")
            except Exception as e:
                logging.error(f"Error loading {file_path}: {str(e)}")
                
        logging.info(f"Loaded {len(self.knowledge_base)} knowledge topics")
    
    def get_available_topics(self) -> List[str]:
        """Return list of available knowledge topics"""
        return self.topics
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for better matching"""
        # Convert to lowercase and remove extra whitespace
        text = text.lower().strip()
        # Remove special characters but keep alphanumeric and spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def find_best_match(self, user_input: str) -> Dict[str, Any]:
        """Find the best matching response from knowledge base"""
        user_input_processed = self.preprocess_text(user_input)
        best_match = None
        best_score = 0.0
        best_topic = None
        
        for topic, knowledge in self.knowledge_base.items():
            if 'responses' not in knowledge:
                continue
                
            for response_data in knowledge['responses']:
                # Check keywords
                keywords = response_data.get('keywords', [])
                keyword_score = 0.0
                
                for keyword in keywords:
                    if keyword.lower() in user_input_processed:
                        keyword_score += 1.0
                
                # Normalize keyword score
                keyword_score = keyword_score / len(keywords) if keywords else 0.0
                
                # Check patterns
                patterns = response_data.get('patterns', [])
                pattern_score = 0.0
                
                for pattern in patterns:
                    pattern_processed = self.preprocess_text(pattern)
                    similarity = self.calculate_similarity(user_input_processed, pattern_processed)
                    if similarity > pattern_score:
                        pattern_score = similarity
                
                # Combined score (weighted average)
                combined_score = (keyword_score * 0.6) + (pattern_score * 0.4)
                
                if combined_score > best_score and combined_score > 0.3:  # Minimum threshold
                    best_score = combined_score
                    best_match = response_data
                    best_topic = topic
        
        return {
            'match': best_match,
            'score': best_score,
            'topic': best_topic
        }
    
    def get_response(self, user_input: str) -> str:
        """Get AI response for user input"""
        if not user_input.strip():
            return "Please provide a question or topic you'd like to discuss."
        
        # Find best match
        match_result = self.find_best_match(user_input)
        
        if match_result['match'] and match_result['score'] > 0.3:
            response_data = match_result['match']
            topic = match_result['topic']
            
            # Get the response text
            response = response_data.get('response', '')
            
            # Add topic context if available
            if topic in self.knowledge_base and 'topic_info' in self.knowledge_base[topic]:
                topic_info = self.knowledge_base[topic]['topic_info']
                if 'context' in topic_info:
                    response = f"**{topic_info['name']}**: {response}"
            
            return response
        
        # Fallback responses
        fallback_responses = [
            "I specialize in advanced scientific and engineering concepts including space-time manipulation, dimensional physics, Prāṇika multi-form substances, space colonization technologies, renewable energy systems, and waste processing innovations. Could you rephrase your question to focus on one of these areas?",
            "My expertise covers cutting-edge topics like black holes as dimensional portals, space-time bending technologies, advanced energy systems using friction and piezometric principles, and innovative waste processing methods. What specific aspect would you like to explore?",
            "I'm designed to discuss revolutionary concepts in physics and engineering, particularly related to dimensional manipulation, space colonization, sustainable energy, and advanced materials like Prāṇika. Please provide more specific details about what you'd like to know.",
            "As Asura-AI, I focus on breakthrough scientific concepts including quantum dimensional physics, space-time engineering, renewable energy innovations, and advanced space technologies. Could you be more specific about which area interests you?",
        ]
        
        # Simple hash-based selection for consistent responses
        response_index = hash(user_input.lower()) % len(fallback_responses)
        return fallback_responses[response_index]
