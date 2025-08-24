from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import pymysql.cursors
from datetime import datetime
import os

# 首先实例化Flask应用
app = Flask(__name__)
app.secret_key = os.urandom(24)  # 用于会话管理的密钥

# 数据库配置 - 请根据你的实际配置修改
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234567890',
    'database': 'students',
    'port': 3306,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 数据库连接函数
def get_db_connection():
    connection = pymysql.connect(** db_config)
    return connection

# 所有路由定义都放在app实例化之后

# 登录页面
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['userType']
        
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                if user_type == 'admin':
                    # 管理员登录
                    cursor.execute(
                        "SELECT * FROM tb_admininfo WHERE account = %s AND password = %s",
                        (username, password)
                    )
                    admin = cursor.fetchone()
                    if admin:
                        session['user_id'] = admin['id']
                        session['username'] = admin['account']
                        session['user_type'] = 'admin'
                        return redirect(url_for('admin_dashboard'))
                    else:
                        flash('管理员账号或密码错误', 'error')
                else:
                    # 学生登录
                    cursor.execute(
                        "SELECT * FROM tb_studentsinfo WHERE number = %s AND password = %s",
                        (username, password)
                    )
                    student = cursor.fetchone()
                    if student:
                        session['user_id'] = student['id']
                        session['username'] = student['name']
                        session['student_number'] = student['number']
                        session['user_type'] = 'student'
                        return redirect(url_for('student_dashboard'))
                    else:
                        flash('学生账号或密码错误', 'error')
        finally:
            connection.close()
    
    return render_template('login.html')

# 管理员仪表盘
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

# 学生仪表盘
@app.route('/student/dashboard')
def student_dashboard():
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    return render_template('student_dashboard.html')

# 学生选课页面
@app.route('/student/courses')
def student_courses():
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    student_id = session['user_id']
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            # 获取已选课程
            cursor.execute("""
                SELECT c.* FROM tb_courseinfo c
                JOIN tb_student_course sc ON c.id = sc.courseid
                WHERE sc.studentid = %s
            """, (student_id,))
            selected_courses = cursor.fetchall()
            
            # 获取未选课程
            cursor.execute("""
                SELECT * FROM tb_courseinfo
                WHERE id NOT IN (
                    SELECT courseid FROM tb_student_course
                    WHERE studentid = %s
                )
            """, (student_id,))
            available_courses = cursor.fetchall()
    finally:
        connection.close()
    
    return render_template('student_courses.html', 
                          selected_courses=selected_courses,
                          available_courses=available_courses)

# 选择课程
@app.route('/student/select/<int:course_id>')
def select_course(course_id):
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    student_id = session['user_id']
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            # 检查是否已选该课程
            cursor.execute("""
                SELECT * FROM tb_student_course
                WHERE studentid = %s AND courseid = %s
            """, (student_id, course_id))
            
            if cursor.fetchone():
                flash('您已选择该课程', 'warning')
            else:
                # 添加选课记录
                cursor.execute("""
                    INSERT INTO tb_student_course (studentid, courseid)
                    VALUES (%s, %s)
                """, (student_id, course_id))
                connection.commit()
                flash('课程选择成功', 'success')
    finally:
        connection.close()
    
    return redirect(url_for('student_courses'))

# 退选课程
@app.route('/student/deselect/<int:course_id>')
def deselect_course(course_id):
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    student_id = session['user_id']
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            # 删除选课记录
            cursor.execute("""
                DELETE FROM tb_student_course
                WHERE studentid = %s AND courseid = %s
            """, (student_id, course_id))
            connection.commit()
            flash('课程退选成功', 'success')
    finally:
        connection.close()
    
    return redirect(url_for('student_courses'))

# 学生个人信息页面
@app.route('/student/info', methods=['GET', 'POST'])
def student_info():
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    student_id = session['user_id']
    connection = get_db_connection()
    
    try:
        if request.method == 'POST':
            # 更新学生信息
            name = request.form['name']
            password = request.form['password']
            sex = request.form['sex']
            birthday = request.form['birthday'] if request.form['birthday'] else None
            other = request.form['other']
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE tb_studentsinfo
                    SET name = %s, password = %s, sex = %s, birthday = %s, other = %s
                    WHERE id = %s
                """, (name, password, sex, birthday, other, student_id))
                connection.commit()
            
            # 更新会话中的用户名
            session['username'] = name
            flash('个人信息更新成功', 'success')
            return redirect(url_for('student_info'))
        
        # 获取学生信息
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM tb_studentsinfo
                WHERE id = %s
            """, (student_id,))
            student = cursor.fetchone()
    finally:
        connection.close()
    
    return render_template('student_info.html', student=student)

# 管理员学生管理页面
@app.route('/admin/manage_students')
def manage_students():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    search_query = request.args.get('search', '')
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            if search_query:
                # 按姓名搜索学生
                cursor.execute(
                    "SELECT * FROM tb_studentsinfo WHERE name LIKE %s ORDER BY id DESC",
                    (f'%{search_query}%',)
                )
            else:
                # 获取所有学生
                cursor.execute("SELECT * FROM tb_studentsinfo ORDER BY id DESC")
            
            students = cursor.fetchall()
    finally:
        connection.close()
    
    return render_template('manage_students.html', students=students, search_query=search_query)

