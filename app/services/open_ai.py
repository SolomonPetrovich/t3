from openai import OpenAI
import json
from pathlib import Path
from typing import Dict, Any
from app.core import settings


def mock_ai_analyze(file_data: Dict[str, Any]) -> str:
    file_size = file_data.get("file_size", 0)
    version = file_data.get("version", 1)
    file_name = file_data.get("file_name", "unknown")
    
    size_mb = file_size / (1024 * 1024)
    
    if size_mb < 0.1:
        size_comment = "Файл очень маленького размера"
    elif size_mb < 1:
        size_comment = "Файл небольшого размера"
    elif size_mb < 10:
        size_comment = "Файл среднего размера"
    elif size_mb < 50:
        size_comment = "Файл большого размера"
    else:
        size_comment = "Файл очень большого размера"
    
    if version == 1:
        version_comment = "Это первая версия документа."
    elif version == 2:
        version_comment = "Документ был обновлен один раз."
    elif version <= 5:
        version_comment = f"Документ был обновлен {version - 1} раз(а)."
    else:
        version_comment = f"Документ активно обновляется (версия {version})."
    
    extension = Path(file_name).suffix.lower()
    type_comments = {
        ".pdf": "PDF документ, вероятно содержит текстовую или графическую информацию.",
        ".docx": "Word документ, текстовый файл с форматированием.",
        ".doc": "Word документ (старый формат), текстовый файл.",
        ".txt": "Текстовый файл без форматирования.",
        ".png": "PNG изображение, возможно скриншот или диаграмма.",
        ".jpg": "JPEG изображение, фотография или иллюстрация.",
        ".jpeg": "JPEG изображение, фотография или иллюстрация.",
        ".gif": "GIF изображение или анимация.",
        ".xlsx": "Excel таблица с данными.",
        ".xls": "Excel таблица (старый формат) с данными.",
        ".csv": "CSV файл с табличными данными.",
        ".pptx": "PowerPoint презентация.",
        ".ppt": "PowerPoint презентация (старый формат).",
        ".zip": "ZIP архив, содержит сжатые файлы.",
        ".rar": "RAR архив, содержит сжатые файлы.",
        ".json": "JSON файл со структурированными данными.",
        ".xml": "XML файл со структурированными данными.",
        ".html": "HTML веб-страница.",
        ".css": "CSS файл со стилями.",
        ".js": "JavaScript файл с программным кодом.",
        ".py": "Python скрипт с программным кодом.",
        ".java": "Java файл с программным кодом.",
        ".cpp": "C++ файл с программным кодом.",
        ".c": "C файл с программным кодом.",
    }
    type_comment = type_comments.get(extension, "Файл неизвестного типа.")
    
    analysis_parts = [
        f"{size_comment} ({size_mb:.2f} MB).",
        version_comment,
        type_comment
    ]
    
    if version > 1:
        analysis_parts.append("Новое изменение может содержать обновленную информацию или исправления.")
    
    if version > 5:
        analysis_parts.append("Высокая частота обновлений может указывать на активную работу над документом.")
    
    if size_mb > 50:
        analysis_parts.append("Рекомендуется проверить возможность оптимизации размера файла.")
    
    return " ".join(analysis_parts)


def analyze_with_openai(file_data: Dict[str, Any]) -> str:
    try:
        client = OpenAI(api_key=settings.OPEANAI_API_KEY)
        
        prompt = f"""
        Проанализируйте следующий документ и предоставьте краткий анализ:
        
        Имя файла: {file_data.get('file_name')}
        Размер: {file_data.get('file_size') / (1024 * 1024):.2f} MB
        Версия: {file_data.get('version')}
        Дата загрузки: {file_data.get('uploaded_at')}
        
        Предоставьте анализ на русском языке, учитывая:
        1. Размер файла и его соответствие типу
        2. Историю версионирования
        3. Возможное содержание на основе расширения файла
        4. Рекомендации по работе с документом
        """
        
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system", 
                    "content": "Вы - профессиональный аналитик документов. Предоставляйте краткие и информативные анализы."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Error during OpenAI analysis: {str(e)}"