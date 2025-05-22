```javascript
// generated_project\controllers\courseController.js

const Course = require('../models/course');

// Controller function to get all courses
const getAllCourses = async (req, res) => {
  try {
    const courses = await Course.findAll();
    res.json(courses);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Controller function to get a single course by ID
const getCourseById = async (req, res) => {
  const { id } = req.params;
  try {
    const course = await Course.findByPk(id);
    if (course) {
      res.json(course);
    } else {
      res.status(404).json({ message: 'Course not found' });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Controller function to create a new course
const createCourse = async (req, res) => {
  const { name, description } = req.body;
  try {
    const newCourse = await Course.create({ name, description });
    res.status(201).json(newCourse);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
};

// Controller function to update a course by ID
const updateCourse = async (req, res) => {
  const { id } = req.params;
  const { name, description } = req.body;
  try {
    const course = await Course.findByPk(id);
    if (course) {
      await course.update({ name, description });
      res.json(course);
    } else {
      res.status(404).json({ message: 'Course not found' });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Controller function to delete a course by ID
const deleteCourse = async (req, res) => {
  const { id } = req.params;
  try {
    const course = await Course.findByPk(id);
    if (course) {
      await course.destroy();
      res.json({ message: 'Course deleted successfully' });
    } else {
      res.status(404).json({ message: 'Course not found' });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

module.exports = {
  getAllCourses,
  getCourseById,
  createCourse,
  updateCourse,
  deleteCourse,
};
```