# 添加学生
@app.route('/admin/add_student', methods=['GET', 'POST'])
def add_student():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        number = request.form['number']
        password = request.form['password']
        name = request.form['name']
        sex = request.form['sex']
        birthday = request.form['birthday'] if request.form['birthday'] else None
        other = request.form['other']
        
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 检查学号是否已存在
                cursor.execute(
                    "SELECT * FROM tb_studentsinfo WHERE number = %s",
                    (number,)
                )
                if cursor.fetchone():
                    flash('该学号已存在', 'error')
                    return redirect(url_for('add_student'))
                
                # 添加新学生
                cursor.execute("""
                    INSERT INTO tb_studentsinfo (number, password, name, sex, birthday, other)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (number, password, name, sex, birthday, other))
                connection.commit()
                flash('学生添加成功', 'success')
                return redirect(url_for('manage_students'))
        finally:
            connection.close()
    
    return render_template('student_form.html', student=None, action="add")

# 编辑学生
@app.route('/admin/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    try:
        if request.method == 'POST':
            password = request.form['password']
            name = request.form['name']
            sex = request.form['sex']
            birthday = request.form['birthday'] if request.form['birthday'] else None
            other = request.form['other']
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE tb_studentsinfo
                    SET password = %s, name = %s, sex = %s, birthday = %s, other = %s
                    WHERE id = %s
                """, (password, name, sex, birthday, other, student_id))
                connection.commit()
                flash('学生信息更新成功', 'success')
                return redirect(url_for('manage_students'))
        
        # 获取学生信息
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM tb_studentsinfo WHERE id = %s",
                (student_id,)
            )
            student = cursor.fetchone()
            
            if not student:
                flash('学生不存在', 'error')
                return redirect(url_for('manage_students'))
    finally:
        connection.close()
    
    return render_template('student_form.html', student=student, action="edit")

# 删除学生
@app.route('/admin/delete_student/<int:student_id>')
def delete_student(student_id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 先删除该学生的选课记录
            cursor.execute(
                "DELETE FROM tb_student_course WHERE studentid = %s",
                (student_id,)
            )
            
            # 再删除学生信息
            cursor.execute(
                "DELETE FROM tb_studentsinfo WHERE id = %s",
                (student_id,)
            )
            connection.commit()
            flash('学生删除成功', 'success')
    finally:
        connection.close()
    
    return redirect(url_for('manage_students'))

# 管理员课程管理页面
@app.route('/admin/manage_courses')
def manage_courses():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tb_courseinfo ORDER BY id DESC")
            courses = cursor.fetchall()
    finally:
        connection.close()
    
    return render_template('manage_courses.html', courses=courses)

# 添加课程
@app.route('/admin/add_course', methods=['GET', 'POST'])
def add_course():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        coursename = request.form['coursename']
        teacher = request.form['teacher']
        score = request.form['score']
        
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO tb_courseinfo (coursename, teacher, score)
                    VALUES (%s, %s, %s)
                """, (coursename, teacher, score))
                connection.commit()
                flash('课程添加成功', 'success')
                return redirect(url_for('manage_courses'))
        finally:
            connection.close()
    
    return render_template('course_form.html', course=None, action="add")

# 编辑课程
@app.route('/admin/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    try:
        if request.method == 'POST':
            coursename = request.form['coursename']
            teacher = request.form['teacher']
            score = request.form['score']
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE tb_courseinfo
                    SET coursename = %s, teacher = %s, score = %s
                    WHERE id = %s
                """, (coursename, teacher, score, course_id))
                connection.commit()
                flash('课程信息更新成功', 'success')
                return redirect(url_for('manage_courses'))
        
        # 获取课程信息
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM tb_courseinfo WHERE id = %s",
                (course_id,)
            )
            course = cursor.fetchone()
            
            if not course:
                flash('课程不存在', 'error')
                return redirect(url_for('manage_courses'))
    finally:
        connection.close()
    
    return render_template('course_form.html', course=course, action="edit")

# 删除课程
@app.route('/admin/delete_course/<int:course_id>')
def delete_course(course_id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 先删除该课程的选课记录
            cursor.execute(
                "DELETE FROM tb_student_course WHERE courseid = %s",
                (course_id,)
            )
            
            # 再删除课程信息
            cursor.execute(
                "DELETE FROM tb_courseinfo WHERE id = %s",
                (course_id,)
            )
            connection.commit()
            flash('课程删除成功', 'success')
    finally:
        connection.close()
    
    return redirect(url_for('manage_courses'))

# 查看选课信息
@app.route('/admin/view_selections')
def view_selections():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    # 获取排序参数，默认为按课程名称排序
    sort_by = request.args.get('sort_by', 'course')
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            if sort_by == 'student':
                # 按学生姓名排序
                cursor.execute("""
                    SELECT sc.id, s.name as student_name, s.number as student_number, 
                           c.coursename as course_name, c.teacher as teacher, c.score as score
                    FROM tb_student_course sc
                    JOIN tb_studentsinfo s ON sc.studentid = s.id
                    JOIN tb_courseinfo c ON sc.courseid = c.id
                    ORDER BY s.name ASC
                """)
            else:
                # 按课程名称排序
                cursor.execute("""
                    SELECT sc.id, s.name as student_name, s.number as student_number, 
                           c.coursename as course_name, c.teacher as teacher, c.score as score
                    FROM tb_student_course sc
                    JOIN tb_studentsinfo s ON sc.studentid = s.id
                    JOIN tb_courseinfo c ON sc.courseid = c.id
                    ORDER BY c.coursename ASC
                """)
            
            selections = cursor.fetchall()
    finally:
        connection.close()
    
    return render_template('view_selections.html', selections=selections, sort_by=sort_by)

# 登出功能
@app.route('/logout')
def logout():
    session.clear()
    flash('已成功退出登录', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
