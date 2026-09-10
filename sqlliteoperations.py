import psycopg
connection_string = "postgresql://neondb_owner:npg_E1K3WPzXntMy@ep-soft-lake-a571b2p7-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

conn = psycopg.connect(connection_string)
cursor = conn.cursor()


def validate_input(data):

    values = data.split()

    if len(values) != 3:
        print("Each input must contain exactly 3 values")
        return None

    try:
        id = int(values[0])
    except ValueError:
        print("ID must be an integer")
        return None

    name = values[1]

    if name.isdigit():
        print("Name cannot contain only an integer")
        return None

    if name == "":
        print("Name cannot be empty")
        return None

    try:
        age = float(values[2])
    except ValueError:
        print("Age must be a valid number")
        return None

    if id <= 0:
        print("ID must be greater than 0")
        return None

    if age < 0:
        print("Age cannot be negative")
        return None

    return [id, name, age]


def check_user(IdsList):

    placeholders = ", ".join(["%s"] * len(IdsList))

    query = f"""
        SELECT id
        FROM students
        WHERE id IN ({placeholders})
    """

    cursor.execute(query, IdsList)

    rows = cursor.fetchall()

    if rows:
        print("These IDs already exist:", [row[0] for row in rows])
        return True

    return False


def add_users(list1, list2, list3):

    query = """
        INSERT INTO students (id, name, age)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query, list1)
    cursor.execute(query, list2)
    cursor.execute(query, list3)

    conn.commit()

    print("All three users added successfully")


while True:

    num = int(input("Enter the number: "))

    if num == 1:

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER,
                name TEXT,
                age FLOAT
            )
        """)

        conn.commit()

        print("Table created")

    elif num == 2:

        list1 = validate_input(input("Enter first student: "))

        if list1 is None:
            continue

        list2 = validate_input(input("Enter second student: "))

        if list2 is None:
            continue

        list3 = validate_input(input("Enter third student: "))

        if list3 is None:
            continue

        IdsList = [list1[0], list2[0], list3[0]]

        if len(IdsList) != len(set(IdsList)):
            print("Duplicate IDs found in the three inputs")
            continue

        if check_user(IdsList):
            continue

        add_users(list1, list2, list3)

    elif num == 3:

        cursor.execute("SELECT * FROM students")

        rows = cursor.fetchall()

        for row in rows:
            print(row)

    elif num == 4:
        break

    else:
        print("Invalid option")


cursor.close()
conn.close()