import json
import os
import logging
import time
from langchain.tools import Tool
from langchain.tools.render import render_text_description
from langchain.agents import AgentExecutor
from langchain_core.agents import AgentAction, AgentFinish
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import MessagesPlaceholder
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames
from langchain_ibm import WatsonxLLM
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from .output_parser import CustomJSONAgentOutputParser
from config.app_config import AppConfig
app_config = AppConfig()

# Set up logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'ERROR'))
logger = logging.getLogger(__name__)

class Agent:
    def __init__(self, tools, planning) -> None:
        try:
            with open(app_config.AGENT_CONFIG_PATH, 'r') as configfile:
                self.config = json.load(configfile)
        except FileNotFoundError:
            logger.error("Configuration file not found.")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing configuration file: {e}")
            raise

        self.tools = tools
        self.planning = planning
            
        # Load configuration with defaults
        self.WX_ENDPOINT = self.config.get('wx_endpoint')
        self.IBM_CLOUD_API_KEY = self.config.get('wx_api_key')
        self.WX_PROJECT_ID = self.config.get('wx_project_id')
        self.model_id = self.config.get('model_id')
        self.verbose = self.config.get('agent_verbose', False)
        
        # Initialize the agent
        self._init_agent()

    def _init_agent(self) -> None:
        """Initializes the LLM agent with WatsonxLLM and custom settings."""
        try:
            parameters = {
                GenTextParamsMetaNames.MAX_NEW_TOKENS: 500,
                GenTextParamsMetaNames.MIN_NEW_TOKENS: 10,
                GenTextParamsMetaNames.DECODING_METHOD: 'greedy',
            }

            watsonx_llm = WatsonxLLM(
                url=self.WX_ENDPOINT,
                apikey=self.IBM_CLOUD_API_KEY,
                project_id=self.WX_PROJECT_ID,
                model_id=self.model_id,
                params=parameters
            )

            system_prompt = self.planning
            user_input = '{input}\n{agent_scratchpad}\n(reminder to respond in a JSON blob no matter what and use tools only if necessary)'

            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    MessagesPlaceholder(variable_name="chat_history", optional=True),
                    ("user", user_input)
                ]
            )

            tools_chat = self.tools
            prompt_chat = prompt.partial(
                tools=render_text_description(list(tools_chat)),
                tool_names=", ".join([t.name for t in tools_chat]),
            )

            # Create the chain of runnables for agent chat handling
            agent_chat = (
                RunnablePassthrough.assign(
                    agent_scratchpad=lambda x: format_log_to_str(x["intermediate_steps"]),
                )
                | prompt_chat
                | watsonx_llm.bind(stop=["}\n"])
                | CustomJSONAgentOutputParser()
            )

            # Set up the agent executor
            self.agent_executor_chat = AgentExecutor(
                agent=agent_chat,
                tools=tools_chat,
                verbose=self.verbose,
                handle_parsing_errors=True
            )

            # Message history for session management
            message_history = ChatMessageHistory()
            self.agent_with_chat_history = RunnableWithMessageHistory(
                self.agent_executor_chat,
                get_session_history=lambda session_id: message_history,
                input_messages_key="input",
                history_messages_key="chat_history",
            )
        
        except Exception as e:
            logger.error(f"Error initializing agent: {e}")
            raise

    def invoke_agent(self, input_: str) -> dict:
        """Invokes the agent to process the input and return the result."""
        try:
            start_time = time.time()
            answer = self.agent_with_chat_history.invoke(
                {"input": input_},
                config={"configurable": {"session_id": "watsonx"}}
            )
            end_time = time.time()
            execution_time = round(end_time - start_time, 2)

            logger.info(f"Agent execution completed in {execution_time} seconds.")
            return {
                "output": answer['output'],
                "execution_time": f"{execution_time} sec"
            }
        except Exception as e:
            logger.error(f"Error during agent invocation: {e}")
            raise
