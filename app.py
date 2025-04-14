from flask import Flask, render_template, request, redirect, url_for, session, flash
from wtforms import Form, StringField, PasswordField, validators, IntegerField, SelectField, DecimalField, SubmitField, DateField, BooleanField, DateTimeField, HiddenField
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
import datetime




app = Flask(__name__)
app.secret_key = "supersecretkey"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'fms2'


# Database Connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(host=app.config['MYSQL_HOST'], user=app.config['MYSQL_USER'], password=app.config['MYSQL_PASSWORD'], database=app.config['MYSQL_DB'])
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None




# Forms-------------------------------------------------------------------------------------------------------------------------------

class SignupForm(FlaskForm):
    name = StringField("Name", [validators.InputRequired(), validators.Length(min=3, max=100)])
    email = StringField("Email", [validators.InputRequired(), validators.Email()])
    address = StringField("Address", [validators.InputRequired(), validators.Length(min=5, max=255)])
    age = IntegerField("Age", [validators.InputRequired(), validators.NumberRange(min=18, max=100)])
    sex = SelectField("Sex", choices=[('M', 'Male'), ('F', 'Female'), ('Other', 'Other')])
    contacts = StringField("Contacts", [validators.InputRequired(), validators.Length(min=10, max=50)])
    password = PasswordField("Password", [validators.InputRequired(), validators.Length(min=6)])
    confirm_password = PasswordField("Confirm Password", [validators.InputRequired(), validators.EqualTo("password", message="Passwords must match")])
    
# Login Form
class LoginForm(FlaskForm):
    email = StringField("Email", [validators.InputRequired(), validators.Email()])
    password = PasswordField("Password", [validators.InputRequired()])

# Update profile form
class EditProfile(FlaskForm):
    name = StringField("Name", [validators.InputRequired(), validators.Length(min=3, max=100)])
    email = StringField("Email", [validators.InputRequired(), validators.Email()])
    address = StringField("Address", [validators.InputRequired(), validators.Length(min=5, max=255)])
    age = IntegerField("Age", [validators.InputRequired(), validators.NumberRange(min=18, max=100)])
    sex = SelectField("Sex", choices=[('M', 'Male'), ('F', 'Female'), ('Other', 'Other')])
    contacts = StringField("Contacts", [validators.InputRequired(), validators.Length(min=10, max=50)])

# Search Flight Form
class FlightSearchForm(FlaskForm):
    from_airport = SelectField('From Airport', choices=[], validators=[validators.Optional()])
    to_airport = SelectField('To Airport', choices=[], validators=[validators.Optional()])
    max_price = DecimalField('Max Price', validators=[validators.Optional()])
    departure_date = DateField('Departure After', format='%Y-%m-%d', validators=[validators.Optional()])
    arrival_date = DateField('Arrival Before', format='%Y-%m-%d', validators=[validators.Optional()])
    submit = SubmitField('Search')

#Transaction Form
class TransactionForm(FlaskForm):
    submit = SubmitField("Confirm & Pay")

