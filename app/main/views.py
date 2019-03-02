
from flask_login import login_user,logout_user,login_required
from flask import render_template,request,flash,redirect,url_for,abort
from ..models import  User
from flask_login import login_required,current_user
from . import main
from .forms import  PitchForm, CommentForm
from ..models import User,Pitches, Comments
from flask_login import login_user
from .. import db,photos

from .forms import UpdateProfile

# Views
@main.route('/')
def index():
      all_pitches = Pitches.get_pitches()
      title = 'Home - Welcome to The best Movie Review Website Online'
      return render_template('index.html', title = title , all_pitches=all_pitches)


@main.route('/newpitch/',methods = ['GET','POST'])
@login_required
def newpitch():

    form = PitchForm()
  
    if form.validate_on_submit():
       
        pitch= form.pitch.data

        # Updated review instance
        newpitch = Pitches(pitches = pitch ,user_id=current_user.id)

        # save review method
        newpitch.save_pitch()
        return redirect(url_for('.index',pitch = pitch))

   
    return render_template('newpitch.html',newpitch=form)











@main.route('/comment/new/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    description_form = CommentForm()

    pitch = Pitches.query.get(id)

    if description_form.validate_on_submit():
       
        comment = description_form.comment.data
        new_comment = Comments(comment=comment,user_id=current_user.id,pitch_id = pitch.id )
        new_comment.save_comments() 
        return redirect(url_for('main.index'))
    return render_template('comment.html',description_form=description_form)





@main.route('/pitch/<int:id>')
def single_pitch(id):
    pitch=Pitches.query.filter_by(id=id).first()
    comments=Comments.query.filter_by(pitch_id=id).all()
    return render_template('pitch.html',pitch=pitch,comments=comments)





@main.route('/downvotes/<int:id>')
def upvoting(id):
    pitch1=Pitch.query.filter_by(id=id).first()
    pitch1.upvotes=Pitch.upvote(id)
    return redirect(url_for('main.single_pitch',pitch=pitch1.upvotes))









@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)  




@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))  



