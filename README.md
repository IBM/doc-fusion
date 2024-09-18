# Doc Fusion - A data extraction framework powered by watsonx.ai

[![Build](https://img.shields.io/badge/build-0.1.0-green.svg)](/)
[![License](https://img.shields.io/badge/license-APACHE_2.0-blue.svg)](LICENSE)

## Overview

In an era where data drives decisions and innovation, efficiently extracting meaningful information from vast amounts of text is more crucial than ever. The quality of data utilised in your AI applications can make a significant difference in the value it provides, hence the first step towards building apowerful AI application is an efficient strategy for handling the data utilised.While the data processing stage involves two major processes - data extraction and data curation, the framework we built primarily focuses on the former stage.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Example Usage](#example-usage)
5. [API Reference](#api-reference)
6. [Contributing](#contributing)
7. [License](#license)
8. [Acknowledgments](#acknowledgments)

## Features

- Parse different data formats (pdf, docx, xlsx, csv).

- Web crawling and parsing of HTML content from web pages.

- Handle complexities in data such as multi columnar, and tabular data.

- Leverage an Agentic approach, where the Agent would decide how each data format is handled.

- Extract metadata from the file – filename, page no., in case of tables – table id, row id, column name.  

- Provide a user-friendly configuration mechanism for chunking.

## Installation

### Prerequisites

- Python version 3.11.9 or higher

### Installing via Package Manager

```bash
pip install docfusion==0.1.0
```

## Example Usage

1. Import the library

    ```python
    import docfusion
    ```

2. Configuration

    - 2.1. Interactive configuration

        ```python
        docfusion.configure()
        ```

        This will invoke the LLM agent to configure the agent and data parameters.

    - 2.2. Non-interactive configuration

        ```python
        docfusion.configure(
          input_data={
                    "agent_verbose": False,
                    "model_id": "mistralai/mixtral-8x7b-instruct-v01",
                    "wx_project_id": "****",
                    "wx_api_key": "****",
                    "wx_endpoint": "https://us-south.ml.cloud.ibm.com",
                    "chunk": True,
                    "chunk_table_rows": True,
                    "chunk_table_row_size": 3,
                    "chunk_table_row_overlap": 1,
                    "chunk_table_output_format": "md",
                    "chunk_text_size": 512,
                    "chunk_text_overlap": 10
                }
        )
        ```

3. Data Sourcing

    ```python
    # Load structured data
    docs = DocFusion.source(
        input_data="Source this: docs/samplestructured1.xlsx"
    )
    ```

    ```python
    # Load unstructured data
    docs = DocFusion.source(
        input_data="Source this: docs/insurance.pdf"
        )
    ```

    ```python
    # Load website data
    docs = docfusion.source(
        input_data="Source this: https://www.sentinelone.com/anthology/8base/"
    )

    ```

## API Reference

### Class: `DocFusion`

#### Method: `source()`

- Description: This method is used to source data from various sources such as structured data files, unstructured data files, and web pages.
- Parameters:
  - `input_data` (str): The input data to be sourced. This can be a file path, a URL, or a string.
- Returns: A list of documents.

### Class: `src/core/agent.py`

#### Method: `Agent`

- Description: This class is used to create an agent for data sourcing.
- Parameters:
  - `model_id` (str): The ID of the model to be used for the agent.
  - `wx_project_id` (str): The project ID of the WatsonX.ai project.
  - `wx_api_key` (str): The API key for the WatsonX.ai project.

### Class `src/core/output_parser.py`

#### Method: `OutputParser`

- Description: This class is used to parse the output from the agent.
- Parameters:
  - `output` (str): The output from the agent.
- Returns: A list of documents.

### Class `src/core/structured_data_loader.py`

#### Method: `StructuredDataLoader`

- Description: This class is used to load structured data from a file.
- Parameters:
  - `file_path` (str): The path to the file to be loaded.
- Returns: A list of documents.

### Class `src/core/unstructured_data_loader.py`

#### Method: `UnstructuredDataLoader`

- Description: This class is used to load unstructured data from a file.
- Parameters:
  - `file_path` (str): The path to the file to be loaded.
- Returns: A list of documents.

### Class `src/core/web_crawler_loader.py`

#### Method: `WebCrawlerLoader`

- Description: This class is used to load web page data from a URL.
- Parameters:
  - `url` (str): The URL of the web page to be loaded.
- Returns: A list of documents.

### Class `src/core/splitter.py`

#### Method: `Splitter`

- Description: This class is used to split the data into chunks.
- Parameters:
  - `documents` (list): The list of documents to be split into chunks.
- Returns: A list of chunks.

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to get started.

### Reporting Issues

If you encounter any issues or have feature requests, please report them using [GitHub Issues](https://github.com/IBM/doc-fusion/issues).

### Code of Conduct

Please note that this project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [manoj.jahgirdar@ibm.com](mailto:manoj.jahgirdar@ibm.com).

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details. 

## Acknowledgments

We would like to thank the following resources and contributors:

- [watsonx.ai](https://www.ibm.com/products/watsonx-ai) - IBM's platform for building AI applications.
- [LangChain](https://python.langchain.com/v0.1/docs/getting_started/introduction/) - A framework for building language model applications.
- [Contributors](https://github.com/IBM/doc-fusion/graphs/contributors) - A list of notable contributors or a link to the GitHub contributors page.

## Contributors

We would like to thank the following individuals for their contributions to this project:

- [Ravi Kumar Srirangam](https://www.linkedin.com/in/ravisrirangam) - Solutions Architect, IBM
- [Manoj Jahgirdar](https://www.linkedin.com/in/manojjahgirdar) - Software Engineer, IBM
- [Surya Deep Singh](https://www.linkedin.com/in/surya-deep-singh-b9b94813a) - Software Engineer, IBM
- [Aishwarya Pradeep](https://www.linkedin.com/in/aishwarya-pradeep108) - Software Engineer, IBM
- [Suman P](https://www.linkedin.com/in/suman-p-756266202) - Software Engineer, IBM

