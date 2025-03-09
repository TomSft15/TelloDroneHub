const express = require('express');
const { getMedia, deleteMedia, streamMedia } = require('../controllers/mediaController');
const { protect } = require('../middlewares/auth');

const router = express.Router();

// Apply authentication to all routes
router.use(protect);

router.get('/:id', getMedia);
router.delete('/:id', deleteMedia);
router.get('/:id/stream', streamMedia);

module.exports = router;
