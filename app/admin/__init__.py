from sqladmin import Admin
from app.core import engine
from .views import FileAdmin, AnalysisAdmin



def setup_admin(app):
    admin = Admin(
        app, 
        engine,
        title="Document Service Admin",
        base_url="/admin"
    )
    
    admin.add_view(FileAdmin)
    admin.add_view(AnalysisAdmin)
    
    return admin