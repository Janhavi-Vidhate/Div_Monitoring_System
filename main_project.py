
from flask import Flask, render_template, request,redirect,url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import  MySQL
import MySQLdb.cursors
import  re
import  datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/div_record'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
db = SQLAlchemy(app)


app.secret_key='dgzsjgjf1232'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='password'
app.config['MYSQL_DB']='div_record'

# Intialize MySQL
mysql = MySQL(app)

#************************************************************************************************************************************************************
class student_table(db.Model):
    '''
    sid, s_first_name, s_last_name ,s_email,s_mobno ,s_dob
    '''
    sid = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(12), nullable=False)
    s_firstname= db.Column(db.String(100), nullable=False)
    s_lastname= db.Column(db.String(100), nullable=False)
    s_email = db.Column(db.String(100), nullable=False)
    s_mobno = db.Column(db.String(20), nullable=False)
    s_dob= db.Column(db.String(20), nullable=False)


class teacher_table(db.Model):
    '''
    sid, s_first_name, s_last_name ,s_email,s_mobno ,s_dob ,username ,password
    '''
    tid = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(12), nullable=False)
    t_firstname= db.Column(db.String(100), nullable=False)
    t_lastname= db.Column(db.String(100), nullable=False)
    t_email = db.Column(db.String(100), nullable=False)
    t_mobno = db.Column(db.String(12), nullable=False)
    t_sub= db.Column(db.String(100), nullable=False)

class notice_table(db.Model):
    
    notice_no = db.Column(db.Integer,primary_key=True)
    notice = db.Column(db.String(500), nullable=False)


class Attendance(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(500), nullable=False)
    total_attendance = db.Column(db.String(500), nullable=True)
    total_lectures = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(500), nullable=False)

class Susers(db.Model):
    '''
    sid, s_first_name, s_last_name ,s_email,s_mobno ,s_dob ,username ,password
    '''
    sid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(12), nullable=False)


class tusers(db.Model):
    '''
    sid, s_first_name, s_last_name ,s_email,s_mobno ,s_dob ,username ,password
    '''
    tid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(12), nullable=False)

#************************************************************************************************************************************************************

@app.route("/")
def pg1():
    return render_template('1_title.html')

@app.route("/identification")
def identification():
    return render_template('2_identification.html')

@app.route("/key11")
def key():
    return render_template('3_sec_key.html')

