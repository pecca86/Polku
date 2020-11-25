# Project kirjuri

## DEPENDENCIES:
- Django 3.0.3
- Misaka 2.1.0
- jQuery
- django-bootstrap3
- django-bootstrap4
- pip install django-cors-headers
- django-braces
- pip install django-utils-six
- functional.py -> from toolz import curry
- pip install django-betterforms
- Charts.js

## TODO:
- Juttu:
	- Add yhteenveto view
	- IT-tutkijan määrittäminen jutulle
	- Valikko mistä voi valita IT-tutkijan
	- Alert tjsp kun avaat jutun missä ei ole IT-tutkijaa
	- Teon kuvaus
	- Kiinnostavat sovellukset
- Laite:
	- 	
- Other
	- Filters
	
### Update history:
- Added juttu foreign key to laite
- User can now create a laite & add it to a specific juttu /20.7
- User can see a list of all laitteet /20.7
- User can now create two identical juttus, slug differs them by pk id /21.7
- Laite List view updated -> Can now select a specific laite -> get into detail view -> update the laite details /22.7
- Changed models.Juttu to reverse single juttu slug
- JuttuDetail can now show a correct queryset of devices belonging to the juttu
- All the laitteet are now presented correctly inside juttu /27.7
- Return user to kaikki laitteet view after deleting a laite (change this at some point to juttu_detail) /27.7
- Juttu_detail contains links to all the laitteet
- Added static css and js functionality /28.7
- Show & hide laite details inside juttu_detail using javascript /30.7.
- Canceling the deletion of a laite return the user to the corresponding juttu_detail view /31.7
- Muokkaa laite returns to the juttu_detail view of the laite /31.7
- Delete laite returns to the juttu_detail of the laite /31.7
- Changed everything to work with int:pk instead of slug /31.7
- Creating a new laite returns the user back to the juttu_Detail of the laite /31.7
- Updated readme to show correct dependencies /3.8
- Inserted a javascript cancle button when adding a new device that redirect back to previous screen /3.8	
- Created a view that passes in pk to next view /3.8
- Automatically adds a new laite to the corresponding juttu /4.8
- Shows in juttu list if kiireellinen /4.8	
- Added juttu status, still need to add place where to change it /4.8.
- Navbar sticky-top /6.8
- User now able to update juttu_status directly from juttu_detail view /10.8
- Added laite_status options to laite /10.8


### Thoughts

- Best way to display laite inside juttu_detail?

### Next up:

- Update laite status from juttu_detail

### Helpful links:
- https://stackoverflow.com/questions/45659986/django-implementing-a-form-within-a-generic-detailview
- https://docs.djangoproject.com/en/3.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin
