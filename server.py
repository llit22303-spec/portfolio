from database import DatabaseManager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


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
    return {'message':'welcome to Portfolio Api'}

@app.get('/rehmanali/portfolio/projects')
def getProjects():
    projects = get_projects()
    return {
        'message': 'Success',
        'projects': projects
    }
    