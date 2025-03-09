const express = require('express');
const { check } = require('express-validator');
const { register, login, getMe, logout } = require('../controllers/authController');
const { protect } = require('../middlewares/auth');
const { validateRequest } = require('../middlewares/validation');

const router = express.Router();

router.post('/register', [
  check('name', 'Name is required').not().isEmpty(),
  check('email', 'Please include a valid email').isEmail(),
  check('password', 'Please enter a password with 6 or more characters').isLength({ min: 6 })
], validateRequest, register);

router.post('/login', [
  check('email', 'Please include a valid email').isEmail(),
  check('password', 'Password is required').exists()
], validateRequest, login);

router.get('/me', protect, getMe);
router.get('/logout', protect, logout);

module.exports = router;
