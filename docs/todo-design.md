# Todo API Design - Step 1: Data Structure

## Fields

A todo resource should contain the following fields:

### fields:
- **id** (string/UUID): Unique identifier for the todo item
- **title** (string): Short description of the task (max 200 chars)
- **description** (string): Detailed description of the task (max 1000 chars)
- **is_completed** (boolean): Flag to check whether the task is completed
- **created_at** (datetime): Timestamp when the todo was created
- **updated_at** (datetime): Timestamp when the todo was last updated

## Actions Apply to Todo Resource

### Collection Actions (on /todos endpoint):
1. **GET /todos** - List all todos with optional filtering and pagination
2. **POST /todos** - Create a new todo item

### Member Actions (on /todos/{id} endpoint):
3. **GET /todos/{id}** - Retrieve a specific todo item
4. **PATCH /todos/{id}** - Update a todo item
5. **DELETE /todos/{id}** - Delete a todo item