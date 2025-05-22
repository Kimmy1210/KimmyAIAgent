```javascript
const { DataTypes } = require('sequelize');
const db = require('../utils/database');

const Course = db.define('Course', {
  name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  code: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  credits: {
    type: DataTypes.INTEGER,
    allowNull: false
  }
});

module.exports = Course;
```