# Admin Login Form
class AdminLoginForm(FlaskForm):
    email = StringField("Email", validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    submit = SubmitField("Login")

#Add admin form
class AddAdminForm(FlaskForm):
    name = StringField('Full Name', validators=[validators.DataRequired(), validators.Length(min=2, max=100)])
    email = StringField('Email Address', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Dummy Password', validators=[validators.DataRequired(), validators.Length(min=4)])
    is_super = BooleanField('Grant Super Admin Privileges')
    submit = SubmitField('Add Admin')

# Add new airplane form
class AirplaneTypeForm(FlaskForm):
    A_ID = StringField("Airplane ID", validators=[validators.DataRequired(), validators.Length(max=10)])
    Capacity = IntegerField("Capacity", validators=[validators.DataRequired(), validators.NumberRange(min=1)])
    A_weight = DecimalField("Airplane Weight (kg)", places=2, validators=[validators.DataRequired(), validators.NumberRange(min=100000)])
    Company = StringField("Company", validators=[validators.DataRequired(), validators.Length(max=100)])
    submit = SubmitField("Add Airplane Type")

#Add Country form
class CountryForm(FlaskForm):
    country_code = StringField('Country Code', validators=[validators.DataRequired(), validators.Length(min=2, max=3)])
    country_name = StringField('Country Name', validators=[validators.DataRequired(), validators.Length(max=100)])
    submit = SubmitField('Add Country')


# Add Airport Form
class AirportForm(FlaskForm):
    air_code = StringField('Airport Code', validators=[validators.DataRequired(), validators.Length(max=5)])
    air_name = StringField('Airport Name', validators=[validators.DataRequired(), validators.Length(max=100)])
    city = StringField('City', validators=[validators.DataRequired(), validators.Length(max=50)])
    country_code = SelectField('Country Code', choices=[], validators=[validators.DataRequired()])
    submit = SubmitField('Add Airport')


# Add Flight Form
class FlightForm(FlaskForm):
    departure = DateTimeField('Departure (YYYY-MM-DD HH:MM:SS)', format='%Y-%m-%d %H:%M:%S', validators=[validators.DataRequired()])
    arrival = DateTimeField('Arrival (YYYY-MM-DD HH:MM:SS)', format='%Y-%m-%d %H:%M:%S', validators=[validators.DataRequired()])
    fare_amount = DecimalField('Fare Amount', validators=[validators.DataRequired()])
    a_id = SelectField('Airplane Type', choices=[], validators=[validators.DataRequired()])
    starting_airport = SelectField('Starting Airport', choices=[], validators=[validators.DataRequired()])
    ending_airport = SelectField('Ending Airport', choices=[], validators=[validators.DataRequired()])
    remaining_seats = HiddenField('Remaining Seats')
    submit = SubmitField('Add Flight')

# Routes-------------------------------------------------------------------------------------------------------------------------------

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


# Passenger Routes-------------------------------------------------------------------------------------------------------------------------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm(request.form)
    if request.method == "POST" and form.validate():
        # Get form data
        name = form.name.data
        email = form.email.data
        address = form.address.data
        age = form.age.data
        sex = form.sex.data
        contacts = form.contacts.data
        password = form.password.data
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO passenger (name, email, address, age, sex, contacts, password) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, email, address, age, sex, contacts, password))
                conn.commit()
                conn.close()
                flash(f"Signup successful for {name}. You can now log in.", "success")
                return redirect(url_for("login"))
            except mysql.connector.Error as err:
                flash(f"Error: {err}", "danger")
            finally:
                conn.close()
        

    return render_template("signup.html", form=form)



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        email = form.email.data
        password = form.password.data  # Here you would check credentials in a real app

        # getting user from database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("select * from passenger where email=%s",([email]))
        user = cursor.fetchone()
        conn.close()

        # Authenticate user and create session
        if user and user[7] == password:
            session["user_id"] = user[0]
            return redirect(url_for("passenger_dashboard"))
        else:
            flash("Login failed! Please check your email and password","danger")
            return redirect(url_for("login"))
        

    return render_template("login.html", form=form)



@app.route("/passenger_dashboard", methods=["GET", "POST"])
def passenger_dashboard():
    if "user_id" in session:
        user_id = session["user_id"]

        #Getting user from database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("select * from passenger where ps_id=%s",([user_id]))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return render_template("passenger_dashboard.html", user=user)
 
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have logged out successfully", "info")
    return redirect(url_for("login"))


@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        flash("You must be logged in to edit your profile.", "danger")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch user details
    cursor.execute("SELECT * FROM passenger WHERE ps_id = %s", (user_id,))
    user = cursor.fetchone()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("passenger_dashboard"))

    form = EditProfile(request.form)
    print(user)

    # Pre-fill the form with current user data
    if request.method == "GET":
        form.name.data = user['Name']
        form.email.data = user["Email"]
        form.address.data = user["Address"]
        form.age.data = user["Age"]
        form.sex.data = user["Sex"]
        form.contacts.data = user["Contacts"]
        print("prefill")

    #Update database when form is submitted
    if request.method == "POST" and form.validate():
        # Get form data
        name = form.name.data
        email = form.email.data
        address = form.address.data
        age = form.age.data
        sex = form.sex.data
        contacts = form.contacts.data

        print("done")
        conn = get_db_connection()
        cursor = conn.cursor()
    
        # Update user details including password
        update_query = """
            UPDATE passenger
            SET name=%s, email=%s, address=%s, age=%s, sex=%s, contacts=%s
            WHERE ps_id=%s
        """
        cursor.execute(update_query, (name, email, address, age, sex, contacts, user_id))

        conn.commit()
        conn.close()
        flash("Profile successfully updated!", "success")
        return redirect(url_for("edit_profile"))
        
    return render_template("edit_profile.html", user=user, form=form)



