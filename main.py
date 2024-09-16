import json
import logging
import getpass
from src.core.agent import Agent
from src.core.structured_data_loader import StructuredLoader
from src.core.web_crawler_loader import WebCrawler
from src.core.unstructured_data_loader import UnstructuredLoader
from src.core.splitter import Splitter
from langchain.tools import Tool
import os
from config.app_config import AppConfig
app_config = AppConfig()

# Set up logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'ERROR'))
logger = logging.getLogger(__name__)

class DocFusion:
    def __init__(self, config_path=app_config.AGENT_CONFIG_PATH):
        self.config_path = config_path

    def write_to_config(self, file_path, obj):
        """
        Writes a dictionary to a JSON configuration file.

        Args:
            file_path (str): The path of the configuration file to write to.
            obj (dict): The dictionary to write to the configuration file.

        Returns:
            None
        """
        try:
            with open(file_path, 'w') as ffile:
                json.dump(obj, ffile, indent=2)
            logger.info('Configuration file successfully written!')
            return True
        except Exception as e:
            logger.error(f"Error writing configuration file: {e}")
            return False

    def get_agent_config(self):
        """
        Prompts user for agent configuration input and returns the configuration as a dictionary.

        Args:
            None
        
        Returns:
            None
        """
        def parse_boolean_input(input_str):
            return input_str.lower() in ['yes', 'y']

        try:
            config = {
                'wx_endpoint': input('Enter watsonx.ai endpoint URL (https://us-south.ml.cloud.ibm.com): ') or 'https://us-south.ml.cloud.ibm.com',
                'wx_api_key': getpass.getpass('Enter watsonx.ai API Key: '),
                'wx_project_id': input('Enter watsonx.ai project ID: '),
                'model_id': input('Enter LLM to use (mistralai/mixtral-8x7b-instruct-v01): ') or 'mistralai/mixtral-8x7b-instruct-v01',
                'agent_verbose': parse_boolean_input(input('Do you want to see the LLM Agent\'s reasoning process? (yes/no): ') or 'no')
            }
            return config
        except Exception as e:
            logger.error(f"Error in agent configuration input: {e}")
            raise e

    @staticmethod
    def configure(input_data:dict=None):
        """
        Handles the configuration process, either using input data or prompting the user.

        Args:
            input_data (dict): The input config file.
        
        Returns:
            None
        """
        docfusion = DocFusion()
        keys_to_extract = ['wx_endpoint', 'wx_api_key', 'wx_project_id', 'model_id', 'agent_verbose']
        if input_data:
            config = {}

            for key in keys_to_extract:
                if key in input_data:
                    config[key] = input_data.pop(key)

            if config:
                docfusion.write_to_config(app_config.AGENT_CONFIG_PATH, config)

            logger.info(f"Configuration provided: {input_data}")
            input_data = str(input_data)
        else:
            is_agent_config_required = True
            if os.path.isfile(app_config.AGENT_CONFIG_PATH):
                logger.info("Agent config file exists, skipping agent config process...")
                try:
                    with open(app_config.AGENT_CONFIG_PATH, 'r') as config:
                        agent_config = json.load(config)        
                    is_agent_config_required = False
                    for key in keys_to_extract:
                        if key not in agent_config:
                            logger.info(f"{key} not found in Agent config file, prompting user to reconfigure...")
                            is_agent_config_required = True
                            break
                except json.JSONDecodeError:
                        is_agent_config_required = True
        
            if is_agent_config_required:
                logger.info("Starting agent configuration process...")
                agent_config = docfusion.get_agent_config()
                docfusion.write_to_config(app_config.AGENT_CONFIG_PATH, agent_config)
                if agent_config.get('wx_api_key') == "":
                    print("\nPlease provide a valid watsonx.ai API Key!")
                    exit(1)
                elif agent_config.get('wx_project_id') == "":
                    print("\nPlease provide a valid watsonx.ai project ID!")
                    exit(1)

        from src.tools.ask_user import ask_user
        from src.tools.write_config_file import write_config_file

        ask_user_tool = Tool(
            name="ask_user",
            func=ask_user,
            description="Use this tool to ask the user a question and get their response."
        )

        write_config_file_tool = Tool(
            name="write_config_file",
            func=write_config_file,
            description="Use this tool to create the config.json file based on the user's responses. The input to this tool should be a stringified json."
        )

        # Load planning prompt
        with open(app_config.CONFIGURATOR_PLANNING_PROMPT, 'r') as ffile:
            agent_planning_prompt = ffile.read()

        agent = Agent(
            tools=[ask_user_tool, write_config_file_tool],
            planning=agent_planning_prompt
        )

        logger.info("Configuring data...")
        agent_configurator = agent.invoke_agent(input_=input_data)
        logger.info("Configuration completed.")
        return agent_configurator.get('output')

    @staticmethod
    def source(input_data):
        """
        Sources data by recognizing the appropriate loader and splitting if necessary.

        Args:
            input_data (str): The natural language input consisting of a File or URL to be sourced.
        
        Returns:
            None
        """
        nlp_input = input_data

        from src.tools.recognize_loader import recognize_loader

        recognize_loader_tool = Tool(
            name="recognize_loader",
            func=recognize_loader,
            description="Use this tool to recognize the right loader to source the document."
        )

        # Load planning prompt
        with open(app_config.ORCHESTRATOR_PLANNING_PROMPT, 'r') as ffile:
            agent_planning_prompt = ffile.read()

        agent = Agent(
            tools=[recognize_loader_tool],
            planning=agent_planning_prompt
        )

        agent_orchestrator = agent.invoke_agent(input_=nlp_input)
        intent_entity = dict(agent_orchestrator.get('output'))

        logger.info(f"Intent Entity: {intent_entity}")
        class_name = intent_entity.get('function')
        params = intent_entity.get('param')

        # Dynamically retrieve the loader class
        loader_class = globals().get(class_name)
        if not loader_class:
            raise ValueError(f"Loader class '{class_name}' not found.")

        loader_instance = loader_class(params)
        documents = loader_instance.load()

        # Check if chunking is enabled in the config
        try:
            with open(app_config.DATA_CONFIG_PATH, 'r') as configfile:
                config = json.load(configfile)
        except FileNotFoundError:
            config = {}

        try:
            is_chunking_required =  bool(config.get('chunk')) if 'chunk' in config else False
        except TypeError as e:
            logging.error(f"TypeError: Invalid type for 'chunk' value: {e}")
            is_chunking_required = False

        if is_chunking_required:
            logger.info(f"Chunking ...")
            chunks = Splitter().split(documents=documents)
            return chunks
        else:
            try:
                text_list = documents.get('text', [])
                tables_list = documents.get('tables', [])
                combined_list = text_list + [doc for sublist in tables_list for doc in sublist]
                return combined_list

            except Exception as e:
                logging.error(f"An error occurred while merging lists: {e}")
                return []
            
