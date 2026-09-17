from database import DatabaseManager
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from upload_image import upload_image
from pydantic import BaseModel
from typing import Optional

# Initialize app
app = FastAPI()
# intialize database
db = DatabaseManager()


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=['*'],
    allow_origins=['*']
)
# Models
class Project(BaseModel):
    name: str
    desc: str
    github_link: Optional[str]
    preview_link: Optional[str]
    category_id: int
    
# Helper Functions
def get_projects():
    try:
        conn, cursor = db.getConnection()
        cursor.execute("SELECT * FROM projects")
        projects = cursor.fetchall()
        return projects
    except Exception as e:
        return e
    finally:
        db.closeConnection()
        
# routes
@app.get('/')
def show():
    return {'message':'welcome to Portfolio Api Admin Api'}

@app.get('/rehmanali/portfolio/projects')
def getProjects():
    projects = get_projects()
    return {
        'message': 'Success',
        'projects': projects
    }
@app.post('/images/upload')
def upload_api(file:UploadFile = File(...)):
    try:
        image_url = upload_image(file.file)
        return {
            'message':'image uploaded success',
            'success': True,
            'image_url': image_url
        }
    except Exception as e:
        return {
                    'message':str(e),
                    'success': False
        }

@app.post('/project/upload')
def upload_project(project:Project):
    pass
if __name__ == "__main__":
    uvicorn.run("server:app",port=9090, host='localhost', reload=True)
    