@app.route("/book_flight", methods=["GET", "POST"])
def book_flight():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT Air_Code, Air_Name, City FROM Airport ORDER BY City")
    airport_list = cursor.fetchall()

    airport_choices = [('', '-- All --')] + [(a["Air_Code"], f"{a['Air_Name']} ({a['City']})") for a in airport_list]

    form = FlightSearchForm(request.args)
    form.from_airport.choices = airport_choices
    form.to_airport.choices = airport_choices

    query = """
        SELECT 
            f.Flight_ID, f.Departure, f.Arrival, f.Fare_Amount, f.Remaining_Seats,
            ap.Company,
            a1.Air_Name AS From_Name, a1.City AS From_City,
            a2.Air_Name AS To_Name, a2.City AS To_City
        FROM Flight f
        JOIN Airplane_Type ap ON f.A_ID = ap.A_ID
        JOIN Airport a1 ON f.Starting_Airport = a1.Air_Code
        JOIN Airport a2 ON f.Ending_Airport = a2.Air_Code
        WHERE f.Departure > NOW()
    """

    filters = []
    params = []

    if form.from_airport.data:
        filters.append("a1.Air_Code = %s")
        params.append(form.from_airport.data)

    if form.to_airport.data:
        filters.append("a2.Air_Code = %s")
        params.append(form.to_airport.data)

    if form.max_price.data:
        filters.append("f.Fare_Amount <= %s")
        params.append(form.max_price.data)

    if form.departure_date.data:
        filters.append("DATE(f.Departure) >= %s")
        params.append(form.departure_date.data)

    if form.arrival_date.data:
        filters.append("DATE(f.Arrival) <= %s")
        params.append(form.arrival_date.data)

    if filters:
        query += " AND " + " AND ".join(filters)
    else:
        query += " ORDER BY f.Departure"

    cursor.execute(query, tuple(params))
    flights = cursor.fetchall()
    print(flights)

    conn.close()

    return render_template("book_flight.html", form=form, flights=flights)



@app.route("/book/<int:flight_id>", methods=["GET", "POST"])
def transaction(flight_id):
    if "user_id" not in session:
        flash("You must be logged in to book a flight.", "danger")
        return redirect(url_for("login"))

    user_id = session["user_id"]  # Assuming user_id maps to Ps_ID
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    form = TransactionForm()

    # Fetch flight details
    cursor.execute("""
        SELECT 
            f.Flight_ID, f.Departure, f.Arrival, f.Fare_Amount, f.Remaining_Seats,
            ap.Company,
            a1.Air_Name AS From_Name, a1.City AS From_City,
            a2.Air_Name AS To_Name, a2.City AS To_City
        FROM Flight f
        JOIN Airplane_Type ap ON f.A_ID = ap.A_ID
        JOIN Airport a1 ON f.Starting_Airport = a1.Air_Code
        JOIN Airport a2 ON f.Ending_Airport = a2.Air_Code
        WHERE f.Flight_ID = %s
    """, (flight_id,))
    flight = cursor.fetchone()

    if not flight:
        flash("Flight not found.", "danger")
        return redirect(url_for("book_flight"))

    if request.method == "POST" and form.validate_on_submit():
        if flight['Remaining_Seats'] <= 0:
            flash("No seats available for this flight.", "danger")
            return redirect(url_for("book_flight"))

        # Insert transaction
        cursor.execute("""
            INSERT INTO Transactions (Transaction_Date, Amount, Ps_ID, Flight_ID)
            VALUES (%s, %s, %s, %s)
        """, (datetime.datetime.now(), flight["Fare_Amount"], user_id, flight_id))
        
        conn.commit()
        conn.close()
        flash("Booking successful!", "success")
        return redirect(url_for("passenger_dashboard"))  # Update as needed

    conn.close()
    return render_template("transaction.html", flight=flight, form=form)


