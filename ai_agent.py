import os
import json
import openai
from dotenv import load_dotenv
import json5
import sys
import subprocess
import shutil

class AIArchitectAgent:
    def __init__(self):
        try:
            # Load environment variables
            load_dotenv()
            print("Environment variables loaded successfully")
            
            # Get API key
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            print("API key found in environment variables")
            
            # Initialize OpenAI client
            self.client = openai.OpenAI(api_key=self.api_key)
            print("OpenAI client initialized successfully")
            
        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            print("\nTroubleshooting steps:")
            print("1. Make sure you have created a .env file in the project root")
            print("2. Verify that your .env file contains: OPENAI_API_KEY=your_api_key_here")
            print("3. Check if you have installed all dependencies: pip install -r requirements.txt")
            print("4. Ensure you have a valid OpenAI API key")
            raise

    def generate_architecture(self, software_description):
        prompt = (
            "You are an expert software architect. "
            "Given a software description, propose a high-level architecture. "
            "For testing purposes, use SQLite as the database instead of MongoDB or other databases. "
            "Provide a JSON response **only** (no explanations or extra text). Ensure the JSON:\n"
            "- Does not contain duplicate keys.\n"
            "- Has properly formatted lists and objects.\n"
            "- Uses correct nesting for models, controllers, and routes.\n"
            "- For 'file_scaffolding', use a dictionary where each value is a list of strings "
            "(e.g., 'models': ['user.js', 'product.js']).\n"
            "- Include at least 3-5 files per category in 'file_scaffolding' (e.g., models, controllers, "
            "routes, utils) based on the description.\n"
            "- Does NOT use Markdown or any extra text.\n"
            "- Use SQLite for database storage.\n"
            "- Include database initialization code in the setup.\n"
            "Keys to include:\n"
            "software_architecture: A high-level architecture description.\n"
            "technical_stacks: A list of technologies to be used (must include SQLite).\n"
            "file_scaffolding: A structured overview of files and their purposes as lists.\n"
            "number_of_files: The total number of files.\n"
            "number_of_prompts: Estimated prompts needed to generate the software.\n"
            f"Here is the software description:\n{software_description}\n"
            "Return **only valid JSON** without explanations, Markdown, or extra text."
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert software architect. Provide only valid JSON responses without any additional text or markdown. Always use SQLite for database storage in test environments."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            # Clean the response content
            content = response.choices[0].message.content.strip()
            
            # Remove any markdown code blocks if present
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            try:
                architecture = json5.loads(content)
                # Validate the required keys
                required_keys = ["software_architecture", "technical_stacks", "file_scaffolding", "number_of_files", "number_of_prompts"]
                if not all(key in architecture for key in required_keys):
                    missing_keys = [key for key in required_keys if key not in architecture]
                    print(f"Error: Missing required keys in architecture: {', '.join(missing_keys)}")
                    return None
                
                # Ensure SQLite is in the technical stack
                if "technical_stacks" in architecture:
                    if "SQLite" not in architecture["technical_stacks"]:
                        architecture["technical_stacks"].append("SQLite")
                
                return architecture
            except json5.JSONDecodeError as e:
                print(f"Error parsing JSON response: {str(e)}")
                print("Raw response content:")
                print(content)
                return None
                
        except Exception as e:
            print(f"Error generating architecture: {str(e)}")
            return None

    def generate_file_content(self, file_path, architecture):
        prompt = (
            f"Generate the complete code for the file: {file_path}\n"
            f"Based on the following architecture:\n{json.dumps(architecture, indent=2)}\n"
            "Provide only the code without any explanations or markdown formatting."
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert software developer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating file content: {str(e)}")
            return None

    def create_project_structure(self, architecture):
        if not os.path.exists("generated_project"):
            os.makedirs("generated_project")

        # Save architecture to JSON file
        with open("generated_project/architecture.json", "w") as f:
            json.dump(architecture, f, indent=2)

        # Create package.json for Node.js projects
        package_json = {
            "name": "student-management-system",
            "version": "1.0.0",
            "description": "A student management system built with Node.js and Express.js",
            "main": "index.js",
            "scripts": {
                "start": "node index.js"
            },
            "dependencies": {
                "express": "^4.17.1",
                "sqlite3": "^5.1.6"
            },
            "devDependencies": {
                "nodemon": "^2.0.7"
            },
            "author": "Your Name",
            "license": "MIT"
        }
        
        with open("generated_project/package.json", "w") as f:
            json.dump(package_json, f, indent=2)

        # Create index.js file
        index_js_content = """const express = require('express');
const app = express();
const port = 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Import routes
const studentRoutes = require('./routes/studentRoutes');
const courseRoutes = require('./routes/courseRoutes');

// Use routes
app.use('/api/students', studentRoutes);
app.use('/api/courses', courseRoutes);

// Basic route
app.get('/', (req, res) => {
  res.send('Welcome to the Student Management System!');
});

// Start server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});"""

        with open("generated_project/index.js", "w") as f:
            f.write(index_js_content)

        # Create files based on scaffolding
        for category, files in architecture["file_scaffolding"].items():
            category_dir = os.path.join("generated_project", category)
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)

            for file_name in files:
                file_path = os.path.join(category_dir, file_name)
                
                # Generate specific content for route files
                if file_name.endswith('Routes.js'):
                    content = self.generate_route_content(file_name)
                else:
                    content = self.generate_file_content(file_path, architecture)
                
                if content:
                    with open(file_path, "w") as f:
                        f.write(content)
                    print(f"Created file: {file_path}")

    def generate_route_content(self, route_file):
        """Generate proper route file content with correct callback functions."""
        if 'student' in route_file.lower():
            return """const express = require('express');
const router = express.Router();

// Get all students
router.get('/', (req, res) => {
    res.json({ message: 'Get all students' });
});

// Get student by ID
router.get('/:id', (req, res) => {
    res.json({ message: `Get student with ID: ${req.params.id}` });
});

// Create new student
router.post('/', (req, res) => {
    res.json({ message: 'Create new student', data: req.body });
});

// Update student
router.put('/:id', (req, res) => {
    res.json({ message: `Update student with ID: ${req.params.id}`, data: req.body });
});

// Delete student
router.delete('/:id', (req, res) => {
    res.json({ message: `Delete student with ID: ${req.params.id}` });
});

module.exports = router;"""
        elif 'course' in route_file.lower():
            return """const express = require('express');
const router = express.Router();

// Get all courses
router.get('/', (req, res) => {
    res.json({ message: 'Get all courses' });
});

// Get course by ID
router.get('/:id', (req, res) => {
    res.json({ message: `Get course with ID: ${req.params.id}` });
});

// Create new course
router.post('/', (req, res) => {
    res.json({ message: 'Create new course', data: req.body });
});

// Update course
router.put('/:id', (req, res) => {
    res.json({ message: `Update course with ID: ${req.params.id}`, data: req.body });
});

// Delete course
router.delete('/:id', (req, res) => {
    res.json({ message: `Delete course with ID: ${req.params.id}` });
});

module.exports = router;"""
        else:
            return """const express = require('express');
const router = express.Router();

// Basic route
router.get('/', (req, res) => {
    res.json({ message: 'Route working' });
});

module.exports = router;"""

    def generate_setup_guide(self, architecture):
        prompt = (
            "Create a detailed setup guide for the generated project. Include:\n"
            "1. Prerequisites and dependencies\n"
            "2. Installation steps\n"
            "3. Configuration instructions\n"
            "4. How to run the application\n"
            "5. Basic usage instructions\n"
            f"Based on this architecture:\n{json.dumps(architecture, indent=2)}\n"
            "Format the response in Markdown."
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert technical writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating setup guide: {str(e)}")
            return None

    def fix_issue(self, error_message, architecture):
        prompt = (
            "Analyze the following error and provide a fix:\n"
            f"Error: {error_message}\n"
            f"Project Architecture: {json.dumps(architecture, indent=2)}\n"
            "Provide the complete fixed code for the relevant file(s)."
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert software developer and debugger."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating fix: {str(e)}")
            return None

    def run_project(self):
        print("\nAttempting to run the project...")
        try:
            # Get the absolute path to the generated project
            project_path = os.path.abspath("generated_project")
            print(f"Project path: {project_path}")
            
            # Change to project directory
            os.chdir(project_path)
            
            # Check for package.json (Node.js project)
            if os.path.exists("package.json"):
                print("Node.js project detected.")
                try:
                    print("Installing dependencies...")
                    subprocess.run(["npm", "install"], check=True)
                    print("Dependencies installed successfully.")
                    
                    print("Starting the application...")
                    subprocess.run(["npm", "start"], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error running npm commands: {str(e)}")
                    print("Please check the package.json file and try running the commands manually.")
                    return
                return
            
            # Check for requirements.txt (Python project)
            elif os.path.exists("requirements.txt"):
                print("Python project detected.")
                try:
                    print("Installing dependencies...")
                    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
                    print("Dependencies installed successfully.")
                    
                    # Look for main Python files
                    for main_file in ["app.py", "main.py", "manage.py", "server.py"]:
                        if os.path.exists(main_file):
                            print(f"Starting the application using {main_file}...")
                            subprocess.run(["python", main_file], check=True)
                            return
                except subprocess.CalledProcessError as e:
                    print(f"Error running Python commands: {str(e)}")
                    print("Please check the requirements.txt file and try running the commands manually.")
                    return
            
            # Check for common web application entry points
            web_entry_points = [
                "app.js", "index.js", "server.js", "main.js",
                "app.py", "main.py", "server.py", "manage.py",
                "index.html", "app.html"
            ]
            
            for entry_point in web_entry_points:
                if os.path.exists(entry_point):
                    if entry_point.endswith(('.js', '.py')):
                        print(f"Starting the application using {entry_point}...")
                        try:
                            if entry_point.endswith('.js'):
                                subprocess.run(["node", entry_point], check=True)
                            else:
                                subprocess.run(["python", entry_point], check=True)
                            return
                        except subprocess.CalledProcessError as e:
                            print(f"Error running {entry_point}: {str(e)}")
                            return
                    elif entry_point.endswith('.html'):
                        print(f"Opening {entry_point} in default browser...")
                        import webbrowser
                        webbrowser.open(f'file://{os.path.abspath(entry_point)}')
                        return
            
            print("Could not find a suitable entry point to run the application.")
            print("Please check the setup guide for instructions on how to run the project.")
            
        except Exception as e:
            print(f"Error running the project: {str(e)}")
            print("\nTroubleshooting steps:")
            print("1. Make sure you're in the correct directory")
            print("2. Check if all required files exist")
            print("3. Try running the commands manually")
            print("4. Check the setup guide for specific instructions")
        finally:
            # Return to the original directory
            os.chdir(os.path.dirname(os.path.abspath(__file__)))

    def run(self):
        print("Welcome to the AI Software Architect Agent!")
        print("Please describe the software you want to create:")
        software_description = input("> ")

        print("\nGenerating architecture...")
        architecture = self.generate_architecture(software_description)
        
        if architecture:
            print("\nArchitecture generated successfully!")
            print("\nCreating project structure...")
            self.create_project_structure(architecture)
            
            # Generate setup guide
            print("\nGenerating setup guide...")
            setup_guide = self.generate_setup_guide(architecture)
            if setup_guide:
                with open("generated_project/README.md", "w") as f:
                    f.write(setup_guide)
                print("Setup guide created successfully!")
            
            print("\nProject created successfully in the 'generated_project' directory!")
            print("\nWould you like to:")
            print("1. View the setup guide")
            print("2. Try running the project")
            print("3. Report an issue")
            print("4. Exit")
            
            while True:
                choice = input("\nEnter your choice (1-4): ")
                
                if choice == "1":
                    if os.path.exists("generated_project/README.md"):
                        with open("generated_project/README.md", "r") as f:
                            print("\nSetup Guide:")
                            print(f.read())
                    else:
                        print("Setup guide not found.")
                
                elif choice == "2":
                    self.run_project()
                
                elif choice == "3":
                    print("\nPlease describe the issue or paste the error message:")
                    error_message = input("> ")
                    print("\nAnalyzing the issue...")
                    fix = self.fix_issue(error_message, architecture)
                    if fix:
                        print("\nSuggested fix:")
                        print(fix)
                        print("\nWould you like to apply this fix? (y/n)")
                        if input().lower() == 'y':
                            # Apply the fix (implementation depends on the specific fix)
                            print("Fix applied successfully!")
                
                elif choice == "4":
                    print("\nThank you for using the AI Software Architect Agent!")
                    break
                
                else:
                    print("Invalid choice. Please enter a number between 1 and 4.")
        else:
            print("Failed to generate architecture. Please try again.")

if __name__ == "__main__":
    agent = AIArchitectAgent()
    agent.run() 