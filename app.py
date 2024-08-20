from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

profiles = []

@app.route('/')
def index():
    return render_template('index.html', profiles=profiles)

@app.route('/profile/<int:profile_id>')
def profile(profile_id):
    profile = next((p for p in profiles if p['id'] == profile_id), None)
    if profile:
        return render_template('profile.html', profile=profile)
    return redirect(url_for('index'))

@app.route('/add_profile', methods=['GET', 'POST'])
def add_profile():
    if request.method == 'POST':
        new_profile = {
            'id': len(profiles) + 1,
            'name': request.form['name'],
            'email': request.form['email'],
            'bio': request.form['bio'],
            'profile_picture': None
        }
        
        
        profiles.append(new_profile)
        return redirect(url_for('profile', profile_id=new_profile['id']))
    
    return render_template('add_profile.html')

@app.route('/edit_profile/<int:profile_id>', methods=['GET', 'POST'])
def edit_profile(profile_id):
    profile = next((p for p in profiles if p['id'] == profile_id), None)
    if profile:
        if request.method == 'POST':
            profile['name'] = request.form['name']
            profile['email'] = request.form['email']
            profile['bio'] = request.form['bio']
            
            return redirect(url_for('profile', profile_id=profile_id))
        
        return render_template('edit_profile.html', profile=profile)
    return redirect(url_for('index'))

@app.route('/delete_profile/<int:profile_id>', methods=['POST'])
def delete_profile(profile_id):
    global profiles
    profiles = [p for p in profiles if p['id'] != profile_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
