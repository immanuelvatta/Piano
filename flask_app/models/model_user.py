# import the function that will return an instance of a connection
#       folder  folder  file                    function
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE , bcrypt
from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
# model the class after the users table from  database
class User:
    # should change db based on schema you're trying to access
    # DB = 'users_db'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.full_name = f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

        
    #TODO CREATE
    #* the save method will be used when we need to save a new user to our database
    @classmethod
    def create(cls, data):
        """
        This if successful add user to database and returns the new row's id
        """
        query = """INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s,%(email)s,%(password)s);"""
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result
    
    #TODO READ
    #*the display_all_users method will be used when we need to retrieve all the rows of the table user
    @classmethod
    def get_all(cls):
        """
        Function doesn't take in anything but returns a list of instances of dealers
        """
        query = """SELECT * FROM users;"""
        #what is results?  list !! list of what? dictionaries
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        #transform the list of dictionaries -> a list of object/instances
        for dict in results:
            users.append(cls(dict))
        return users
    
    #* the get_one method will be used when we need to retrieve just one specific row of the table
    @classmethod
    def get_one(cls,email):
        query = """SELECT * FROM users WHERE email = %(email)s;"""
        # data = {'id':id}
        
        results = connectToMySQL(DATABASE).query_db(query,{'email': email})
        return cls(results[0])
    
    
    #TODO UPDATE
    #* the update method will be used when we need to update a user in our database
    @classmethod
    def update(cls,data):
        query = """UPDATE users 
                SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = CURRENT_TIMESTAMP 
                WHERE id = %(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #TODO DELETE
    #* the delete method will be used when we need to delete a user from our database
    @classmethod
    def delete(cls,data):
        """
        This function takes in a dictionary containing a key of 'id' and value that is the int representation of the id you want to delete
        """
        query = """DELETE FROM users WHERE id = %(id)s;"""
        # data = {'id': id}
        #returns nothing
        return connectToMySQL(DATABASE).query_db(query,data)
    
    
    @staticmethod
    #data:dict => request.form from the controller file -> html page
    def validator(data:dict):
        
        is_valid = True

        if len(data['first_name']) == 0 or len(data['last_name']) == 0 or len(data['email']) == 0  or len(data['password'])== 0:
            flash("All input fields must be filled", 'err_global_err' )
            is_valid = False 
        else:
            if len(data['first_name']) < 3:
                flash("First name should be at least 2 characters", 'err_user_first_name')
                is_valid = False
            elif not NAME_REGEX.match(data['first_name']):
                flash("First name can only have letters ", 'err_user_first_name')
                is_valid = False
            
            if len(data['last_name']) < 3:
                flash("Last name should be at least 2 characters", 'err_user_last_name')
                is_valid = False
            elif not NAME_REGEX.match(data['last_name']):
                flash("Last name can only have letters ", 'err_user_last_name')
                is_valid = False
            
            query = """SELECT * FROM users WHERE email = %(email)s;"""
            results = connectToMySQL(DATABASE).query_db(query,data)
            if len(results) >= 1:
                flash ('***Email EXISTS***','err_user_email')
                is_valid = False
            if not EMAIL_REGEX.match(data['email']):
                flash('Invalid email format','err_user_email')
                is_valid = False
            
            if len(data['password']) < 8:
                flash("Password must be more than 8 characters",'err_user_password')
                is_valid = False
            
            if data["password"] != data["password1"]:
                flash("Passwords do not match",'err_user_password_confirm')
                is_valid = False
            
        
        flash("You have registered successfully",'success_registration')
        
        return is_valid
    
    @staticmethod
    def validator_login(data):

        query = """SELECT * FROM users WHERE email = %(email)s"""
        results = connectToMySQL(DATABASE).query_db(query,data)
        is_valid = True

        if results:
            if not bcrypt.check_password_hash (results[0]['password'] , data['password']) :
                flash("Password do not match", 'err_user_login_password')
                is_valid = False
        else:
            flash("Email does not exist", 'err_user_login_email')
            is_valid = False
        if is_valid:
            user = results[0]
            return user['email']
        else:
            return False


