from flask_app import app
#! import controllers
from flask_app.controllers import controller_user, controller_routes, controller_piano


#MAKE SURE THIS IS AT THE BOTTOM
if __name__=="__main__":
    app.run(debug=True)