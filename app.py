from flask import Flask, render_template, flash, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet

from forms import AddPetForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "pugsrcool24"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///pets_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["DEBUG_TB_INTERCEPT_DIRECTS"] = False

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def homepage():
    """Show homepage"""
    pets = Pet.query.all()
    return render_template("home.html", pets=pets)

@app.route("/add", methods=["GET","POST"])
def add_pet_form():
    """Show add pet form"""
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        if form.photo_url.data:
            photo_url = form.photo_url.data
        else:
            photo_url = "/static/images/nopic.jpg"
        age = form.age.data
        notes = form.notes.data
        available = form.available.data

        new_pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes, available=available)
        db.session.add(new_pet)
        db.session.commit()
        flash(f'New pet added: {name}!')
        return redirect('/')
    else:
        return render_template("addpetform.html", form=form)

@app.route("/pets/<int:pet_id>")
def show_pet_page(pet_id):
    """this page will show details about pet"""
    pet = Pet.query.get_or_404(pet_id)
    return render_template("pet.html", pet=pet)

@app.route("/pets/<int:pet_id>/delete", methods=["POST"])
def delete_pet(pet_id):
    """this will delete a pet, and redirect to home page"""
    pet = Pet.query.get_or_404(pet_id)
    Pet.query.filter_by(id = pet_id).delete()
    db.session.commit()
    flash(f'Pet {pet.name} removed.')
    return redirect("/")

@app.route("/pets/<int:pet_id>/edit", methods=["GET","POST"])
def edit_pet(pet_id):
    """this will edit pet with supplied info"""
    pet = Pet.query.get_or_404(pet_id)
    form = AddPetForm(obj=pet)
    
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        if pet.photo_url:
            pet.photo_url = form.photo_url.data
        pet.age = form.age.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()
        flash(f'Pet {pet.name} was edited successfully.')
        return redirect("/")
    else:
        return render_template("edit.html", pet=pet, form=form)