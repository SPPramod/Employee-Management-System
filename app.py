import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Database connection
def create_connection():
    """ create a database connection to the MySQL database """
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='employee',
            user='root',  # replace with your MySQL username
            password='823f2987c3b2'  # replace with your MySQL password
        )
        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Insert employee
def add_employee(conn, employee):
    if conn:
        sql = ''' INSERT INTO employees(name, age, department, salary)
                  VALUES(%s, %s, %s, %s) '''
        cur = conn.cursor()
        cur.execute(sql, employee)
        conn.commit()
        return cur.lastrowid
    else:
        st.error("Failed to connect to the database.")
        return None

# Update employee
def update_employee(conn, employee):
    if conn:
        sql = ''' UPDATE employees
                  SET name = %s,
                      age = %s,
                      department = %s,
                      salary = %s
                  WHERE id = %s'''
        cur = conn.cursor()
        cur.execute(sql, employee)
        conn.commit()
    else:
        st.error("Failed to connect to the database.")

# Delete employee
def delete_employee(conn, id):
    if conn:
        sql = 'DELETE FROM employees WHERE id=%s'
        cur = conn.cursor()
        cur.execute(sql, (id,))
        conn.commit()
    else:
        st.error("Failed to connect to the database.")

# Select all employees
def select_all_employees(conn):
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees")
        rows = cur.fetchall()
        return rows
    else:
        st.error("Failed to connect to the database.")
        return []

# Main function for Streamlit
def main():
    conn = create_connection()

    st.title("Employee Management System")

    menu = ["Add", "View", "Update", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add":
        st.subheader("Add Employee")
        with st.form("employee_form"):
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=18, max_value=100, step=1)
            department = st.text_input("Department")
            salary = st.number_input("Salary", min_value=0.0, step=0.1)
            submitted = st.form_submit_button("Add Employee")
            
            if submitted:
                employee = (name, age, department, salary)
                add_employee(conn, employee)
                st.success("Employee added successfully!")

    elif choice == "View":
        st.subheader("View Employees")
        rows = select_all_employees(conn)
        if rows:
            df = pd.DataFrame(rows, columns=['ID', 'Name', 'Age', 'Department', 'Salary'])
            st.table(df)
        else:
            st.write("No employees found.")

    elif choice == "Update":
        st.subheader("Update Employee")
        employee_id = st.number_input("Enter Employee ID", min_value=1, step=1)
        with st.form("update_form"):
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=18, max_value=100, step=1)
            department = st.text_input("Department")
            salary = st.number_input("Salary", min_value=0.0, step=0.1)
            submitted = st.form_submit_button("Update Employee")
            
            if submitted:
                employee = (name, age, department, salary, employee_id)
                update_employee(conn, employee)
                st.success("Employee updated successfully!")

    elif choice == "Delete":
        st.subheader("Delete Employee")
        employee_id = st.number_input("Enter Employee ID", min_value=1, step=1)
        if st.button("Delete Employee"):
            delete_employee(conn, employee_id)
            st.success("Employee deleted successfully!")

if __name__ == '__main__':
    main()
