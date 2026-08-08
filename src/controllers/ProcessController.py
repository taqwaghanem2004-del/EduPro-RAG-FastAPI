from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from models import ProcessingEnum
from typing import List
from dataclasses import dataclass

@dataclass
class Document:
    page_content: str
    metadata: dict

class ProcessController(BaseController):

    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1].lower()

    def get_file_loader(self, file_id: str):
        file_ext = self.get_file_extension(file_id=file_id)
        file_path = os.path.join(self.project_path, file_id)

        if not os.path.exists(file_path):
            return None

        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")

        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)

        if file_ext in [".docx", ".doc"]:
            return Docx2txtLoader(file_path)

        if file_ext in [".pptx", ".ppt"]:
            return UnstructuredPowerPointLoader(file_path)

        return None

    def get_file_content(self, file_id: str):
        loader = self.get_file_loader(file_id=file_id)
        if loader:
            return loader.load()
        return None

    def process_file_content(self, file_content: list, file_id: str,
                            chunk_size: int=100, overlap_size: int=20):
        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunks = self.process_simpler_splitter(
            texts=file_content_texts,
            metadatas=file_content_metadata,
            chunk_size=chunk_size,
            overlap_size=overlap_size,
        )

        return chunks

    def process_simpler_splitter(self, texts: List[str], metadatas: List[dict],
                                  chunk_size: int, overlap_size: int=20,
                                  splitter_tag: str="\n"):
        full_text = " ".join(texts)

        full_text = full_text.replace('\x00', '')
        full_text = ''.join(c for c in full_text if ord(c) >= 32 or c in '\n\t')

        lines = [doc.strip() for doc in full_text.split(splitter_tag) if len(doc.strip()) > 1]

        chunks = []
        overlap_lines = [] 

        i = 0
        while i < len(lines):
            current_chunk_lines = list(overlap_lines)
            current_chunk = splitter_tag.join(current_chunk_lines) + (splitter_tag if current_chunk_lines else "")

            while i < len(lines) and len(current_chunk) < chunk_size:
                current_chunk += lines[i] + splitter_tag
                current_chunk_lines.append(lines[i])
                i += 1

            if current_chunk.strip():
                chunks.append(Document(
                    page_content=current_chunk.strip(),
                    metadata={}
                ))

            overlap_lines = current_chunk_lines[-2:] if len(current_chunk_lines) >= 2 else current_chunk_lines

        return chunks