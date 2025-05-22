# Setup Guide for Student Management System

## Prerequisites and Dependencies
- Node.js installed on your machine
- SQLite database
- Basic knowledge of JavaScript, HTML, and CSS

## Installation Steps
1. Clone the project repository from [GitHub link].
2. Navigate to the project directory in your terminal.
3. Run `npm install` to install project dependencies.

## Configuration Instructions
1. Create a new SQLite database file for the project.
2. Update the database configuration in `utils/database.js` with your database file path.
3. Ensure Node.js is properly configured on your machine.

## How to Run the Application
1. Run `node database.js` to initialize the database tables.
2. Start the server by running `node app.js`.
3. Access the application in your browser at `http://localhost:3000`.

## Basic Usage Instructions
1. Use the following routes to interact with the application:
   - `/students` for student-related operations
   - `/courses` for course-related operations
   - `/enrollments` for enrollment-related operations
2. Perform CRUD operations on student data using the provided routes.
3. Refer to the respective controller and model files for customization and additional functionalities.

---
### Project Details:
- **Software Architecture:** The web version of the student management system follows MVC architecture.
- **Technical Stacks:** SQLite, JavaScript, Node.js, Express, HTML, CSS.
- **File Scaffolding:**
  - **Models:** student.js, course.js, enrollment.js
  - **Controllers:** studentController.js, courseController.js, enrollmentController.js
  - **Routes:** studentRoutes.js, courseRoutes.js, enrollmentRoutes.js
  - **Utils:** database.js, validation.js
- **Number of Files:** 12
- **Number of Prompts:** 5

For any further assistance, refer to the project documentation or contact the project maintainers.

[GitHub link]: # (Provide the link to the project repository)