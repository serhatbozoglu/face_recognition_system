from app.repository import UserRepository
from app.ui import UserInterface

if __name__ == "__main__":
    repo = UserRepository()
    ui = UserInterface(repo)
    ui.run()
    
    