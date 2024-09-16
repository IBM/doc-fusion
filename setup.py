from setuptools import setup, find_packages

setup(
    name="docfusion",
    version="0.1.0",
    author="Manoj Jahgirdar",
    author_email="manoj.jahgirdar@in.ibm.com",
    description="Doc Fusion is a Data Sourcing framework capable of parsing various data types such as pdf, txt, md, docx, xlsx, csv and even a webpage url.",
    long_description="Doc Fusion is a Data Sourcing framework capable of parsing various data types such as pdf, txt, md, docx, xlsx, csv and even a webpage url. It can handle several types of data such as multi columnar, tabular and invoices. The framework uses an LLM (Large Language Model) Agentic approach, where each data type is managed by a dedicated LLM Agent.",
    long_description_content_type="text/markdown",
    url="https://github.com/IBM/doc-fusion",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0 License",  # Replace with your license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=open("requirements.txt").read().splitlines(),  # Use requirements.txt for dependencies
)
