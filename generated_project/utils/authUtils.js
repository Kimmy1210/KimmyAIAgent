const jwt = require('jsonwebtoken');

function generateToken(payload) {
  return jwt.sign(payload, 'your_secret_key_here', { expiresIn: '1h' });
}

function verifyToken(token) {
  return jwt.verify(token, 'your_secret_key_here');
}

module.exports = {
  generateToken,
  verifyToken
};
