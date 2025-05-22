```javascript
// generated_project\utils\validator.js

function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function validatePassword(password) {
  return password.length >= 6;
}

module.exports = {
  validateEmail,
  validatePassword
};
```