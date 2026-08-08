from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os

class DataController(BaseController):
    
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576  

        self.video_types = [
            "video/mp4",
            "video/quicktime",       # MOV
            "video/x-msvideo",       # AVI
            "video/x-matroska"       # MKV
        ]

        self.document_types = [
            "text/plain",            # TXT
            "application/pdf",       # PDF
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",   # DOCX
            "application/vnd.openxmlformats-officedocument.presentationml.presentation", # PPTX
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"          # XLSX
        ]

        self.video_max_size = 500   
        self.document_max_size = 20 

    def validate_uploaded_file(self, file: UploadFile):

        all_allowed_types = self.document_types + self.video_types

        if file.content_type not in all_allowed_types:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

       
        if file.content_type in self.video_types:
            max_size = self.video_max_size
        else:
            max_size = self.document_max_size

        if file.size > max_size * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value

    def generate_unique_filepath(self, orig_file_name: str, project_id: str):

        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)

        cleaned_file_name = self.get_clean_file_name(
            orig_file_name=orig_file_name
        )

        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_file_name
        )

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_file_name
            )

        return new_file_path, random_key + "_" + cleaned_file_name

    def get_clean_file_name(self, orig_file_name: str):

      
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name