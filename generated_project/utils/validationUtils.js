```javascript
// generated_project\utils\validationUtils.js

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isValidPassword(password) {
  return password.length >= 8;
}

module.exports = {
  isValidEmail,
  isValidPassword
};
```