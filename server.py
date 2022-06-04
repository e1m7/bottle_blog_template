from bottle import run, get, post, request, redirect, error, template, auth_basic
import sqlite3

LOGIN = "admin"
PASS = "admin"

def check(user, password):
    return user == LOGIN and password == PASS

@get('/')
def index():
    return template('index.html')


@get('/blog')
@get('/blog/')
def blog_list():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT blog_id, blog_title FROM blog_table")
    result = c.fetchall()
    c.close()
    return template('blog.html', result=result)


@get('/blog/<post_id:int>')
@get('/blog/<post_id:int>/')
def post_detail(post_id):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM blog_table WHERE blog_id=?", (post_id,))
    result = c.fetchall()
    c.close()
    return template('detail.html', result=result)


@get('/blog/post_form')
@get('/blog/post_form/')
@get('/blog/post_form/<post_id:int>')
@get('/blog/post_form/<post_id:int>/')
@auth_basic(check)
def post_form_get(post_id=None):
    if post_id:
        conn = sqlite3.connect('blog.db')
        c = conn.cursor()
        c.execute("SELECT * FROM blog_table WHERE blog_id=?", (post_id,))
        result = c.fetchall()
        c.close()
        if result:
            return template('post_form.html', result=result)
        else:
            return redirect('/blog')
    else:
        return template('post_form.html', result=None)


@post('/blog/post_form')
@post('/blog/post_form/')
@post('/blog/post_form/<post_id:int>')
@post('/blog/post_form/<post_id:int>/')
@auth_basic(check)
def post_form_post(post_id=None):
    new_title = request.forms.new_title
    new_body = request.forms.new_body
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    if post_id:
        c.execute("UPDATE blog_table SET blog_title=?, blog_body=? WHERE blog_id LIKE ?", (new_title, new_body, post_id))
    else:
        c.execute("INSERT INTO blog_table (blog_title, blog_body) VALUES (?,?)", (new_title, new_body))
    conn.commit()
    c.close()
    post_id = post_id or c.lastrowid
    return redirect(f'/blog/{post_id}')


@get('/blog/post_delete/<post_id:int>')
@get('/blog/post_delete/<post_id:int>/')
@auth_basic(check)
def post_delete(post_id):
    if post_id:
        conn = sqlite3.connect('blog.db')
        c = conn.cursor()
        c.execute("DELETE FROM blog_table WHERE blog_id=?", (post_id,))
        conn.commit()
        c.close()
    return redirect('/blog')


@error(404)
@error(401)
def error(code):
    return template('error.html')


run(debug=True, reloader=True)