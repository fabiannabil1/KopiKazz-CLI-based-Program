# Coffee Management System

## Overview

The ** Coffee Management System** is a comprehensive application designed to manage various aspects of coffee production and administration within the  organization. The system provides functionalities for managing farmers, coffee types, invoices, and administrative tasks. It is built to streamline operations, improve data accuracy, and enhance the overall efficiency of coffee production management.

## Features

### 1. **User Authentication**
   - **Admin Login**: Admins can log in to access the full range of administrative features.
   - **Team Login**: Team members can log in to access limited functionalities relevant to their roles.
   - **Registration**: Admins can register new users with a secure registration code.

### 2. **Farmer Management**
   - **Add Farmers**: Admins and team members can add new farmers to the system, including details such as name, land area, estimated production, and address.
   - **View Farmers**: Users can view a list of all farmers with pagination support.
   - **Update Farmer Information**: Admins can update farmer details such as land area, estimated production, and address.
   - **Delete Farmers**: Admins can remove farmers from the system.

### 3. **Coffee Type Management**
   - **View Coffee Types**: Users can view a list of all coffee types along with their prices and PNBP (Non-Tax State Revenue).
   - **Update Coffee Prices**: Admins can update the prices and PNBP of coffee types.

### 4. **Invoice Management**
   - **Issue Invoices**: Admins can issue new invoices for farmers.
   - **Update Invoice Status**: Admins and team members can update the status of invoices (e.g., paid, unpaid).
   - **View Invoices**: Users can view a list of all invoices with pagination support.
   - **Delete Invoices**: Admins can delete invoices from the system.

### 5. **Team Management**
   - **Add Team Members**: Admins can add new team members to the system.
   - **View Team Members**: Admins can view a list of all team members.
   - **Update Team Member Information**: Admins can update team member details such as name, username, and password.
   - **Delete Team Members**: Admins can remove team members from the system.

### 6. **User Interface**
   - **Clear and Intuitive UI**: The system features a clear and user-friendly interface with ASCII art headers and menus.
   - **Pagination**: Lists of farmers, invoices, and team members are displayed with pagination for easier navigation.

## Installation

### Prerequisites
- Python 3.x
- MySQL Database
- Required Python libraries: `tabulate`, `pandas`, `mysql-connector-python`

### Steps
1. **Clone the Repository**

2. **Set Up the Database**:
   - Create a MySQL database named `_coffee`.
   - Import the provided SQL schema into the database.

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database Connection**:
   - Update the `Koneksi_db.py` file with your MySQL database credentials.

5. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage

1. **Start the Application**:
   - Run the application using the command above.
   - The main menu will be displayed, offering options to log in, register as an admin, or exit the system.

2. **Log In**:
   - Use the provided credentials to log in as an admin or team member.
   - Admins will have access to all features, while team members will have limited access.

3. **Navigate the Menus**:
   - Use the menu options to manage farmers, coffee types, invoices, and team members.
   - Follow the on-screen instructions to perform various operations.

4. **Exit the Application**:
   - Use the logout option to return to the main menu and exit the system.

## Code Structure

- **main.py**: The main entry point of the application.
- **Koneksi_db.py**: Handles database connections and operations.
- **UI/**: Contains text files for UI headers and menus.
- **README.md**: This file, providing an overview of the project.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- ****: For providing the opportunity to develop this system.
- **Python Community**: For the wealth of libraries and resources available.

---

Thank you for using the Coffee Management System! We hope it helps streamline your coffee production management processes.
