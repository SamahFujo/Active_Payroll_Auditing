"""
Filename: models.py

Purpose: This file contains the database models for the application.

Dependencies:

Flask (version not specified)
Flask_SQLAlchemy (version not specified)
Flask_Login (version not specified)
Werkzeug (version not specified)
Pandas (version not specified)
datetime (built-in Python module)
Code structure:

The file starts with importing necessary modules and packages.
The User class is defined with attributes such as user_id, username, password, created_at, and last_login. It also has a relationship with the Role class and implements the UserMixin class from Flask_Login.
The Role class is defined with attributes such as role_id and name.
The UserRoles class is defined with attributes such as id, user_id, and role_id. It also has a relationship with the User and Role classes.
The system_keywords class is defined with attributes such as kid, Keyword, Label, File_name, created_at, updated_at, created_by, and updated_by. It also has methods to fetch, add, update, and delete keywords from the database.
The system_high_ranking_positions class is defined with attributes such as pid, position_title, created_at, updated_at, created_by, and updated_by. It also has methods to fetch, add, update, and delete positions from the database.
The user_logs class is defined with attributes such as id, user_id, log_type, log_details, and created_at. It also has a method to add logs to the database.

"""

#
# class User(db.Model, UserMixin):
#     # attributes
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(500), nullable=False)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(500), nullable=False)
#
#     def __init__(self, name, username, password):
#         self.name = name
#         self.username = username
#         self.password = generate_password_hash(password, method='s ha256')


# class User(db.Model, UserMixin):
#     # attributes
#     user_id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(500), nullable=False)
#
#     # foreign keys
#     position_id = db.Column(db.Integer, db.ForeignKey('position.position_id', ondelete='CASCADE'))
#
#     # relationships
#     roles = db.relationship('Role', secondary='user_roles')
#
#     def __init__(self, employee_name, username, password, email, position_id):
#         self.username = username
#         self.password = generate_password_hash(password, method='sha256')
#
#     def get_id(self):
#         return self.user_id
#
#
# class Role(db.Model):
#     # attributes
#     role_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#
#     def __init__(self, name):
#         self.name = name
#
#
# class UserRoles(db.Model):
#     __tablename__ = 'user_roles'
#     # attributes
#     id = db.Column(db.Integer, primary_key=True)
#
#     # foreign keys
#     employee_id = db.Column(db.Integer(), db.ForeignKey('employee.employee_id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer(), db.ForeignKey('role.role_id', ondelete='CASCADE'))
#
#     def __init__(self, employee_id, role_id):
#         self.employee_id = employee_id
#         self.role_id = role_id





#
# class User(db.Model, UserMixin):
#     # attributes
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(500), nullable=False)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(500), nullable=False)
#
#     def __init__(self, name, username, password):
#         self.name = name
#         self.username = username
#         self.password = generate_password_hash(password, method='s ha256')


from application import db
from datetime import datetime
from application import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
import pandas as pd

from application.Control_Panel.validation import sanitize_input

class Role(db.Model):
    # attributes
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    print(created_at)
    def __init__(self, name):
        self.name = name


class User(db.Model, UserMixin):
    # attributes
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # relationships
    roles = db.relationship('Role', secondary='user_roles')

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password, method='sha256')

    def get_id(self):
        return self.user_id
    def UpdateLastLogin(self):
        self.last_login = datetime.utcnow()



class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    # attributes
    id = db.Column(db.Integer, primary_key=True)

    # foreign keys
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.role_id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id




