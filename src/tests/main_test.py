import unittest
from unittest.mock import patch, MagicMock
import os
from main import DocFusion

class TestDocFusion(unittest.TestCase):

    @patch('builtins.input', side_effect=[
        'https://us-south.ml.cloud.ibm.com',  # watsonx.ai endpoint URL
        '',  # watsonx.ai API Key (handled by getpass)
        'project_id',  # watsonx.ai project ID
        'mistralai/mixtral-8x7b-instruct-v01',  # LLM model ID
        'no'  # Agent reasoning process
    ])
    @patch('getpass.getpass', return_value='test_api_key')  # Mock API Key input
    @patch('main.DocFusion.write_to_config')
    def test_user_input_configuration(self, mock_write_to_config, mock_getpass, mock_input):
        """Test the configure method with user input."""
        
        # Mock the agent's invocation (simulating agent asking questions)
        with patch('src.core.agent.Agent.invoke_agent', return_value={'output': 'docs'}):
            result = DocFusion.configure()

            # Assertions to verify behavior
            self.assertEqual(result, 'docs')
            mock_write_to_config.assert_called_with('config/agent_config.json', {
                'wx_endpoint': 'https://us-south.ml.cloud.ibm.com',
                'wx_api_key': 'test_api_key',
                'wx_project_id': 'project_id',
                'model_id': 'mistralai/mixtral-8x7b-instruct-v01',
                'agent_verbose': False
            })

    @patch('main.DocFusion.write_to_config')
    def test_file_input_configuration(self, mock_write_to_config):
        """Test the configure method with input from a configuration file."""
        
        input_data = {
            "agent_verbose": True,
            "model_id": "mistralai/mixtral-8x7b-instruct-v01",
            "wx_project_id": "yyyy",
            "wx_api_key": "xxxx",
            "wx_endpoint": "https://us-south.ml.cloud.ibm.com",
            "chunk": True,
            "chunk_table_rows": True,
            "chunk_table_row_size": 3,
            "chunk_table_row_overlap": 1,
            "chunk_table_output_format": "md",
            "chunk_text_size": 512,
            "chunk_text_overlap": 10
        }

        # Mock the agent's invocation (simulating agent response)
        with patch('src.core.agent.Agent.invoke_agent', return_value={'output': 'chunks'}):
            result = DocFusion.configure(input_data=input_data)

            # Assertions to verify behavior
            self.assertEqual(result, 'chunks')
            mock_write_to_config.assert_called_with('config/agent_config.json', {
                'wx_endpoint': 'https://us-south.ml.cloud.ibm.com',
                'wx_api_key': 'xxxx',
                'wx_project_id': 'yyyy',
                'model_id': 'mistralai/mixtral-8x7b-instruct-v01',
                'agent_verbose': True
            })

if __name__ == '__main__':
    unittest.main()
