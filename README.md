# python_flask_books_project
Introduction:
-----------------------------------------------
In python web framework flask and mysql implementation books to add and delete.

Involving module:
-------------------------------------------------

from flask import Flask,render_template,request,flash,redirect,url_for

from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField

from wtforms.validators import DataRequired


Database：
-------------------------------------------------
uncomment：

if __name__=='__main__':

    #db.drop_all()
    
    #db.create_all()
    
    app.run()
    

example：
---------------------------------------------------

![image](https://user-images.githubusercontent.com/73530205/125425609-0db1223d-0e10-460f-acbd-1c28490b3ac7.png)