@app.route("/my_bookings", methods=["GET", "POST"])
def my_bookings():
    if "user_id" not in session:
        flash("You must be logged in to view your bookings.", "danger")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Handle cancellation
    if request.method == "POST":
        ts_id = request.form.get("ts_id")
        flight_id = request.form.get("flight_id")

        # Delete transaction
        cursor.execute("DELETE FROM Transactions WHERE TS_ID = %s AND Ps_ID = %s", (ts_id, user_id))

        # Increment remaining seats
        cursor.execute("UPDATE Flight SET Remaining_Seats = Remaining_Seats + 1 WHERE Flight_ID = %s", (flight_id,))

        conn.commit()
        flash("Booking cancelled successfully.", "success")
        return redirect(url_for("my_bookings"))

    query = """
    SELECT 
        t.TS_ID, t.Transaction_Date, t.Amount,
        f.Flight_ID, f.Departure, f.Arrival, f.Fare_Amount,
        ap.Company,
        a1.Air_Name AS From_Name, a1.City AS From_City,
        a2.Air_Name AS To_Name, a2.City AS To_City
    FROM Transactions t
    JOIN Flight f ON t.Flight_ID = f.Flight_ID
    JOIN Airplane_Type ap ON f.A_ID = ap.A_ID
    JOIN Airport a1 ON f.Starting_Airport = a1.Air_Code
    JOIN Airport a2 ON f.Ending_Airport = a2.Air_Code
    WHERE t.Ps_ID = %s
    ORDER BY f.Departure ASC
    """
    cursor.execute(query, (user_id,))
    bookings = cursor.fetchall()
    conn.close()

    # Split into upcoming and completed based on current time
    now = datetime.datetime.now()
    upcoming_flights = [b for b in bookings if b['Departure'] > now]
    completed_flights = [b for b in bookings if b['Departure'] <= now]

    return render_template("my_bookings.html", upcoming=upcoming_flights, completed=completed_flights)


# End Passenger Routes-------------------------------------------------------------------------------------------------------------------------------



# Admin Routes-------------------------------------------------------------------------------------------------------------------------------


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Admins WHERE Email = %s", (email,))
        admin = cursor.fetchone()
        conn.close()

        print(admin)

        if admin and admin["Email"] == email:
            # For now we're using plaintext password comparison (update later for security)
            if password == admin["Password"]:  # Replace with real password check
                session["admin_id"] = admin["Admin_ID"]
                session["is_superadmin"] = admin["Is_SuperAdmin"]
                flash("Logged in successfully!", "success")
                return redirect(url_for("admin_dashboard"))
            else:
                flash("Incorrect password!", "danger")
        else:
            flash("Admin not found!", "danger")
    return render_template("admin_login.html", form=form)


@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'danger')
        return redirect(url_for('admin_login'))  # Adjust if your login route is different

    # Fetch admin info from DB if needed
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admins WHERE admin_id = %s", (session["admin_id"],))
    admin = cursor.fetchone()
    conn.close()

    return render_template('admin_dashboard.html', admin=admin)


@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('admin_login'))  



@app.route('/admin/manage_admins', methods=['GET', 'POST'])
def manage_admins():

    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'danger')
        return redirect(url_for('admin_login'))
    
    form = AddAdminForm()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Handle deletion
    if request.method == 'POST' and 'delete_admin_id' in request.form:
        delete_id = request.form['delete_admin_id']
        try:
            cursor.execute("DELETE FROM admins WHERE admin_id = %s", (delete_id,))
            conn.commit()
            flash("Admin deleted successfully.", "success")
        except Exception as e:
            print(e)
            flash("Error deleting admin.", "danger")
        return redirect(url_for('manage_admins'))

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data  # You can hash it if needed
        is_super = form.is_super.data

        try:
            cursor.execute("""
                INSERT INTO admins (name, email, password, is_superadmin)
                VALUES (%s, %s, %s, %s)
            """, (name, email, password, int(is_super)))
            conn.commit()
            flash('New admin added successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')

        return redirect(url_for('manage_admins'))

    cursor.execute("SELECT admin_id, name, email, is_superadmin FROM admins")
    admins = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('manage_admins.html', form=form, admins=admins)



@app.route('/admin/manage_airplanes', methods=['GET', 'POST'])
def manage_airplanes():

    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'danger')
        return redirect(url_for('admin_login'))
    
    form = AirplaneTypeForm()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if form.validate_on_submit():
        try:
            cursor.execute("""
                INSERT INTO Airplane_Type (A_ID, Capacity, A_weight, Company)
                VALUES (%s, %s, %s, %s)
            """, (form.A_ID.data, form.Capacity.data, form.A_weight.data, form.Company.data))
            conn.commit()
            flash("Airplane type added successfully!", "success")
            return redirect(url_for('manage_airplanes'))
        except Exception as e:
            print("Error:", e)
            flash("An error occurred while adding airplane type.", "danger")

    # Fetch all airplane types
    cursor.execute("SELECT * FROM Airplane_Type ORDER BY Capacity DESC")
    airplane_types = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("manage_airplanes.html", form=form, airplane_types=airplane_types)


