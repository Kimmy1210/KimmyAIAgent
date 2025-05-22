const express = require('express');
const router = express.Router();
const path = require('path');
const authUtils = require('../utils/authUtils');

// Serve the login page
router.get('/login', (req, res) => {
  const filePath = path.join(__dirname, '../views/index.html');
  res.sendFile(filePath);
});

// POST route for authentication
const authController = require('../controllers/authController');

// Login route
router.post('/login', authController.login);

module.exports = router;


module.exports = router;