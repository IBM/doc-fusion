import time
from main import DocFusion

if __name__ == '__main__':
    response = DocFusion.configure()
    print(response)
    
    # response = DocFusion.configure(
    #     input_data={
    #         "agent_verbose": False,
    #         "model_id": "mistralai/mixtral-8x7b-instruct-v01",
    #         "wx_project_id": "XXXXX",
    #         "wx_api_key": "XXXXXX",
    #         "wx_endpoint": "XXXXX",
    #         "chunk": True,
    #         "chunk_table_rows": True,
    #         "chunk_table_row_size": 3,
    #         "chunk_table_row_overlap": 1,
    #         "chunk_table_output_format": "md",
    #         "chunk_text_size": 512,
    #         "chunk_text_overlap": 10
    #     }
    # )
    # print(response)
    
    start_time = time.time()
    
    # #Load structured data
    # docs = DocFusion.source(
    #     input_data="Source this: docs/samplestructured1.xlsx"
    # )

    # # Load unstructured data
    # docs = DocFusion.source(
    #     input_data="Source this: docs/rfpdocument.pdf"
    # )

    # Load website data
    docs = DocFusion.source(
        input_data="Source this: https://www.sentinelone.com/anthology/8base/"
    )

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Exec time: {round(execution_time, 2)} sec")

    print("Sourced DOCUMENTS:", docs)
