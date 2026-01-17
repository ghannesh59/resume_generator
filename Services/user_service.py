import importlib
from typing import Dict, Any

class UserService:
    def __init__(self):
        # Dictionary to map API keys to their corresponding data files
        self.api_key_mapping = {
            "123e4567-e89b-12d3-a456-426614174000": "data.mohith_resume",
            "f47ac10b-58cc-4372-a567-0e02b2c3d479": "data.viswa_resume",
            "550e8400-e29b-41d4-a716-446655440000": "data.karthik_resume",
            "6ba7b810-9dad-11d1-80b4-00c04fd430c8": "data.varshith_resume",
            "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6": "data.prudhvi_resume",
            "f27020e2-176f-4d13-99ce-3a00a7d89135": "data.revanth_resume"
        }
    
    def load_user_data(self, api_key: str) -> Dict[str, Any]:
        """
        Loads user data based on the provided API key
        
        Args:
            api_key (str): The API key to identify the user
            
        Returns:
            Dict[str, Any]: Dictionary containing user data
            
        Raises:
            ValueError: If the API key is invalid or data cannot be loaded
        """
        try:
            # Get the module path from the mapping
            module_path = self.api_key_mapping.get(api_key)
            if not module_path:
                raise ValueError(f"Invalid API key: {api_key}")
            
            # Dynamically import the user data module
            user_module = importlib.import_module(module_path)
            
            # Create a dictionary of all non-private attributes
            user_data = {
                attr: getattr(user_module, attr)
                for attr in dir(user_module)
                if not attr.startswith('_')
            }
            
            return user_data
            
        except ImportError:
            raise ValueError(f"Could not load data for API key: {api_key}")
        except Exception as e:
            raise ValueError(f"Error loading user data: {str(e)}")