class system_keywords(db.Model):
    kid = db.Column(db.Integer, primary_key=True)
    Keyword = db.Column(db.String(100), nullable=False)
    Label = db.Column(db.String(100), nullable=False)
    File_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    created_by = db.Column(db.String(100), nullable=False)
    updated_by = db.Column(db.String(100), nullable=True)

    def __init__(self, Keyword, Label, File_name, created_by, updated_by):
        self.Keyword = Keyword
        self.Label = Label
        self.File_name = File_name
        # self.created_at = created_at
        # self.updated_at = updated_at
        self.created_by = created_by
        self.updated_by = updated_by

    def Fetch_All_Keywords_dataframe(self):
        return pd.DataFrame(db.session.query(system_keywords).all())


    def Fetch_File_Name_by_Id(id):
        return db.session.query(system_keywords).filter_by(kid=id).first().File_name

    def Fetch_All_labels_by_File_Name_dataframe(File_name):
        return pd.DataFrame(db.session.query(system_keywords).filter_by(File_name=File_name).all())

    def Fetch_All_labels_by_File_Name_And_Keyword_dataframe(File_name, Keywords):
        return pd.DataFrame(db.session.query(system_keywords).filter_by(File_name=File_name, Keyword=Keywords).all())

    def Check_Keyword_Exist(Keywords, File_name):
        return db.session.query(system_keywords).filter_by(Keyword=Keywords, File_name=File_name).first()

    def Add_Keyword_check_not_exist(Keyword, Label, File_name, created_by):
        if system_keywords.Check_Keyword_Exist(Keyword, File_name) is None:

            new_keyword = system_keywords(sanitize_input(Keyword), Label, File_name, datetime.datetime.now(), None, created_by, None)
            db.session.add(new_keyword)
            db.session.commit()
            duplication = 'True'
        else:
            duplication = 'duplicate'

        return duplication


    def Update_Keyword_check_exist(Keywords, Label, File_name, updated_by):
        if system_keywords.Check_Keyword_Exist(Keywords, File_name) is not None:
            db.session.query(system_keywords).filter_by(Keyword=Keywords, File_name=File_name).update(
                {system_keywords.Label: Label, system_keywords.updated_at: datetime.now(),
                 system_keywords.keyword: Keywords,
                 system_keywords.File_name: File_name,
                 system_keywords.updated_by: updated_by})
            db.session.commit()
            duplication = 'no-duplicate'
        else:
            duplication = 'duplicate'

        return duplication

    def Update_keyword_by_id(id, Keywords, Label, File_name, updated_by):
        duplication = system_keywords.Update_Keyword_check_exist(Keywords, Label, File_name,updated_by)
        if duplication == 'no-duplicate':
            db.session.query(system_keywords).filter_by(kid=id).update(
                {system_keywords.Label: Label.upper(),
                 system_keywords.updated_at: datetime.now(),
                 system_keywords.File_name: File_name.upper(),
                 system_keywords.keyword: Keywords.upper(),
                 system_keywords.updated_by: updated_by})
            db.session.commit()
        return duplication


    def Fetch_all_label_by_kid_dataframe(kid):
        return pd.DataFrame(db.session.query(system_keywords).filter_by(kid=kid).all())


    def Delete_Keyword_by_Id(id):
        db.session.query(system_keywords).filter_by(kid=id).delete()
        db.session.commit()
        return True

    def Fetch_keyword_by_File_Name_list(File_names):
        return db.session.query(system_keywords).filter_by(File_name=File_names).all()


    def Fetch_keyword_by_File_Name_and_Label_list(File_names, Label):
        return db.session.query(system_keywords).filter_by(File_name=File_names, Label=Label).all()



class system_high_ranking_positions(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    position_title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True,default=datetime.utcnow)
    created_by = db.Column(db.String(100), nullable=False)
    updated_by = db.Column(db.String(100), nullable=True)

    def __init__(self, position_title, created_by, updated_by):
        self.position_title = position_title
        # self.created_at = created_at
        # self.updated_at = updated_at
        self.created_by = created_by
        self.updated_by = updated_by

    def Fetch_All_Positions_dataframe(self):
        return pd.DataFrame(db.session.query(system_high_ranking_positions).all())

    def Fetch_All_positions_dataframe_by_position_title(position_title):
        return pd.DataFrame(db.session.query(system_high_ranking_positions).filter_by(position_title=position_title).all())

    def Check_Position_Exist(position_title):
        return db.session.query(system_high_ranking_positions).filter_by(position_title=position_title).first()

    def Add_position_check_not_exist(position_title, created_by):
        if system_high_ranking_positions.Check_Position_Exist(position_title) is None:
            new_position = system_high_ranking_positions(position_title, datetime.now(), None, created_by, None)
            db.session.add(sanitize_input(new_position))
            db.session.commit()
            duplication = 'no-duplicate'
        else:
            duplication = 'duplicate'

        return duplication


    def Delete_position_check_exist(position_title):
        if system_high_ranking_positions.Check_Position_Exist(position_title) is not None:
            db.session.query(system_high_ranking_positions).filter_by(position_title=position_title).delete()
            db.session.commit()
            return True
        else:
            return False

    def Update_position_check_exist(pid, position_title, updated_by):
        if system_high_ranking_positions.Check_Position_Exist(position_title) is None:
            db.session.query(system_high_ranking_positions).filter_by(pid=pid).update(
                {system_high_ranking_positions.position_title: sanitize_input(position_title),
                 system_high_ranking_positions.updated_at: datetime.now(),
                 system_high_ranking_positions.updated_by: updated_by})
            db.session.commit()
            duplication = 'no-duplicate'
        else:
            duplication = 'duplicate'
        return duplication

    # def Update_position_by_id(pid, position_title, updated_by):
    #     db.session.query(system_high_ranking_positions).filter_by(pid=pid).update({system_high_ranking_positions.position_title: position_title, system_high_ranking_positions.updated_at: datetime.now(), system_high_ranking_positions.updated_by: updated_by})
    #     db.session.commit()
    #     return True
    #

    def Fetch_All_position_in_list(self):
        return db.session.query(system_high_ranking_positions).all()

    def Fetch_poistion_by_id(pid):
        return db.session.query(system_high_ranking_positions).filter_by(pid=pid).first()

    def Fetch_poistion_by_title(position_title):
        return db.session.query(system_high_ranking_positions).filter_by(position_title=position_title).first()

    def Delete_position_by_id(pid):
        db.session.query(system_high_ranking_positions).filter_by(pid=pid).delete()
        db.session.commit()

class user_logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    log_type = db.Column(db.String(500), nullable=False)
    log_details = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    def __init__(self, user_id, log_type, log_details):
        self.user_id = user_id
        self.log_type = log_type
        self.log_details = log_details
        # self.created_at = created_at

    def Add_log(user_id, log_type, log_details):
        new_log = user_logs(user_id, log_type, log_details, datetime.now())
        db.session.add(new_log)
        db.session.commit()

    def Fetch_All_Logs_dataframe(self):
        return pd.DataFrame(db.session.query(user_logs).all())

