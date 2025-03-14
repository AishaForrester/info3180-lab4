import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import UserProfile
from app.forms import LoginForm
from app.forms import UploadForm
from werkzeug.security import check_password_hash
from flask import Flask, send_from_directory


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@login_required
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    # Instantiate your form class
    form = UploadForm()

        # Validate file upload on submit

        #if the user is submiting a form and the form is valid
    if request.method == 'POST' and form.validate_on_submit(): 
        # Get file data and save to your uploads folder
        file=form.imagefile.data #getting the file data (image)
        filename = secure_filename(file.filename)
        #we would get something like this: uploads/filename.jpg
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        flash('File Saved', 'success')
        return redirect(url_for('home')) # Update this to redirect the user to a route that displays all uploaded image files

    return render_template('upload.html', form=form)


#Exercise 6 functions

def get_uploaded_images():
    image_list = []
    rootdir = os.path.abspath(app.config['UPLOAD_FOLDER']) #move up one folder  
    print("checking directory:", rootdir)

    for subdir, dirs, files in os.walk(rootdir):  #walk through the directory
        print("currently in:", subdir) 
        for file in files:
            print("Found file:", file)
            if file.lower().endswith(('.jpg', '.png', '.jpeg', '.gif')):
                image_list.append(file)    # file name 
    return image_list

@app.route('/uploads/<filename>')
def get_image(filename):

    """Return a specific image from the uploads folder."""
    print(app.config['UPLOAD_FOLDER'])
    
    return send_from_directory(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)

    

@app.route('/files', methods=['POST', 'GET'])
def files():
    images = get_uploaded_images()
    print(images)
    return render_template("files.html", images=images)
#end 


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    # change this to actually validate the entire form submission
    # and not just one field
    if form.validate_on_submit():
        # Get the username and password values from the form.
        username = form.username.data
        password = form.password.data

        # Using your model, query database for a user based on the username
        # and password submitted. Remember you need to compare the password hash.
        # You will need to import the appropriate function to do so.
        # Then store the result of that query to a `user` variable so it can be
        # passed to the login_user() method below.
        user = db.session.execute(db.select(UserProfile).filter_by(username=username)).scalar()
        if user and check_password_hash(user.password, password):
            login_user(user) #log the user in using Flask-Login
            flash('Logged in successfully.', 'success')
            return redirect(url_for("upload"))  # The user should be redirected to the upload form instead
        else:
            flash('Username or Password is incorrect.', 'danger')


               
        
    return render_template("login.html", form=form)

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()

###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
