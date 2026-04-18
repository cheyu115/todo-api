# Todo API Action Mapping - Request/Response Examples

## 1. GET /todos - List all todos

### Request
- **Method**: GET
- **URL**: `/todos`
- **Query Parameters** (optional):
  - `page` - Page number for pagination
  - `limit` - Number of items per page

### Response (200 OK)
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Complete API design documentation",
      "description": "Design the REST API endpoints and data models for the todo application",
      "is_completed": false,
      "created_at": "2026-04-17T10:30:00Z",
      "updated_at": "2026-04-17T14:25:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 1
  }
}
```

---

## 2. POST /todos - Create a new todo

### Request
- **Method**: POST
- **URL**: `/todos`
- **Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, vegetables",
  "is_completed": false
}
```

### Response (201 Created)
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, vegetables",
  "is_completed": false,
  "created_at": "2026-04-18T09:00:00Z",
  "updated_at": "2026-04-18T09:00:00Z"
}
```

---

## 3. GET /todos/{id} - Get a specific todo

### Request
- **Method**: GET
- **URL**: `/todos/550e8400-e29b-41d4-a716-446655440000`

### Response (200 OK)
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Complete API design documentation",
  "description": "Design the REST API endpoints and data models for the todo application",
  "is_completed": false,
  "created_at": "2026-04-17T10:30:00Z",
  "updated_at": "2026-04-17T14:25:00Z"
}
```

---

## 4. PATCH /todos/{id} - Update a todo

### Request
- **Method**: PATCH
- **URL**: `/todos/550e8400-e29b-41d4-a716-446655440000`
- **Request Body** (only fields to update - optional fields):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "is_completed": true
}
```

**Available optional fields for PATCH:**
- `title` - Task description (max 200 chars)
- `description` - Detailed description (max 1000 chars)
- `is_completed` - Boolean flag indicating completion status

**Notes:**
- Only include fields that need to be updated
- Omitted fields remain unchanged
- At least one field must be provided in the request body

### Response (200 OK)
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Complete API design documentation",
  "description": "Design the REST API endpoints and data models for the todo application",
  "is_completed": true,
  "created_at": "2026-04-17T10:30:00Z",
  "updated_at": "2026-04-18T10:30:00Z"
}
```

---

## 5. DELETE /todos/{id} - Delete a todo

### Request
- **Method**: DELETE
- **URL**: `/todos/550e8400-e29b-41d4-a716-446655440000`

### Response (204 No Content)
```
(Empty body)
```