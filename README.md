# Message Management Application

A simple full-stack application that allows users to view and add messages based on their roles. This project demonstrates role-based access control, user authentication, and basic CRUD operations.

## Features

### 1. User Authentication
- Secure login system with username/password authentication
- Role-based access control (admin vs. read-only users)
- Default credentials:
  - Admin: `admin/admin123`
  - Regular user: `user/user123`

### 2. Message Management
- View all messages in a clean, tabular format
- Messages are stored with ID, userID, and content
- Data persistence using a simple file-based storage system
- **Pagination support** for efficient browsing of large message collections

### 3. Role-Based Access Control
- **Admin users** can:
  - View all messages
  - Add new messages

- **Read-only users** can:
  - View all messages

### 4. Responsive UI
- Modern React-based user interface
- Mobile-friendly design
- Intuitive navigation and user experience

## Tech Stack

- **Frontend**: React.js
- **Backend**: Python (Flask)
- **Authentication**: JWT-based token system
- **Data Storage**: File-based storage (JSON)
- **Deployment**: Docker containerization

## Project Structure

```
message-app/
├── frontend/          # React frontend application
├── backend/           # Python Flask backend API
├── Dockerfile         # Multi-stage build for the application
├── docker-compose.yml # Docker compose configuration
└── README.md          # Project documentation
```

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (optional)

### Running the Application

#### Using Docker

```bash
# Build the Docker image
docker build -t message-app .

# Run the container
docker run -p 3000:3000 -p 5000:5000 message-app

# Or use docker compose
docker-compose up --build
```
### Accessing the Application

Once the application is running:

- **Frontend UI**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:5000](http://localhost:5000)

### Default Login Credentials

| Username | Password | Role      |
| -------- | -------- | --------- |
| admin    | admin123 | Admin     |
| user     | user123  | Read-only |

## API Endpoints

| Endpoint                       | Method | Description                 | Access        |
| ------------------------------ | ------ | --------------------------- | ------------- |
| `/api/login`              | POST   | User authentication         | Public        |
| `/api/messages`                | GET    | Retrieve all messages       | Authenticated |
| `/api/messages?page=1&size=10` | GET    | Retrieve paginated messages | Authenticated |
| `/api/messages`                | POST   | Create a new message        | Admin only    |

## Development

### Local Development Setup

If you want to develop the application locally without Docker:

#### 1. **Backend setup**:
```bash
cd backend
pip install -r requirements.txt
python app.py
```
#### 2. **Frontend setup**:
```bash
cd frontend
npm install
npm start
```
### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.
