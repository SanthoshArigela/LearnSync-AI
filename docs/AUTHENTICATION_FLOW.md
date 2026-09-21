# LearnSync AI — Authentication & Role-Based Routing Architecture

**LearnSync AI** is a general-purpose, AI-powered education web application connecting students, personalized learning intelligence, and faculty.

This document details the primary web application authentication flow, role-based route protection, session management, backend API endpoints, and production JWT extensibility.

---

## 1. Primary Web Authentication Architecture

The LearnSync AI Web Application (`teacher-dashboard`) serves as the central entry point for all users. Access to student and faculty features is controlled via client-side role-based routing and FastAPI backend authentication.

```
                      UNAUTHENTICATED USER
                               │
                               ▼
                        WEB ROUTE: /login
               ┌───────────────────────┐
               │ LearnSync AI Login UI │
               │  [ Student ] [ Faculty]│
               └───────────┬───────────┘
                           │
                           ▼
                 POST /api/auth/login
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
      ROLE == "STUDENT"           ROLE == "FACULTY"
             │                           │
             ▼                           ▼
      WEB ROUTE: /student/*       WEB ROUTE: /faculty/*
     (Student Web Application)   (Teacher Web Dashboard)
```

---

## 2. Controlled Demo Credentials

For hackathon demonstration and testing, safe controlled demo credentials are provided:

| Role | Email | Password | Allowed Web Routes | Default Land |
| :--- | :--- | :--- | :--- | :--- |
| **Student** | `student@learnsync.ai` | `student123` | `/student/*` (`/student/home`, `/student/tutor`, `/student/vision`, `/student/voice`, `/student/assessments`, `/student/progress`, `/student/profile`) | `/student/home` |
| **Faculty** | `faculty@learnsync.ai` | `faculty123` | `/faculty/*` (`/faculty/dashboard`, `/faculty/students`, `/faculty/topics`, `/faculty/assessments`, `/faculty/recommendations`, `/faculty/profile`) | `/faculty/dashboard` |

> *Note:* Credentials are for demonstration purposes only. Zero real credentials or secret keys are stored in source code.

---

## 3. Role-Based Route Protection Rules

1. **Unauthenticated Redirect**:
   - Any user attempting to access `/student/*` or `/faculty/*` without an active session is automatically redirected to `/login`.

2. **Student Access Control**:
   - Users logged in with `ROLE: STUDENT` are restricted to `/student/*`.
   - Attempting to manually navigate to `/faculty/*` or `/login` automatically redirects back to `/student/home`.

3. **Faculty Access Control**:
   - Users logged in with `ROLE: FACULTY` are restricted to `/faculty/*`.
   - Attempting to manually navigate to `/student/*` or `/login` automatically redirects back to `/faculty/dashboard`.

4. **Session Persistence & Page Refresh**:
   - Session state (`learnsync_session`) is persisted in `localStorage`.
   - Refreshing the browser preserves the active session and retains current route context.

5. **Logout Execution**:
   - Triggering **Sign Out** clears `localStorage` session state and redirects immediately to `/login`.

---

## 4. Backend Authentication Endpoint Specification

### `POST /api/auth/login`

**Request Body**:
```json
{
  "email": "student@learnsync.ai",
  "password": "student123",
  "role": "student"
}
```

**Success Response (HTTP 200 OK)**:
```json
{
  "authenticated": true,
  "user": {
    "id": "std_001",
    "name": "Santhosh",
    "email": "student@learnsync.ai",
    "role": "student"
  },
  "message": "Login successful"
}
```

**Failure Response (HTTP 401 Unauthorized)**:
```json
{
  "detail": "Invalid email or password for the selected role"
}
```

---

## 5. Security Considerations & Production JWT Upgrade Path

### Current Demo Authentication Scope
- Uses in-memory credential evaluation in `AuthService` (`backend/app/services/auth_service.py`).
- Client-side `localStorage` session management for hackathon simplicity.

### Upgrading to Production Security
1. **Password Hashing**:
   - Replace plaintext comparison with `passlib[bcrypt]` salted hash verification.
2. **JSON Web Tokens (JWT)**:
   - Issue signed `access_token` and `refresh_token` upon successful authentication (`PyJWT` / `python-jose`).
   - Store JWT in `HttpOnly`, `SameSite=Strict`, `Secure` cookies to prevent XSS credential theft.
3. **Database Integration**:
   - Connect `AuthService` to PostgreSQL/SQLAlchemy user database.
4. **Role Middleware Guards**:
   - Add FastAPI `Depends(get_current_user_with_role("faculty"))` dependency guards on sensitive endpoints.
