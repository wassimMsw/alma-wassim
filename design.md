# Design Overview

## Leads Management

### Resume Upload
I created a separate API endpoint to handle resume uploads. This endpoint stores the uploaded resume and returns a unique ID. This ID is then mapped to the lead created. 

**Benefits:**
- **Separation of Concerns:** By separating resume upload from lead creation, we ensure that each endpoint has a single responsibility, making the codebase easier to maintain and extend.
- **Reusability:** The resume upload endpoint can be reused in other contexts where resume handling is required.
- **Scalability:** This design allows for easier scaling and modification, such as switching to an S3 storage solution in the future.

### Email Notifications
Emails are sent as background tasks. This approach is chosen because sending emails is not directly related to the primary purpose of the endpoint and can introduce latency. By offloading email sending to background tasks, we reduce the response time and remove dependencies.

### Authentication
JWT (JSON Web Tokens) is used for authentication. This method is secure and stateless, making it suitable for modern web applications.

### Configuration Management
Pydantic-settings is used to manage configuration settings. This ensures a smooth declaration and use of configurations across the app, promoting consistency and reducing the risk of configuration errors.

### File Storage
Resumes are stored on the host machine. However, the design is flexible enough to accommodate storing files in S3. For simplicity, the current implementation uses local storage, but adding an S3 client for reading and writing files would be straightforward.

### Database
SQLAlchemy is used for ORM (Object-Relational Mapping) and Alembic for database migrations. This combination is a common and robust choice for Python backend development.

### Admin User Creation
The first admin user is created using a script. This initial admin user can then be used to create other admin users.
