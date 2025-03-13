const swaggerJsDoc = require('swagger-jsdoc');

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Drone Management API',
      version: '1.0.0',
      description: 'API for managing and controlling drones',
      contact: {
        name: 'API Support',
        email: 'support@droneapi.com',
      },
    },
    servers: [
      {
        url: 'http://localhost:3000/api',
        description: 'Development server',
      },
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT',
        },
        cookieAuth: {
          type: 'apiKey',
          in: 'cookie',
          name: 'token',
        },
      },
      schemas: {
        User: {
          type: 'object',
          required: ['name', 'email', 'password'],
          properties: {
            id: {
              type: 'string',
              description: 'User ID',
            },
            name: {
              type: 'string',
              description: 'User name',
            },
            email: {
              type: 'string',
              format: 'email',
              description: 'User email',
            },
            role: {
              type: 'string',
              enum: ['user', 'admin'],
              description: 'User role',
            },
            createdAt: {
              type: 'string',
              format: 'date-time',
              description: 'User creation date',
            },
          },
        },
        Drone: {
          type: 'object',
          required: ['name', 'model', 'serialNumber'],
          properties: {
            id: {
              type: 'string',
              description: 'Drone ID',
            },
            name: {
              type: 'string',
              description: 'Drone name',
            },
            model: {
              type: 'string',
              description: 'Drone model',
            },
            serialNumber: {
              type: 'string',
              description: 'Drone serial number',
            },
            status: {
              type: 'string',
              enum: ['idle', 'flying', 'charging', 'maintenance'],
              description: 'Drone current status',
            },
            owner: {
              type: 'string',
              description: 'Drone owner ID',
            },
            keyBindings: {
              type: 'object',
              description: 'Custom keyboard bindings for drone control',
            },
            createdAt: {
              type: 'string',
              format: 'date-time',
              description: 'Drone creation date',
            },
          },
        },
        Media: {
          type: 'object',
          properties: {
            id: {
              type: 'string',
              description: 'Media ID',
            },
            drone: {
              type: 'string',
              description: 'Associated drone ID',
            },
            type: {
              type: 'string',
              enum: ['photo', 'video'],
              description: 'Media type',
            },
            filename: {
              type: 'string',
              description: 'Filename',
            },
            filepath: {
              type: 'string',
              description: 'File path on server',
            },
            size: {
              type: 'integer',
              description: 'File size in bytes',
            },
            mimeType: {
              type: 'string',
              description: 'MIME type',
            },
            resolution: {
              type: 'object',
              properties: {
                width: { type: 'integer' },
                height: { type: 'integer' },
              },
              description: 'Media resolution',
            },
            duration: {
              type: 'number',
              description: 'Video duration in seconds',
            },
            location: {
              type: 'object',
              properties: {
                lat: { type: 'number' },
                lng: { type: 'number' },
                alt: { type: 'number' },
              },
              description: 'Location where media was captured',
            },
            createdAt: {
              type: 'string',
              format: 'date-time',
              description: 'Media creation date',
            },
          },
        },
        FlightLog: {
          type: 'object',
          properties: {
            id: {
              type: 'string',
              description: 'Flight log ID',
            },
            drone: {
              type: 'string',
              description: 'Associated drone ID',
            },
            startTime: {
              type: 'string',
              format: 'date-time',
              description: 'Flight start time',
            },
            endTime: {
              type: 'string',
              format: 'date-time',
              description: 'Flight end time',
            },
            duration: {
              type: 'number',
              description: 'Flight duration in seconds',
            },
            startLocation: {
              type: 'object',
              properties: {
                lat: { type: 'number' },
                lng: { type: 'number' },
                alt: { type: 'number' },
              },
              description: 'Flight start location',
            },
            endLocation: {
              type: 'object',
              properties: {
                lat: { type: 'number' },
                lng: { type: 'number' },
                alt: { type: 'number' },
              },
              description: 'Flight end location',
            },
            batteryStart: {
              type: 'number',
              description: 'Battery percentage at start',
            },
            batteryEnd: {
              type: 'number',
              description: 'Battery percentage at end',
            },
          },
        },
        Error: {
          type: 'object',
          properties: {
            success: {
              type: 'boolean',
              default: false,
            },
            error: {
              type: 'string',
            },
          },
        },
        Telemetry: {
          type: 'object',
          properties: {
            batteryLevel: {
              type: 'number',
              description: 'Current battery percentage',
            },
            temperature: {
              type: 'number',
              description: 'Drone temperature',
            },
            position: {
              type: 'object',
              properties: {
                lat: { type: 'number' },
                lng: { type: 'number' },
                alt: { type: 'number' },
              },
              description: 'Current drone position',
            },
            speed: {
              type: 'number',
              description: 'Current speed in m/s',
            },
            signalStrength: {
              type: 'number',
              description: 'Signal strength percentage',
            },
            orientation: {
              type: 'object',
              properties: {
                roll: { type: 'number' },
                pitch: { type: 'number' },
                yaw: { type: 'number' },
              },
              description: 'Drone orientation in degrees',
            },
            timestamp: {
              type: 'string',
              format: 'date-time',
              description: 'Timestamp of telemetry data',
            },
          },
        },
      },
    },
    security: [
      {
        bearerAuth: [],
      },
      {
        cookieAuth: [],
      },
    ],
    paths: {
      // Authentication routes
      '/auth/register': {
        post: {
          summary: 'Register a new user',
          tags: ['Authentication'],
          security: [],
          requestBody: {
            required: true,
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  required: ['name', 'email', 'password', 'role'],
                  properties: {
                    name: {
                      type: 'string',
                    },
                    email: {
                      type: 'string',
                      format: 'email',
                    },
                    password: {
                      type: 'string',
                      minLength: 6,
                    },
                    role: {
                      type: 'string',
                      enum: ['user', 'admin'],
                    },
                  },
                },
              },
            },
          },
          responses: {
            201: {
              description: 'User registered successfully',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      token: {
                        type: 'string',
                      },
                    },
                  },
                },
              },
            },
            400: {
              description: 'Validation error or user already exists',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            500: {
              description: 'Server error',
            },
          },
        },
      },
      '/auth/login': {
        post: {
          summary: 'Login user',
          tags: ['Authentication'],
          security: [],
          requestBody: {
            required: true,
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  required: ['email', 'password'],
                  properties: {
                    email: {
                      type: 'string',
                      format: 'email',
                    },
                    password: {
                      type: 'string',
                    },
                  },
                },
              },
            },
          },
          responses: {
            200: {
              description: 'User logged in successfully',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      token: {
                        type: 'string',
                      },
                    },
                  },
                },
              },
            },
            401: {
              description: 'Invalid credentials',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            500: {
              description: 'Server error',
            },
          },
        },
      },
      '/auth/me': {
        get: {
          summary: 'Get logged in user',
          tags: ['Authentication'],
          responses: {
            200: {
              description: 'Current user data',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      data: {
                        $ref: '#/components/schemas/User',
                      },
                    },
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            500: {
              description: 'Server error',
            },
          },
        },
      },
      '/auth/logout': {
        get: {
          summary: 'Logout user',
          tags: ['Authentication'],
          responses: {
            200: {
              description: 'Successfully logged out',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      data: {
                        type: 'object',
                      },
                    },
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
            },
            500: {
              description: 'Server error',
            },
          },
        },
      },

      // Drone routes
      '/drones': {
        get: {
          summary: 'Get all drones for current user',
          tags: ['Drones'],
          responses: {
            200: {
              description: 'List of drones',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      count: {
                        type: 'integer',
                      },
                      data: {
                        type: 'array',
                        items: {
                          $ref: '#/components/schemas/Drone',
                        },
                      },
                    },
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            500: {
              description: 'Server error',
            },
          },
        },
        post: {
          summary: 'Create a new drone',
          tags: ['Drones'],
          requestBody: {
            required: true,
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  required: ['name', 'model', 'serialNumber'],
                  properties: {
                    name: {
                      type: 'string',
                    },
                    model: {
                      type: 'string',
                    },
                    serialNumber: {
                      type: 'string',
                    },
                  },
                },
              },
            },
          },
          responses: {
            201: {
              description: 'Drone created',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      data: {
                        $ref: '#/components/schemas/Drone',
                      },
                    },
                  },
                },
              },
            },
            400: {
              description: 'Validation error',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
            },
            500: {
              description: 'Server error',
            },
          },
        },
      },
      '/drones/{id}': {
        get: {
          summary: 'Get single drone by ID',
          tags: ['Drones'],
          parameters: [
            {
              name: 'id',
              in: 'path',
              required: true,
              schema: {
                type: 'string',
              },
              description: 'Drone ID',
            },
          ],
          responses: {
            200: {
              description: 'Drone details',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      data: {
                        $ref: '#/components/schemas/Drone',
                      },
                    },
                  },
                },
              },
            },
            404: {
              description: 'Drone not found',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
            },
            403: {
              description: 'Not authorized',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            500: {
              description: 'Server error',
            },
          },
        },
        put: {
          summary: 'Update drone',
          tags: ['Drones'],
          parameters: [
            {
              name: 'id',
              in: 'path',
              required: true,
              schema: {
                type: 'string',
              },
              description: 'Drone ID',
            },
          ],
          requestBody: {
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  properties: {
                    name: {
                      type: 'string',
                    },
                    model: {
                      type: 'string',
                    },
                    serialNumber: {
                      type: 'string',
                    },
                    status: {
                      type: 'string',
                      enum: ['idle', 'flying', 'charging', 'maintenance'],
                    },
                  },
                },
              },
            },
          },
          responses: {
            200: {
              description: 'Drone updated',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      data: {
                        $ref: '#/components/schemas/Drone',
                      },
                    },
                  },
                },
              },
            },
            400: {
              description: 'Validation error',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            404: {
              description: 'Drone not found',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
            },
            403: {
              description: 'Not authorized',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            500: {
              description: 'Server error',
            },
          },
        },
        delete: {
          summary: 'Delete drone',
          tags: ['Drones'],
          parameters: [
            {
              name: 'id',
              in: 'path',
              required: true,
              schema: {
                type: 'string',
              },
              description: 'Drone ID',
            },
          ],
          responses: {
            200: {
              description: 'Drone deleted',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      data: {
                        type: 'object',
                      },
                    },
                  },
                },
              },
            },
            404: {
              description: 'Drone not found',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
            },
            403: {
              description: 'Not authorized',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            500: {
              description: 'Server error',
            },
          },
        },
      },

      // Flight control routes
      '/drones/{id}/flight/start': {
        post: {
          summary: 'Start a flight',
          tags: ['Flight Control'],
          parameters: [
            {
              name: 'id',
              in: 'path',
              required: true,
              schema: {
                type: 'string',
              },
              description: 'Drone ID',
            },
          ],
          responses: {
            200: {
              description: 'Flight started',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      data: {
                        type: 'object',
                        properties: {
                          flightId: {
                            type: 'string',
                          },
                          startTime: {
                            type: 'string',
                            format: 'date-time',
                          },
                        },
                      },
                    },
                  },
                },
              },
            },
            400: {
              description: 'Drone already flying or in invalid state',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            404: {
              description: 'Drone not found',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
            },
            403: {
              description: 'Not authorized',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            500: {
              description: 'Server error',
            },
          },
        },
      },
      '/drones/{id}/flight/end': {
        post: {
          summary: 'End a flight',
          tags: ['Flight Control'],
          parameters: [
            {
              name: 'id',
              in: 'path',
              required: true,
              schema: {
                type: 'string',
              },
              description: 'Drone ID',
            },
          ],
          responses: {
            200: {
              description: 'Flight ended',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      data: {
                        $ref: '#/components/schemas/FlightLog',
                      },
                    },
                  },
                },
              },
            },
            400: {
              description: 'Drone not flying',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            404: {
              description: 'Drone not found',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
            },
            403: {
              description: 'Not authorized',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            500: {
              description: 'Server error',
            },
          },
        },
      },
      '/drones/{id}/command': {
        post: {
          summary: 'Send a command to drone',
          tags: ['Flight Control'],
          parameters: [
            {
              name: 'id',
              in: 'path',
              required: true,
              schema: {
                type: 'string',
              },
              description: 'Drone ID',
            },
          ],
          requestBody: {
            required: true,
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  required: ['command'],
                  properties: {
                    command: {
                      type: 'string',
                      enum: ['takeoff', 'land', 'move', 'rotate', 'hover', 'emergency'],
                      description: 'Command name',
                    },
                    params: {
                      type: 'object',
                      description: 'Command parameters (varies by command)',
                    },
                  },
                },
              },
            },
          },
          responses: {
            200: {
              description: 'Command sent successfully',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      command: {
                        type: 'string',
                      },
                      result: {
                        type: 'object',
                        description: 'Command result',
                      },
                    },
                  },
                },
              },
            },
            400: {
              description: 'Bad request or drone not flying',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            404: {
              description: 'Drone not found',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
            },
            403: {
              description: 'Not authorized',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            500: {
              description: 'Server error',
            },
          },
        },
      },

      // Telemetry routes
      '/drones/{id}/telemetry': {
        get: {
          summary: 'Get drone telemetry data',
          tags: ['Telemetry'],
          parameters: [
            {
              name: 'id',
              in: 'path',
              required: true,
              schema: {
                type: 'string',
              },
              description: 'Drone ID',
            },
          ],
          responses: {
            200: {
              description: 'Telemetry data',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      data: {
                        $ref: '#/components/schemas/Telemetry',
                      },
                    },
                  },
                },
              },
            },
            404: {
              description: 'Drone not found',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
            },
            403: {
              description: 'Not authorized',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            500: {
              description: 'Server error',
            },
          },
        },
      },

      // Configuration routes
      '/drones/{id}/keyboard-bindings': {
        put: {
          summary: 'Update drone keyboard bindings',
          tags: ['Configuration'],
          parameters: [
            {
              name: 'id',
              in: 'path',
              required: true,
              schema: {
                type: 'string',
              },
              description: 'Drone ID',
            },
          ],
          requestBody: {
            required: true,
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  properties: {
                    keyBindings: {
                      type: 'object',
                      additionalProperties: {
                        type: 'object',
                        properties: {
                          command: { type: 'string' },
                          params: { type: 'object' },
                        },
                      },
                      example: {
                        "ArrowUp": {
                          "command": "move",
                          "params": { "direction": "forward", "speed": 0.5 }
                        },
                        "Space": {
                          "command": "takeoff"
                        }
                      }
                    },
                  },
                },
              },
            },
          },
          responses: {
            200: {
              description: 'Keyboard bindings updated',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      data: {
                        type: 'object',
                        description: 'Updated key bindings',
                      },
                    },
                  },
                },
              },
            },
            404: {
              description: 'Drone not found',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
            },
            403: {
              description: 'Not authorized',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            500: {
              description: 'Server error',
            },
          },
        },
      },

      // Flight logs
      '/drones/{id}/flight-logs': {
        get: {
          summary: 'Get drone flight logs',
          tags: ['Flight Logs'],
          parameters: [
            {
              name: 'id',
              in: 'path',
              required: true,
              schema: {
                type: 'string',
              },
              description: 'Drone ID',
            },
          ],
          responses: {
            200: {
              description: 'Flight logs',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      count: {
                        type: 'integer',
                      },
                      data: {
                        type: 'array',
                        items: {
                          $ref: '#/components/schemas/FlightLog',
                        },
                      },
                    },
                  },
                },
              },
            },
            404: {
              description: 'Drone not found',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
            },
            403: {
              description: 'Not authorized',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            500: {
              description: 'Server error',
            },
          },
        },
      },
      // User routes
      '/users': {
        get: {
          summary: 'Get all users',
          tags: ['Users'],
          security: [{ bearerAuth: [] }],
          responses: {
            200: {
              description: 'List of users',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      count: {
                        type: 'integer',
                      },
                      data: {
                        type: 'array',
                        items: {
                          $ref: '#/components/schemas/User',
                        },
                      },
                    },
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
            },
            403: {
              description: 'Not authorized - admin only',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            500: {
              description: 'Server error',
            },
          },
        },
      },
      '/users/{id}': {
        get: {
          summary: 'Get single user',
          tags: ['Users'],
          parameters: [
            {
              name: 'id',
              in: 'path',
              required: true,
              schema: {
                type: 'string',
              },
              description: 'User ID',
            },
          ],
          responses: {
            200: {
              description: 'User details',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      data: {
                        $ref: '#/components/schemas/User',
                      },
                    },
                  },
                },
              },
            },
            404: {
              description: 'User not found',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
            },
            403: {
              description: 'Not authorized - admin only',
            },
            500: {
              description: 'Server error',
            },
          },
        },
        delete: {
          summary: 'Delete user',
          tags: ['Users'],
          parameters: [
            {
              name: 'id',
              in: 'path',
              required: true,
              schema: {
                type: 'string',
              },
              description: 'User ID',
            },
          ],
          responses: {
            200: {
              description: 'User deleted',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      data: {
                        type: 'object',
                      },
                    },
                  },
                },
              },
            },
            400: {
              description: 'Admin cannot delete themselves',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            404: {
              description: 'User not found',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
            },
            403: {
              description: 'Not authorized - admin only',
            },
            500: {
              description: 'Server error',
            },
          },
        },
      },
      '/users/profile': {
        put: {
          summary: 'Update user profile',
          tags: ['Users'],
          requestBody: {
            required: true,
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  properties: {
                    name: {
                      type: 'string',
                    },
                    email: {
                      type: 'string',
                      format: 'email',
                    },
                  },
                },
              },
            },
          },
          responses: {
            200: {
              description: 'Profile updated successfully',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      data: {
                        $ref: '#/components/schemas/User',
                      },
                    },
                  },
                },
              },
            },
            400: {
              description: 'Validation error',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            401: {
              description: 'Not authenticated',
            },
            500: {
              description: 'Server error',
            },
          },
        },
      },
      '/users/password': {
        put: {
          summary: 'Update user password',
          tags: ['Users'],
          requestBody: {
            required: true,
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  required: ['currentPassword', 'newPassword'],
                  properties: {
                    currentPassword: {
                      type: 'string',
                    },
                    newPassword: {
                      type: 'string',
                      minLength: 6,
                    },
                  },
                },
              },
            },
          },
          responses: {
            200: {
              description: 'Password updated successfully',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      success: {
                        type: 'boolean',
                        default: true,
                      },
                      message: {
                        type: 'string',
                      },
                    },
                  },
                },
              },
            },
            400: {
              description: 'Validation error - passwords not provided',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            401: {
              description: 'Current password is incorrect',
              content: {
                'application/json': {
                  schema: {
                    $ref: '#/components/schemas/Error',
                  },
                },
              },
            },
            500: {
              description: 'Server error',
            },
          },
        },
      },
    },
  },
  apis: ['./controllers/*.js'],
};

module.exports = swaggerJsDoc(options);