@app.route('/admin/manage_countries', methods=['GET', 'POST'])
def manage_countries():
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'danger')
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    form = CountryForm()

    if form.validate_on_submit():
        country_code = form.country_code.data.upper()
        country_name = form.country_name.data.title()

        try:
            cursor.execute("INSERT INTO Countries (Country_code, Country_Name) VALUES (%s, %s)", (country_code, country_name))
            conn.commit()
            flash('Country added successfully!', 'success')
            return redirect(url_for('manage_countries'))
        except mysql.connector.IntegrityError:
            flash('Country with this code already exists.', 'warning')

    cursor.execute("SELECT * FROM Countries ORDER BY Country_Name")
    countries = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('manage_countries.html', countries=countries, form=form)


@app.route('/admin/view_passengers')
def view_passengers():
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'danger')
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT Ps_ID, Name, Address, Age, Sex, Contacts, Email FROM Passenger ORDER BY PS_ID")
    passengers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('view_passengers.html', passengers=passengers)


@app.route('/admin/manage_airports', methods=['GET', 'POST'])
def manage_airports():
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'danger')
        return redirect(url_for('admin_login'))

    form = AirportForm()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Populate dropdown
    cursor.execute("SELECT Country_code FROM Countries")
    countries = cursor.fetchall()
    form.country_code.choices = [(c['Country_code'], c['Country_code']) for c in countries]

    # Handle airport addition
    if form.validate_on_submit():
        try:
            cursor.execute("""
                INSERT INTO Airport (Air_Code, Air_Name, City, Country_code)
                VALUES (%s, %s, %s, %s)
            """, (form.air_code.data, form.air_name.data, form.city.data, form.country_code.data))
            conn.commit()
            flash('Airport added successfully!', 'success')
            return redirect(url_for('manage_airports'))
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')

    # Handle deletion
    if request.method == 'POST' and 'delete_airport_code' in request.form:
        delete_code = request.form.get('delete_airport_code')

        # Check if the airport is used in any flight
        cursor.execute("""
            SELECT COUNT(*) AS count FROM Flight
            WHERE Starting_Airport = %s OR Ending_Airport = %s
        """, (delete_code, delete_code))
        usage = cursor.fetchone()
        
        if usage['count'] > 0:
            flash(f"Cannot delete airport '{delete_code}': it is used in one or more flights.", 'danger')
        else:
            try:
                cursor.execute("DELETE FROM Airport WHERE Air_Code = %s", (delete_code,))
                conn.commit()
                flash(f"Airport '{delete_code}' deleted successfully.", 'success')
                return redirect(url_for('manage_airports'))
            except Exception as e:
                conn.rollback()
                flash(f'Error deleting airport: {str(e)}', 'danger')

    # View all airports
    cursor.execute("SELECT * FROM Airport")
    airports = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('manage_airports.html', form=form, airports=airports)



