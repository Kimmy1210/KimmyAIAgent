```javascript
const db = require('../utils/database');

class Grade {
  constructor(id, studentId, courseId, score) {
    this.id = id;
    this.studentId = studentId;
    this.courseId = courseId;
    this.score = score;
  }

  static getAllGrades() {
    return db.query('SELECT * FROM grades');
  }

  static getGradeById(id) {
    return db.query('SELECT * FROM grades WHERE id = ?', [id]);
  }

  static createGrade(newGrade) {
    return db.query('INSERT INTO grades (studentId, courseId, score) VALUES (?, ?, ?)', [newGrade.studentId, newGrade.courseId, newGrade.score]);
  }

  static updateGrade(id, updatedGrade) {
    return db.query('UPDATE grades SET studentId = ?, courseId = ?, score = ? WHERE id = ?', [updatedGrade.studentId, updatedGrade.courseId, updatedGrade.score, id]);
  }

  static deleteGrade(id) {
    return db.query('DELETE FROM grades WHERE id = ?', [id]);
  }
}

module.exports = Grade;
```  