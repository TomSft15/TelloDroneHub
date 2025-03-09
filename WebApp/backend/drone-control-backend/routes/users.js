const express = require('express');
const { check } = require('express-validator');
const { 
  getUsers, 
  getUser, 
  updateProfile, 
  updatePassword, 
  deleteUser 
} = require('../controllers/userController');
const { protect, authorize } = require('../middlewares/auth');
const { validateRequest } = require('../middlewares/validation');

const router = express.Router();

// Apply authentication to all routes
router.use(protect);

// Admin-only routes
router.get('/', authorize('admin'), getUsers);
router.get('/:id', authorize('admin'), getUser);
router.delete('/:id', authorize('admin'), deleteUser);

// User profile routes
router.put('/profile', [
  check('name', 'Name is required').optional().not().isEmpty(),
  check('email', 'Please include a valid email').optional().isEmail()
], validateRequest, updateProfile);

router.put('/password', [
  check('currentPassword', 'Current password is required').not().isEmpty(),
  check('newPassword', 'New password must be at least 6 characters').isLength({ min: 6 })
], validateRequest, updatePassword);

module.exports = router;