#************************************************************************************************************************************************************
@app.route("/tlogin", methods = ['GET', 'POST'])
def tlogin():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'TID' in request.form and 'Password' in request.form:
        # Create variables for easy access
        TID = request.form['TID']
        Password = request.form['Password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM teacher_table WHERE tid = %s AND password = %s', (TID, Password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['tid'] = account['tid']
            session['t_firstname'] = account['t_firstname']
            session['t_lastname'] = account['t_lastname']
            session['t_email'] = account['t_email']
            session['t_mobno'] = account['t_mobno']
            session['t_sub'] = account['t_sub']
            # Redirect to home page
            return redirect(url_for('ta'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('4_teacher_login.html', msg=msg)


@app.route("/treg",methods = ['GET', 'POST'])
def treg():
    if (request.method == 'POST'):
        '''Add entry to the database'''
        tid = request.form.get('tid')
        password = request.form.get('pass')
        t_firstname = request.form.get('fn')
        t_lastname = request.form.get('ln')
        t_email = request.form.get('eid')
        t_mobno = request.form.get('mobno')
        t_sub = request.form.get('sub')

        entry = teacher_table(tid=tid, password=password, t_firstname=t_firstname, t_lastname=t_lastname,
                              t_email=t_email, t_mobno=t_mobno, t_sub=t_sub)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('tlogin'))

    else:
        return render_template('5_teacher_reg.html')


@app.route("/ta", methods = ['GET', 'POST'])
def ta():

    return render_template('6_acces_to_teacher.html', fname=session['t_firstname'])


@app.route("/tvp", methods = ['GET', 'POST'])
def tvp():
    # Check if user is loggedin
    tid = session['tid']
    if 'loggedin' in session:  # and (request.method != 'POST'):

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM teacher_table WHERE tid LIKE %s', [tid])
        # Fetch one record and return result
        taccount = cursor.fetchall()
        cursor.close()

        return render_template('teacher_view_profile.html', tdata=taccount)

        # If account exists in accounts table in out database
        # if saccount:
        # Create session data, we can access this data in other routes
        # session['loggedin'] = True
        # session['sid'] = saccount['sid']
        # session['fname'] = saccount['s_firstname']
        # session['lname'] = saccount['s_lastname']
        # session['semail'] = saccount['s_email']
        # session['smob'] = saccount['s_mobno']
        # session['sdob'] = saccount['s_dob']

    # return render_template('student_view_profile.html', sdata=saccount)

@app.route("/vd")
def vd():
    if 'loggedin' in session:
        # Check if account exists using MySQL
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM student_table")
        # Fetch one record and return result
        tsaccount = cursor.fetchall()
        cursor.close()
        return render_template('stud_details_taccess.html', sdata=tsaccount)
        # If account exists in accounts table in out database
        # if tsaccount:
            # Create session data, we can access this data in other routes
            # session['loggedin'] = True
            # sno = tsaccount[0]
            # sid = tsaccount[1]
            # Sfname = tsaccount[2]
            # Slname = tsaccount[3]
            # Semail = tsaccount[4]
            # Smob = tsaccount[5]
            # Sdob = tsaccount[6]

    # return render_template('stud_details_taccess.html', sno=session['sno'], sid=session['sid'], Sfname=session['Sfname'],
    #                        Slname=session['Slname'], Semail=session['Semail'], Smob=session['Smob'],
    #                        Sdob=session['Sdob'])


@app.route("/vds")
def vds():
    if 'loggedin' in session:
        # Check if account exists using MySQL
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM student_table")
        # Fetch one record and return result
        saccount = cursor.fetchall()
        cursor.close()
        return render_template('student_details_saccess.html', sdata=saccount)
        # If account exists in accounts table in out database
        # if tsaccount:
            # Create session data, we can access this data in other routes
            # session['loggedin'] = True
            # sno = tsaccount[0]
            # sid = tsaccount[1]
            # Sfname = tsaccount[2]
            # Slname = tsaccount[3]
            # Semail = tsaccount[4]
            # Smob = tsaccount[5]
            # Sdob = tsaccount[6]

    # return render_template('stud_details_taccess.html', sno=session['sno'], sid=session['sid'], Sfname=session['Sfname'],
    #                        Slname=session['Slname'], Semail=session['Semail'], Smob=session['Smob'],
    #                        Sdob=session['Sdob'])



@app.route("/ed2",methods = ['GET', 'POST'])
def ed2():
    tid= session['tid']
    tfname=session['t_firstname']
    tlname= session['t_lastname']
    temail= session['t_email']
    tmob= session['t_mobno']
    tsub= session['t_sub']

    # print(sdob)

    if (request.method == 'POST'):
        Ntfname = request.form['tfn']
        Ntlname = request.form['tln']
        Ntemail = request.form['temail']
        Ntmob = request.form['tmob']
        Ntsub = request.form['tsub']

        cursor = mysql.connection.cursor()
        cursor.execute("""
                        UPDATE teacher_table
                        SET t_firstname=%s, t_lastname=%s, t_email=%s, t_mobno=%s, t_sub=%s
                        WHERE tid=%s
                        """, (Ntfname, Ntlname, Ntemail, Ntmob, Ntsub, tid))
        mysql.connection.commit()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM teacher_table WHERE tid = %s', [tid])
        # Fetch one record and return result
        uaccount = cursor.fetchone()
        # If account exists in accounts table in out database
        if uaccount:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['tid'] = uaccount['tid']
            session['t_firstname'] = uaccount['t_firstname']
            session['t_lastname'] = uaccount['t_lastname']
            session['t_email'] = uaccount['t_email']
            session['t_mobno'] = uaccount['t_mobno']
            session['t_sub'] = uaccount['t_sub']

        cursor.close()
        return redirect(url_for('tvp'))
    else:
        return render_template('teditp.html', tid=tid, tfname=tfname, tlname=tlname, temail=temail, tmob=tmob,
                               tsub=tsub)


@app.route("/ads",methods = ['GET', 'POST'])
def ads():
    if (request.method == 'POST'):
        '''Add entry to the database'''
        sid = request.form.get('sid')
        student_name = request.form.get('sname')
        total_attendance = request.form.get('ta')
        # total_lectures = request.form.get('tl')
        status = 'verified'

        key='verified'

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT total_lectures FROM attendance WHERE status =%s", [key] )
        # Fetch one record and return result
        saccount = cursor.fetchone()
        # # If account exists in accounts table in out database
        # if saccount:
        #     # Create session data, we can access this data in other routes
        #     session['loggedin'] = True
        #     session['total_lectures'] = saccount['total_lectures']
        #
        #     total_lectures =  session['total_lectures']

        entry = Attendance(sid=sid, student_name=student_name, total_attendance=total_attendance,total_lectures = saccount, status=status)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('ta'))

    else:
        return render_template('addStudent.html')



@app.route("/vps", methods = ['GET', 'POST'])
def vps():
    if (request.method != 'POST'):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM attendance")
        # Fetch one record and return result
        attain = cursor.fetchall()
        cursor.close()
        return render_template('presenty_sheet.html', adata=attain)

    else:
        return render_template('presenty_sheet.html')


@app.route("/an",methods = ['GET', 'POST'])
def an():
    if (request.method == 'POST'):

        notice_no = request.form.get('nono')
        notice = request.form.get('eno')


        entry = notice_table(notice_no=notice_no, notice=notice)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('an'))

    else:
        return render_template('add_notice.html')

@app.route("/add/<string:id_data>",methods = ['GET', 'POST'])
def add(id_data):
    cursor = mysql.connection.cursor()
    cursor.execute("""
                    UPDATE attendance
                    SET total_attendance = total_attendance+1
                    WHERE sid=%s
                    """, (id_data))
    mysql.connection.commit()
    return redirect(url_for('vps'))

@app.route("/addTL",methods = ['GET', 'POST'])
def addTL():
    cursor = mysql.connection.cursor()
    cursor.execute("""
                    UPDATE attendance
                    SET total_lectures = total_lectures+1
                    WHERE status='verified'
                    """)
    mysql.connection.commit()
    return redirect(url_for('vps'))



#******************************************************************************************************************

@app.route("/slogin", methods = ['GET', 'POST'])
def slogin():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'SID' in request.form and 'Password' in request.form:
        # Create variables for easy access
        SID = request.form['SID']
        Password = request.form['Password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student_table WHERE sid = %s AND password = %s', (SID, Password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['sid'] = account['sid']
            session['s_firstname'] = account['s_firstname']
            session['s_lastname'] = account['s_lastname']
            session['s_email'] = account['s_email']
            session['s_mobno'] = account['s_mobno']
            session['s_dob'] = account['s_dob']
            # Redirect to home page
            return redirect(url_for('sa'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('7_student_login.html', msg=msg)

@app.route("/sreg", methods = ['GET', 'POST'])
def sreg():
    if (request.method == 'POST'):
        '''Add entry to the database'''
        sid = request.form.get('sid')
        password = request.form.get('pass')
        s_firstname = request.form.get('fn')
        s_lastname = request.form.get('ln')
        s_email = request.form.get('eid')
        s_mobno = request.form.get('mobno')
        s_dob = request.form.get('dob')

        entry = student_table(sid=sid,password=password,s_firstname=s_firstname,s_lastname=s_lastname, s_email=s_email, s_mobno=s_mobno,s_dob=s_dob)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('slogin'))

    else:
        return render_template('8_student_reg.html')




@app.route("/sa", methods = ['GET', 'POST'])
def sa():
    # Check if user is loggedin
    # if 'loggedin' in session and (request.method != 'POST'):
    #     sid = session['sid']
    #     # Check if account exists using MySQL
    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     cursor.execute('SELECT * FROM student_table WHERE sid = %s',(sid))
    #     # Fetch one record and return result
    #     saccount = cursor.fetchone()
    #     # If account exists in accounts table in out database
    #     if saccount:
    #         # Create session data, we can access this data in other routes
    #         session['loggedin'] = True
    #         session['sid'] = saccount['sid']
    #         session['fname'] = saccount['s_first_name']
    #         session['lname'] = saccount['s_last_name']
    #         session['semail'] = saccount['s_email']
    #         session['smob'] = saccount['s_mobno']
    #         session['sdob'] = saccount['s_dob']

    return render_template('9_access_to_student.html', fname=session['s_firstname'], sid=session['sid'])


@app.route("/ed1",methods = ['GET', 'POST'])
def ed1():
    sid = session['sid']
    sfname = session['s_firstname']
    slname = session['s_lastname']
    semail = session['s_email']
    smob = session['s_mobno']
    sdob = session['s_dob']

    # print(sdob)

    if (request.method == 'POST'):
        Nsfname = request.form['sfn']
        Nslname = request.form['sln']
        Nsemail = request.form['semail']
        Nsmob = request.form['smob']
        Nsdob = request.form['sdob']

        cursor = mysql.connection.cursor()
        cursor.execute("""
                    UPDATE student_table
                    SET s_firstname=%s, s_lastname=%s, s_email=%s, s_mobno=%s, s_dob=%s
                    WHERE sid=%s
                    """, (Nsfname, Nslname, Nsemail, Nsmob, Nsdob, sid))
        mysql.connection.commit()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student_table WHERE sid = %s',[sid] )
        # Fetch one record and return result
        uaccount = cursor.fetchone()
        # If account exists in accounts table in out database
        if uaccount:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['sid'] = uaccount['sid']
            session['s_firstname'] = uaccount['s_firstname']
            session['s_lastname'] = uaccount['s_lastname']
            session['s_email'] = uaccount['s_email']
            session['s_mobno'] = uaccount['s_mobno']
            session['s_dob'] = uaccount['s_dob']

        cursor.close()
        return redirect(url_for('svp'))
    else:
        return render_template('seditp.html', sid=sid, sfname=sfname, slname=slname, semail=semail, smob=smob, s_dob= sdob)


@app.route("/vtt")
def tt():
    return render_template('tt.html')

@app.route("/vaten", methods = ['GET', 'POST'])
def vaten():
    if 'loggedin' in session and (request.method != 'POST'):
        sid = (session['sid'])
        val = 0
        average_attain = 0
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM attendance WHERE sid LIKE %s ',[sid])
        # Fetch one record and return result
        staccount = cursor.fetchone()
        # If account exists in accounts table in out database
        if staccount:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['sid'] = staccount['sid']
            session['total_attendance'] = staccount['total_attendance']
            session['total_lectures'] = staccount['total_lectures']

            roll =session['sid']
            total_att=session['total_attendance']
            total_lect=session['total_lectures']


            val=(total_att/total_lect)*100

            average_attain=int(val)


    return render_template('view_attendance.html', average_attain=average_attain)

@app.route("/vin", methods = ['GET', 'POST'])
def vin():
    # Check if user is loggedin
    if 'loggedin' in session and (request.method != 'POST'):
        # notice_no = session['notice_no']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM notice_table")
        # Fetch one record and return result
        noticeall = cursor.fetchall()
        cursor.close()

    return render_template('imp_notice.html',  notice=noticeall)


@app.route("/svp", methods = ['GET', 'POST'])
def svp():
    # Check if user is loggedin
    sid = session['sid']
    if 'loggedin' in session :#and (request.method != 'POST'):

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM student_table WHERE sid LIKE %s',[sid])
        # Fetch one record and return result
        saccount = cursor.fetchall()
        cursor.close()

        return render_template('student_view_profile.html', sdata=saccount)

        # If account exists in accounts table in out database
        # if saccount:
            # Create session data, we can access this data in other routes
            # session['loggedin'] = True
            # session['sid'] = saccount['sid']
            # session['fname'] = saccount['s_firstname']
            # session['lname'] = saccount['s_lastname']
            # session['semail'] = saccount['s_email']
            # session['smob'] = saccount['s_mobno']
            # session['sdob'] = saccount['s_dob']

       # return render_template('student_view_profile.html', sdata=saccount)

#*****************************************************************************************************

if __name__=='__main__':
  app.run(debug="True")