@app.route('/admin/view_transactions')
def view_transactions():
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'danger')
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Pagination setup
    tx_page = int(request.args.get('tx_page', 1))
    rev_page = int(request.args.get('rev_page', 1))
    per_page = 10
    offset_tx = (tx_page - 1) * per_page
    offset_rev = (rev_page - 1) * per_page

    # Total transactions count
    cursor.execute("SELECT COUNT(*) AS count FROM Transactions")
    total_tx = cursor.fetchone()['count']

    # Paginated Transactions
    cursor.execute("""
        SELECT t.TS_ID, t.Transaction_Date, t.Amount, 
               p.Name AS Passenger_Name, f.Flight_ID
        FROM Transactions t
        JOIN Passenger p ON t.Ps_ID = p.Ps_ID
        JOIN Flight f ON t.Flight_ID = f.Flight_ID
        ORDER BY t.Transaction_Date DESC
        LIMIT %s OFFSET %s
    """, (per_page, offset_tx))
    transactions = cursor.fetchall()

    # Total unique passengers with transactions
    cursor.execute("SELECT COUNT(DISTINCT Ps_ID) AS count FROM Transactions")
    total_passengers = cursor.fetchone()['count']

    # Revenue per passenger (paginated)
    cursor.execute("""
        SELECT p.Ps_ID, p.Name, SUM(t.Amount) AS total_spent
        FROM Transactions t
        JOIN Passenger p ON t.Ps_ID = p.Ps_ID
        GROUP BY p.Ps_ID
        ORDER BY total_spent DESC
        LIMIT %s OFFSET %s
    """, (per_page, offset_rev))
    revenue_by_passenger = cursor.fetchall()

    # Overall revenue
    cursor.execute("SELECT SUM(Amount) AS overall_revenue FROM Transactions")
    overall_revenue = cursor.fetchone()['overall_revenue'] or 0.00

    cursor.close()
    conn.close()

    return render_template(
        'view_transactions.html',
        transactions=transactions,
        revenue_by_passenger=revenue_by_passenger,
        overall_revenue=overall_revenue,
        tx_page=tx_page,
        tx_pages=(total_tx + per_page - 1) // per_page,
        rev_page=rev_page,
        rev_pages=(total_passengers + per_page - 1) // per_page
    )



@app.route('/admin/manage_flights', methods=['GET', 'POST'])
def manage_flights():
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'danger')
        return redirect(url_for('admin_login'))

    form = FlightForm()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Populate dropdowns with existing foreign key values
    cursor.execute("SELECT A_ID FROM Airplane_Type")
    airplanes = cursor.fetchall()
    form.a_id.choices = [(a['A_ID'], a['A_ID']) for a in airplanes]

    cursor.execute("SELECT Air_Code FROM Airport")
    airports = cursor.fetchall()
    airport_choices = [(a['Air_Code'], a['Air_Code']) for a in airports]
    form.starting_airport.choices = airport_choices
    form.ending_airport.choices = airport_choices

    # Handle form submission
    if form.validate_on_submit():
        try:
            cursor.execute("SELECT Capacity FROM Airplane_Type WHERE A_ID = %s", (form.a_id.data,))
            airplane = cursor.fetchone()
            if not airplane:
                raise Exception("Invalid Airplane Type selected.")
            capacity = airplane['Capacity']

            cursor.execute("""
                INSERT INTO Flight (Departure, Arrival, Fare_Amount, A_ID, Starting_Airport, Ending_Airport, Remaining_Seats)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                form.departure.data, form.arrival.data, form.fare_amount.data,
                form.a_id.data, form.starting_airport.data, form.ending_airport.data,
                capacity
            ))
            conn.commit()
            flash('Flight added successfully!', 'success')
            return redirect(url_for('manage_flights'))
        except Exception as e:
            conn.rollback()
            flash(f'Error adding flight: {str(e)}', 'danger')

    # Pagination
    per_page = 5
    active_page = int(request.args.get('active_page', 1))
    completed_page = int(request.args.get('completed_page', 1))
    offset_active = (active_page - 1) * per_page
    offset_completed = (completed_page - 1) * per_page

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Active Flights
    cursor.execute("SELECT COUNT(*) AS total FROM Flight WHERE Arrival > %s", (now,))
    total_active = cursor.fetchone()['total']
    active_total_pages = (total_active + per_page - 1) // per_page

    cursor.execute("""
        SELECT * FROM Flight WHERE Arrival > %s
        ORDER BY Departure ASC LIMIT %s OFFSET %s
    """, (now, per_page, offset_active))
    active_flights = cursor.fetchall()

    # Completed Flights
    cursor.execute("SELECT COUNT(*) AS total FROM Flight WHERE Arrival <= %s", (now,))
    total_completed = cursor.fetchone()['total']
    completed_total_pages = (total_completed + per_page - 1) // per_page

    cursor.execute("""
        SELECT * FROM Flight WHERE Arrival <= %s
        ORDER BY Arrival DESC LIMIT %s OFFSET %s
    """, (now, per_page, offset_completed))
    completed_flights = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('manage_flights.html',
                           form=form,
                           active_flights=active_flights,
                           completed_flights=completed_flights,
                           active_page=active_page,
                           active_total_pages=active_total_pages,
                           completed_page=completed_page,
                           completed_total_pages=completed_total_pages)



# End Admin Routes-------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)