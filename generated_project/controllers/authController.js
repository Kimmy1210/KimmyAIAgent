const express = require('express');
const router = express.Router();

// Default credentials
const defaultUsername = 'admin';
const defaultPassword = 'admin123';

// Login controller function
const login = (req, res) => {
  const { username, password } = req.body;

  if (username === defaultUsername && password === defaultPassword) {
    // Successful login
    res.send('Login successful!'); // You can redirect to the main page here
  } else {
    // Failed login
    res.status(401).send('Invalid credentials. Please try again.');
  }
};

module.exports = {
  login,
};
