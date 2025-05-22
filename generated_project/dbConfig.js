const sqlite3 = require('sqlite3').verbose();

const db = new sqlite3.Database('database.db', (err) => {
  if (err) {
    console.error('Error connecting to the database:', err.message);
  } else {
    console.log('Connected to the SQLite database.');
  }
});

module.exports = db;
```

3. Update your models to use the database connection. For example, in your `student.js` model:

```javascript
// student.js

const db = require('../dbConfig');

class Student {
  static getAll(callback) {
    db.all('SELECT * FROM students', (err, rows) => {
      if (err) {
        callback(err, null);
      } else {
        callback(null, rows);
      }
    });
  }

  // Add other model methods here
}

module.exports = Student;
