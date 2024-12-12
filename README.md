# Github link
https://github.com/catalinamanolache/animal-adoption-center

# **Description**

This project is a website that helps an animal adoption center show animals
available for adoption. There are two main types of users: people who want to
adopt animals (they can look at the photos and see more information about the 
animals) and the admin(s) (it/they post(s) the announcements and manage the
current posts). The platform serves two primary user groups:

1. **Admins** - Admins manage the content, including animal profiles and
adoption updates, ensuring that the information remains current and accurate
2. **Users** - Users can view the animals available for adoption and adopt them

### _Home page_
This is the main page. It contains the logo and a button that leads to the
page with animals. The navigation bar is at the top of the page and has
the following links:
1. "Home"
2. "About",
3. "Sign up"
4. "Login"
5. "Upload" (visible after the user is logged in)
6. "Log out" (visible after the user is logged in)

### _About page_
It contains a brief description of the animal adoption center, the values that
are promoted and some of the animals that were adopted.

### _Sign up page_
This page is for people who want to adopt animals. They can create an account
by filling in the form with their personal information that will be saved in
the database. 

Form fields:
1. Username
2. Email
3. Password

### _Login page_
This page is for people who already have an account. They can log in by
filling in the form with their username and password. They will be logged as
admins or users, depending on the account type.

### _Animals page_
This page contains the photos of the animals that are available for adoption.
It also presents a short description, the name, age and the animals' category.
The search bar helps the users find the animals sorted by category.

### _Logout page_
This button logs out the users and redirects them to the home page.

### _Upload page_
This page is for the admins. They can upload the animals that are available
for adoption by filling in the form with the animals' information.

Form fields:
1. Animal Name
2. Animal Age
3. Animal Type
4. Animal Description
5. Animal Image


# **Functionalities**
- as an admin, you can upload animals, edit and delete them
- as an user, you can see the animals available for adoption and adopt them
- after an animal is adopted, it will be deleted from the website
- the users can search for animals by category

# **Technologies**
- for the front-end we used HTML, CSS and Bootstrap
- for the backend we used python, flask and SQLAlchemy

# **Team roles**
Main tasks:
- Manolache Maria Catalina - database for users, css design
- Diaconescu Stefania Clara - html pages, css design
- Farcasanu Bianca Ioana - database for animals, css design

Even if those were the main responsibilities, each member contributed to both
front-end and back-end development and helped each other to solve the problems
that appeared during the project.

The main problems were caused by the database. For example the users appeared
as logged in even if they were not. This was solved by changing the users'
model in the users' database.
When the animals were uploaded, the images were not displayed. We realised the
problem appeared because of the place where the photos were uploaded. This was
solved by changing the path of the images in the database.
The buttons for signing up, logging in and logging out were displayed even if
the user was connected or not. This was solved by using conditional variables that
were updated when the user logged in or out.
The navigation bar didn't work when the browser was resized. This was solved by
using Bootstrap's responsive design features.
