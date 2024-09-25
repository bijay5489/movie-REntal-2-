Project: BrickSmasher - Movie Rental Management System
Overview:
A Django-based system that manages VHS movie rentals for a revived movie rental chain, BrickSmasher. Employees can create accounts, manage movie inventory, and handle rentals/returns.

Pages:
Home (""): Menu with links to Account Creation, Manage Movies, and Rent/Return Movies.
Account Creation ("account/"):
Form to create user accounts (first name, last name, and unique email). Displays error for duplicate email.
Manage Movies ("movie/"):
Displays a table of movies with options to add/remove stock. Also allows adding new movies to the inventory.
Rent/Return Movies ("rent/"):
Allows users to check out or return movies. Users can only check out a maximum of 3 movies at a time and one copy per movie.
AJAX Paths:
Manage Users ("dbUser/"):
Handles user creation and retrieval.
Manage Movies ("dbMovie/"):
Manages movie inventory with actions: "new", "add", and "remove".
Manage Rentals ("dbRent/"):
Handles movie rentals and returns for users.
Database Structure:
Users table: Stores user details.
Movies table: Stores movie inventory.
Checkouts table: Links users to rented movies.
