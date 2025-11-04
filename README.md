# Faceit Cup API - Frontend Developer Documentation

## Table of Contents
- [Overview](#overview)
- [Base URLs](#base-urls)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [REST API Endpoints](#rest-api-endpoints)
  - [Auth Endpoints](#auth-endpoints)
  - [Customer Endpoints](#customer-endpoints)
  - [Chat Endpoints](#chat-endpoints)
  - [Invite Code Endpoints](#invite-code-endpoints)
- [WebSocket Endpoints](#websocket-endpoints)
  - [Customer Chat WebSocket](#customer-chat-websocket)
  - [Admin Chat WebSocket](#admin-chat-websocket)
  - [Chat Notifications WebSocket](#chat-notifications-websocket)
  - [Customer Error Status WebSocket](#customer-error-status-websocket)
- [Data Schemas](#data-schemas)
- [Enums](#enums)
- [Important Notes](#important-notes)

---

## Overview

This is the backend API for the Faceit Cup management system. It provides REST API endpoints for managing customers, chat rooms, and invite codes, as well as WebSocket endpoints for real-time chat and customer error status updates.

**You do not need to run the project locally.** The API and WebSocket services are already deployed and accessible.

---

## Base URLs

### REST API
```
https://api.cloud9-joins.com/v1
```

**⚠️ IMPORTANT:** All API endpoints have the `/v1` prefix. For example, to get chat rooms, use: `https://api.cloud9-joins.com/v1/chat/rooms`

### WebSocket
```
wss://ws.cloud9-joins.com/
```

**Note:** Use `wss://` (WebSocket Secure) because the WebSocket domain has HTTPS enabled.

---

## API Documentation

Interactive API documentation is available at:

- **Swagger UI:** [https://api.cloud9-joins.com/docs](https://api.cloud9-joins.com/docs)
- **ReDoc:** [https://api.cloud9-joins.com/redoc](https://api.cloud9-joins.com/redoc)

---

## Authentication

### Session-Based Authentication with Cookies

This API uses **session-based authentication**. The backend automatically sets authentication cookies in the response when you log in.

#### How it works:

1. **Login:** Send a POST request to `/auth/login` with username and password
2. **Backend Response:** The backend sets a session cookie (`session_token`) in the response headers
3. **Subsequent Requests:** Your browser/client automatically sends this cookie with all future requests
4. **Logout:** Send a POST request to `/auth/logout` to invalidate the session

#### Important for Frontend Developers:

- **Enable credentials in fetch/axios:**
  ```javascript
  // Using fetch
  fetch('https://api.cloud9-joins.com/v1/customers', {
    credentials: 'include'  // Important: Include cookies
  })

  // Using axios
  axios.get('https://api.cloud9-joins.com/v1/customers', {
    withCredentials: true  // Important: Include cookies
  })
  ```

- **CORS:** The backend is configured to accept credentials from your localhost during development
- **No manual token handling:** You don't need to manually store or send tokens - cookies handle everything automatically
- **Cookie name:** `session_token` (HttpOnly, Secure)

---

## REST API Endpoints

### Auth Endpoints

#### POST `/auth/login`
Login with username and password. Sets session cookie in response.

**Test Credentials:**
- Username: `admin`
- Password: `faceitcup_admin`

**Request Body:**
```json
{
  "username": "admin",
  "password": "faceitcup_admin"
}
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "user": {
    "id": 1,
    "username": "admin",
    "created_at": "2024-11-01T12:00:00"
  }
}
```

**Response Headers:**
```
Set-Cookie: session_token=<token>; HttpOnly; Secure; SameSite=None
```

---

#### POST `/auth/logout`
Logout and invalidate session. Requires authentication (session cookie).

**Response (200 OK):**
```json
null
```

---

### Customer Endpoints

#### POST `/customers`
Create a new customer using an invite code.

**Request Body:**
```json
{
  "invite_code": "ABC123"
}
```

**Response (201 Created):**
```json
1
```
*Returns the ID of the created customer*

---

#### GET `/customers`
Get list of all customers.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "hub_id": 12345678,
    "original_steam_connected": true,
    "second_steam_connected": true,
    "error_status": "success",
    "created_at": "2024-11-01T12:00:00"
  }
]
```

**⚠️ IMPORTANT:** This endpoint only returns customers where `second_steam_connected=true`.

---

#### GET `/customers/{hub_id}`
Get a specific customer by their hub_id.

**Response (200 OK):**
```json
{
  "id": 1,
  "hub_id": 12345678,
  "original_steam_connected": true,
  "second_steam_connected": true,
  "error_status": "success",
  "created_at": "2024-11-01T12:00:00"
}
```

---

#### PATCH `/customers/{hub_id}`
Update customer's steam connection status.

**Request Body:**
```json
{
  "original_steam_connected": true,
  "second_steam_connected": true
}
```

**Response (200 OK):**
```json
null
```

---

#### POST `/customers/{hub_id}/set_error`
Set customer's error status. Triggers a WebSocket notification to the customer.

**Request Body:**
```json
{
  "error_status": "checking"
}
```

**Possible values:** See [ErrorStatus Enum](#errorstatus)

**Response (200 OK):**
```json
null
```

**Side Effect:** Publishes error status update to customer's WebSocket connection (if connected).

---

### Chat Endpoints

#### GET `/chat/rooms`
Get list of all chat rooms. Requires authentication.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "customer_id": 1,
    "customer_hub_id": 12345678,
    "is_customer_in_chat": false,
    "messages_count": 5,
    "created_at": "2024-11-01T12:00:00"
  }
]
```

**⚠️ IMPORTANT:** This endpoint only returns chat rooms for customers where `second_steam_connected=true`.

---

#### GET `/chat/messages/{chat_room_id}`
Get all messages for a specific chat room. Requires authentication.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "author_type": "admin",
    "content": "Hello! How can I help you?",
    "chat_room_id": 1,
    "created_at": "2024-11-01T12:00:00"
  },
  {
    "id": 2,
    "author_type": "customer",
    "content": "I need help with my account",
    "chat_room_id": 1,
    "created_at": "2024-11-01T12:01:00"
  }
]
```

---

### Invite Code Endpoints

#### POST `/invite_codes`
Create a new invite code. Requires authentication.

**Request Body:**
```json
{
  "code": "NEWCODE123"
}
```

**Response (201 Created):**
```json
1
```
*Returns the ID of the created invite code*

---

#### GET `/invite_codes`
Get list of all invite codes. Requires authentication.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "code": "INVITE123",
    "created_at": "2024-11-01T12:00:00"
  }
]
```

---

#### DELETE `/invite_codes/{invite_code_id}`
Delete an invite code. Requires authentication.

**Response (204 No Content)**

---

## WebSocket Endpoints

All WebSocket endpoints use the base URL: `wss://ws.cloud9-joins.com/`

### Customer Chat WebSocket

**Endpoint:** `wss://ws.cloud9-joins.com/chat/customer/{chat_room_id}`

**Purpose:** Real-time chat for customers.

**Connection:**
```javascript
const ws = new WebSocket('wss://ws.cloud9-joins.com/chat/customer/1');
```

**Sending Messages:**
```javascript
// Send message to chat
ws.send(JSON.stringify({
  "content": "Hello, I need help!"
}));
```

**Receiving Messages:**
```javascript
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log(message);
};
```

**Message Format (Received):**
```json
{
  "id": 1,
  "author_type": "admin",
  "content": "Hello! How can I help you?",
  "chat_room_id": 1,
  "created_at": "2024-11-01T12:00:00"
}
```

**Connection Status:**
- When customer connects, `is_customer_in_chat` is set to `true`
- When customer disconnects, `is_customer_in_chat` is set to `false`
- A notification is broadcast to all admins via the Chat Notifications WebSocket

---

### Admin Chat WebSocket

**Endpoint:** `wss://ws.cloud9-joins.com/chat/admin/{chat_room_id}`

**Purpose:** Real-time chat for admins to communicate with customers.

**Connection:**
```javascript
const ws = new WebSocket('wss://ws.cloud9-joins.com/chat/admin/1');
```

**Sending Messages:**
```javascript
// Send message to chat
ws.send(JSON.stringify({
  "content": "I'm here to help!"
}));
```

**Receiving Messages:**
```javascript
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log(message);
};
```

**Message Format (Received):**
```json
{
  "id": 2,
  "author_type": "customer",
  "content": "I need help with my account",
  "chat_room_id": 1,
  "created_at": "2024-11-01T12:01:00"
}
```

---

### Chat Notifications WebSocket

**Endpoint:** `wss://ws.cloud9-joins.com/chat/notifications`

**Purpose:** Receive real-time notifications about chat room updates (customer connections, message counts).

**Connection:**
```javascript
const ws = new WebSocket('wss://ws.cloud9-joins.com/chat/notifications');
```

**Receiving Notifications:**
```javascript
ws.onmessage = (event) => {
  const notification = JSON.parse(event.data);

  if (notification.type === "customer_room_connection_update") {
    console.log(`Customer in room ${notification.chat_room_id} is now ${notification.connected ? 'online' : 'offline'}`);
  }

  if (notification.type === "room_messages_count_update") {
    console.log(`Room ${notification.chat_room_id} now has ${notification.room_messages_count} messages`);
  }
};
```

**Notification Types:**

1. **Customer Connection Update:**
```json
{
  "type": "customer_room_connection_update",
  "chat_room_id": 1,
  "connected": true
}
```

2. **Message Count Update:**
```json
{
  "type": "room_messages_count_update",
  "chat_room_id": 1,
  "room_messages_count": 6
}
```

**Use Case:**
- Admin dashboard can show which customers are currently online
- Update message count badges in real-time
- Notify admins when a customer joins their chat

---

### Customer Error Status WebSocket

**Endpoint:** `wss://ws.cloud9-joins.com/customer?hub_id={hub_id}`

**Purpose:** Real-time updates of customer error status changes.

**Connection:**
```javascript
const hubId = 12345678;
const ws = new WebSocket(`wss://ws.cloud9-joins.com/customer?hub_id=${hubId}`);
```

**Initial Connection Response:**
```json
{
  "status": "ok"
}
```

**Receiving Error Status Updates:**
```javascript
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  // Skip initial connection message
  if (data.status === "ok") return;

  // Handle error status update
  console.log(`Error status updated to: ${data.error_status}`);
};
```

**Error Status Update Format:**
```json
{
  "error_status": "checking"
}
```

**Possible Values:** See [ErrorStatus Enum](#errorstatus)

**Use Case:**
- Customer can see real-time updates of their account verification status
- Display current error status to the customer
- Show progress during account checks

**Example Implementation:**
```javascript
const hubId = 12345678;
const ws = new WebSocket(`wss://ws.cloud9-joins.com/customer?hub_id=${hubId}`);

ws.onopen = () => {
  console.log('Connected to error status updates');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.status === "ok") {
    console.log('Connection confirmed');
    return;
  }

  if (data.error_status) {
    updateUIWithErrorStatus(data.error_status);
  }
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected from error status updates');
};
```

---

## Data Schemas

### User
```typescript
interface User {
  id: number;
  username: string;
  created_at: string; // ISO 8601 datetime
}
```

### Customer
```typescript
interface Customer {
  id: number;
  hub_id: number; // 8-digit unique identifier
  original_steam_connected: boolean;
  second_steam_connected: boolean;
  error_status: ErrorStatus;
  created_at: string; // ISO 8601 datetime
}
```

### ChatRoom
```typescript
interface ChatRoom {
  id: number;
  customer_id: number;
  customer_hub_id: number;
  is_customer_in_chat: boolean;
  messages_count: number;
  created_at: string; // ISO 8601 datetime
}
```

### ChatMessage
```typescript
interface ChatMessage {
  id: number;
  author_type: "customer" | "admin";
  content: string;
  chat_room_id: number;
  created_at: string; // ISO 8601 datetime
}
```

### InviteCode
```typescript
interface InviteCode {
  id: number;
  code: string;
  created_at: string; // ISO 8601 datetime
}
```

---

## Enums

### ErrorStatus

Represents the current status of a customer's account verification.

```typescript
enum ErrorStatus {
  CHECKING = "checking",              // Account is being checked
  BOT_350 = "bot_350",               // Bot detected (350 level)
  BOT_800 = "bot_800",               // Bot detected (800 level)
  BOT_1300 = "bot_1300",             // Bot detected (1300 level)
  BOT_5000 = "bot_5000",             // Bot detected (5000 level)
  FAMILY_VIEW_100 = "family_view_100", // Family View restriction (100 level)
  HUB = "hub",                       // Hub-related issue
  TRADE_BAN = "trade_ban",           // Trade ban detected
  BOT_ANTI_KT = "bot_anti_kt",       // Anti-KT bot detected
  DOUBLE_SUBSTITUTION = "double_substitution", // Double substitution issue
  SUCCESS = "success"                 // Account verified successfully
}
```

### AuthorType

```typescript
enum AuthorType {
  CUSTOMER = "customer",
  ADMIN = "admin"
}
```

### NotificationType

```typescript
enum NotificationType {
  CUSTOMER_ROOM_CONNECTION_UPDATE = "customer_room_connection_update",
  ROOM_MESSAGES_COUNT_UPDATE = "room_messages_count_update"
}
```

---

## Important Notes

### Filtering

1. **Customer Listing (`GET /customers`):**
   - Only returns customers where `second_steam_connected=true`
   - Customers who haven't connected their second Steam account will not appear in this list

2. **Chat Room Listing (`GET /chat/rooms`):**
   - Only returns chat rooms for customers where `second_steam_connected=true`
   - This ensures you only see chat rooms for active customers

### WebSocket Best Practices

1. **Reconnection Logic:**
   - Implement automatic reconnection if WebSocket connection drops
   - Use exponential backoff for reconnection attempts

2. **Error Handling:**
   - Always handle `onerror` and `onclose` events
   - Display connection status to users

3. **Message Validation:**
   - Always parse JSON messages in try-catch blocks
   - Validate message structure before processing

### Example WebSocket Reconnection:
```javascript
class WebSocketClient {
  constructor(url) {
    this.url = url;
    this.reconnectDelay = 1000;
    this.maxReconnectDelay = 30000;
    this.connect();
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log('Connected');
      this.reconnectDelay = 1000; // Reset delay on successful connection
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.handleMessage(data);
      } catch (e) {
        console.error('Failed to parse message:', e);
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.ws.onclose = () => {
      console.log('Disconnected, reconnecting...');
      setTimeout(() => {
        this.reconnectDelay = Math.min(this.reconnectDelay * 2, this.maxReconnectDelay);
        this.connect();
      }, this.reconnectDelay);
    };
  }

  handleMessage(data) {
    // Your message handling logic
  }

  send(data) {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  close() {
    this.ws.close();
  }
}

// Usage
const chatWs = new WebSocketClient('wss://ws.cloud9-joins.com/chat/customer/1');
```

### CORS and Credentials

Always remember to include credentials in your requests:

```javascript
// Fetch API
const response = await fetch('https://api.cloud9-joins.com/v1/customers', {
  method: 'GET',
  credentials: 'include', // REQUIRED for cookies
  headers: {
    'Content-Type': 'application/json'
  }
});

// Axios
const response = await axios.get('https://api.cloud9-joins.com/v1/customers', {
  withCredentials: true // REQUIRED for cookies
});

// Axios global config (set once)
axios.defaults.withCredentials = true;
```

---

## Support

If you encounter any issues or have questions about the API, please contact the backend team or check the interactive API documentation at:
- [https://api.cloud9-joins.com/docs](https://api.cloud9-joins.com/docs)
