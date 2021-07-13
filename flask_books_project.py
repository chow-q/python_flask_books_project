from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_mysqldb import MySQL
#创建flask应用程序实例
app = Flask(__name__)
app.secret_key = 'mima'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:******@192.168.1.*/flask_sql_demo'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#自定义表单类
class AuthorForm(FlaskForm):
    author = StringField('作者:', validators=[DataRequired()])
    book = StringField('书籍:', validators=[DataRequired()])
    submit = SubmitField('提交')

#用户模型
class Author(db.Model):
    #定义表
    __tablename__ = 'authors'
    #定义字段
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16), unique=True)
    books = db.relationship('Book',backref='author')
    def __repr__(self):
        return 'Author: %s' % self.name
#书籍模型
class Book(db.Model):
    #定义表
    __tablename__ = 'books'
    #定义字段
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16), unique=True)
    author_id = db.Column(db.Integer,db.ForeignKey('authors.id'))
    def __repr__(self):
        return 'Author: %s %s' % self.name

#删除作者
@app.route('/delete_author/<author_id>')
def delete_author(author_id):
    #查询数据库，是否有该ID的作者，如果有就删除（先删书籍，再删作者），没有就提示错误

    author = Author.query.get(author_id)
    #如果有就删除，先删书，再删作者
    if author:
        try:
            #查询书之后直接删除
            Book.query.filter_by(author_id=author.id).delete()
            #删除作者
            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除作者出错')
            db.session.rollback()
    else:
        #没有提示错误
        flsh('作者找不到')
    return redirect(url_for('index'))

#删除书籍
@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    #查询数据库，是否有该ID的书籍，如果有就删除，没有就提示错误

    book = Book.query.get(book_id)
    #如果有就删除
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除书籍出错')
            db.session.rollback()
    else:
        flash('书籍找不到')



    #返回当前网址--》重定向
    return redirect(url_for('index'))
#定义路由以及函数视图，通过装饰器实现
@app.route("/",methods=['GET','POST'])
def index():
    #创建自定义的表单类
    author_form = AuthorForm()
    '''
    验证逻辑：
    1、调用wtf的函数实现验证
    2、验证通过获取数据
    3、判断作者是否存在
    4、如果作者存在，判断书籍是否存在，没有重复书籍就添加数据，如果重复就提示错误
    5、如果作者不存在，添加作者和书籍
    6、验证不通过就提示错误
    '''
    #1、调用wtf的函数实现验证
    if author_form.validate_on_submit():
        #2、验证通过获取数据
        author_name = author_form.author.data
        book_name = author_form.book.data
        #3、判断作者是否存在
        author = Author.query.filter_by(name=author_name).first()
        #4、如果作者存在，
        if author:
            #判断书籍是否存在，，
            book = Book.query.filter_by(name=book_name).first()
            #如果重复就提示错误
            if book:
                flash('已存在同名书籍')
            #没有重复书籍就添加数据
            else:
                try:
                    new_book = Book(name=book_name,author_id=author.id)
                    db.session.add(new_book)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash('添加书籍失败')
                    db.session.rollback()
        else:
            #5、如果作者不存在，添加作者和书籍
            try:
                new_author = Author(name=author_name)
                db.session.add(new_author)
                db.session.commit()

                new_book = Book(name=book_name, author_id=new_author.id)
                db.session.add(new_book)
                db.session.commit()
            except Exception as e:
                 print(e)
                 flash('添加作者和书籍失败')
                 db.session.rollback()

    else:
        #6、验证不通过就提示错误
        if request.method == 'POST':
            flash('参数不全')

    #查询所有的作者信息，让信息传递给模板
    authors = Author.query.all()
    return render_template('index.html',authors=authors,form=author_form)

#启动程序
if __name__=='__main__':
    #db.drop_all()
    #db.create_all()
    app.run()


