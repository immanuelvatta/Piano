from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE , bcrypt
from flask_app.models import model_user
from flask import flash
import re

class Score:
    
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.composer = data['composer']
        self.description = data['description']
        self.music_sheet = data['music_sheet']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    
    #TODO CREATE
    #* the save method will be used when we need to save a new user to our database
    @classmethod
    def create(cls, data):
        query = """INSERT INTO scores (user_id, name, composer, description, music_sheet)
                VALUES (%(user_id)s, %(name)s,%(composer)s,%(description)s, %(music_sheet)s);"""
        # print(data['user_id'])
        # print(len(data['music_sheet']))
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result
    
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM scores JOIN users ON scores.user_id = users.id;"""
        
        results = connectToMySQL(DATABASE).query_db(query)
        
        # Initializing an empty list to store all the score instances.
        all_scores = [] #list
        # Looping through each 'user_dict' in the query results.
        for user_dict in results:
            score_instance = cls(user_dict) 
            user_data = {
                'id' : user_dict['users.id'],
                'created_at' : user_dict['users.created_at'],
                'updated_at' : user_dict['users.updated_at'],
                'first_name' : user_dict['first_name'],
                'last_name' : user_dict['last_name'],
                'email' : user_dict['email'],
                'password' : user_dict['password']
            }
            user_instance = model_user.User(user_data) #creating an instance of user
            # Assigning the 'user_instance' as the 'user' attribute of the 'score_instance'.
            score_instance.user = user_instance 
            #populating the list that we assigned to the instance
            all_scores.append(score_instance) 
        return all_scores
    
    @classmethod
    def get_one(cls,id):
        query = """SELECT * FROM scores WHERE id = %(id)s;"""
        results = connectToMySQL(DATABASE).query_db(query,{'id': id})
        return cls(results[0])
    
    #TODO For search function
    @classmethod
    def get_score_by_name(cls,search_query):
        query = """SELECT * FROM scores WHERE name REGEXP %s;"""
        pattern = re.escape(search_query)
        result = connectToMySQL(DATABASE).query_db(query, (f"(?i){pattern}",))
        matched_scores = [cls(score) for score in result]
        return matched_scores
    
    @classmethod
    def get_one_score(cls,id):
        query = """SELECT * FROM scores JOIN users ON scores.user_id = users.id
                WHERE scores.id = %(id)s;"""
        results = connectToMySQL(DATABASE).query_db(query,{'id':id})
        if not results:
            return []
        dictionary = results[0]
        score_instance = cls(dictionary)
        score_instance.music_sheet = results[0]['music_sheet']
        if dictionary['users.id'] != None:
            
            for user_dict in results:
                user_data = {
                    **user_dict,
                    'id' :  user_dict['users.id'],
                    'created_at' :  user_dict['users.created_at'],
                    'updated_at' :  user_dict['users.updated_at']
                }
                user_instance = model_user.User(user_data)
                score_instance.user = user_instance
        return score_instance
    
    @classmethod
    def update(cls,data):
        query = """UPDATE scores
                SET name = %(name)s, composer = %(composer)s, description = %(description)s, music_sheet = %(music_sheet)s 
                WHERE id = %(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def delete(cls,id):
        query = """DELETE FROM scores WHERE id = %(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,{'id':id})
    
    @staticmethod
    def score_validator(data):
        is_valid = True
        # self.name = data['name']
        # self.composer = data['composer']
        # self.description = data['description']
        # self.music_sheet = data['music_sheet']
        if len(data['name']) < 3:
            flash("Name of Composition should be at least 3 characters", 'err_score_name')
            is_valid = False
        if len(data['composer']) < 3:
            flash("Composer should be at least 3 characters", 'err_score_name')
            is_valid = False
        if len(data['description']) < 3:
            flash("Description should be at least 3 characters", 'err_score_name')
            is_valid = False
        
        #!validate music_sheet
        music_sheet = data.get('music_sheet')
        if not music_sheet:
            flash('Please upload a music sheet.', 'err_score_music_sheet')
            is_valid = False
        
        return is_valid