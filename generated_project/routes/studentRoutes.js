const express = require('express');
const router = express.Router();

// Get all students
router.get('/', (req, res) => {
    res.json({ message: 'Get all students' });
});

// Get student by ID
router.get('/:id', (req, res) => {
    res.json({ message: `Get student with ID: ${req.params.id}` });
});

// Create new student
router.post('/', (req, res) => {
    res.json({ message: 'Create new student', data: req.body });
});

// Update student
router.put('/:id', (req, res) => {
    res.json({ message: `Update student with ID: ${req.params.id}`, data: req.body });
});

// Delete student
router.delete('/:id', (req, res) => {
    res.json({ message: `Delete student with ID: ${req.params.id}` });
});

module.exports = router;