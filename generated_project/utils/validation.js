```javascript
const validateStudent = (student) => {
  if (!student.name || !student.age || !student.grade) {
    return false;
  }
  return true;
};

module.exports = {
  validateStudent
};
```