import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s  %(levelname)s : %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


list_of_files=[
    ".env",
    "requirements.txt",
    "main.py",
    "README.md",
    "research/experiment_with_jupiter.ipynb",
    "src/pdf_loader.py",
    "src/data_cleaning.py",
    "src/text_splitters.py",
    "src/embedding.py",
    "src/vector_store.py",
]


for file in list_of_files:
    filepath=Path(file)
    filedir,filename=os.path.split(filepath)
    print(f"Processing file: {filepath}")
    print(f"Directory: {filedir}, Filename: {filename}")

    if filedir != "":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"created directory: {filedir}")
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        with open(filepath, "w") as f:
            pass
        logging.info(f"created file: {filepath}")
    else:
        logging.info(f"file already exists: {filepath}")
