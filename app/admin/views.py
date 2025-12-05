from sqladmin import ModelView
from app.models import FileRecord, AnalysisRecord


class FileAdmin(ModelView, model=FileRecord):    
    name = "File"
    name_plural = "Files"
    icon = "fa-solid fa-file"
    
    column_list = [
        FileRecord.id,
        FileRecord.original_name,
        FileRecord.version,
        FileRecord.file_size,
        FileRecord.uploaded_at,
        FileRecord.uploaded_by
    ]
    
    column_searchable_list = [FileRecord.original_name]
    
    column_sortable_list = [
        FileRecord.id,
        FileRecord.original_name,
        FileRecord.version,
        FileRecord.file_size,
        FileRecord.uploaded_at
    ]
    
    column_default_sort = [(FileRecord.uploaded_at, True)]  
    
    column_formatters = {
        FileRecord.file_size: lambda m, a: f"{m.file_size / 1024:.2f} KB" if m.file_size else "0 KB",
        FileRecord.uploaded_at: lambda m, a: m.uploaded_at.strftime("%Y-%m-%d %H:%M:%S") if m.uploaded_at else "",
    }
    
    form_columns = [
        FileRecord.original_name,
        FileRecord.version,
        FileRecord.path,
        FileRecord.file_size,
        FileRecord.uploaded_by
    ]
    
    column_labels = {
        FileRecord.id: "ID",
        FileRecord.original_name: "File Name",
        FileRecord.version: "Version",
        FileRecord.path: "Path",
        FileRecord.file_size: "Size",
        FileRecord.uploaded_at: "Upload Date",
        FileRecord.uploaded_by: "Uploaded By"
    }
    
    column_details_list = [
        FileRecord.id,
        FileRecord.original_name,
        FileRecord.version,
        FileRecord.path,
        FileRecord.file_size,
        FileRecord.uploaded_at,
        FileRecord.uploaded_by
    ]
    
    
    page_size = 20
    page_size_options = [10, 20, 50, 100]
    
    can_export = True
    export_types = ["csv", "json"]


class AnalysisAdmin(ModelView, model=AnalysisRecord):    
    name = "Analysis"
    name_plural = "Analyses"
    icon = "fa-solid fa-brain"
    
    column_list = [
        AnalysisRecord.id,
        AnalysisRecord.file_id,
        AnalysisRecord.analysis_result,
        AnalysisRecord.analyzed_at
    ]
    
    column_searchable_list = [AnalysisRecord.analysis_result]
    
    column_sortable_list = [
        AnalysisRecord.id,
        AnalysisRecord.file_id,
        AnalysisRecord.analyzed_at
    ]
    
    column_default_sort = [(AnalysisRecord.analyzed_at, True)]
    
    column_formatters = {
        AnalysisRecord.analyzed_at: lambda m, a: m.analyzed_at.strftime("%Y-%m-%d %H:%M:%S") if m.analyzed_at else "",
        AnalysisRecord.analysis_result: lambda m, a: (m.analysis_result[:100] + "...") if m.analysis_result and len(m.analysis_result) > 100 else m.analysis_result
    }
    
    form_columns = [
        AnalysisRecord.file_id,
        AnalysisRecord.analysis_result
    ]
    
    column_labels = {
        AnalysisRecord.id: "ID",
        AnalysisRecord.file_id: "File ID",
        AnalysisRecord.analysis_result: "Analysis Result",
        AnalysisRecord.analyzed_at: "Analysis Date"
    }
    
    column_details_list = [
        AnalysisRecord.id,
        AnalysisRecord.file_id,
        AnalysisRecord.analysis_result,
        AnalysisRecord.analyzed_at
    ]
    
    page_size = 20
    page_size_options = [10, 20, 50, 100]
    
    can_export = True
    export_types = ["csv", "json"]