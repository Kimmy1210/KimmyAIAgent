const sqlite3 = require('sqlite3').verbose();

const DBSOURCE = "./database.sqlite";

let db = new sqlite3.Database(DBSOURCE, (err) => {
  if (err) {
    console.error(err.message);
    throw err;
  } else {
    console.log('Connected to the SQLite database.');
    db.run(`CREATE TABLE IF NOT EXISTS students (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      age INTEGER,
      email TEXT UNIQUE
    )`, (err) => {
      if (err) {
        console.error(err.message);
      }
    });
  }
});

module.exports = db;