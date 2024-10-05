# Django Task Management API

## Overview

This project is a **Task Management API** built with **Django** and **Django REST Framework (DRF)**. The API allows users to manage tasks by creating, updating, deleting, and marking tasks as complete or incomplete. Additionally, it supports advanced features like task filtering, task categories, task collaboration, recurring tasks, and more. The application uses a custom user model for authentication, supports token-based authentication (using JWT), and is deployed on **Heroku**.

## Features

### Core Task Management (CRUD):
- **Create** tasks with attributes like title, description, due date, priority level, and status.
- **Read** tasks, view detailed information, and filter by attributes such as status, priority, and due date.
- **Update** tasks, modify task attributes, or mark tasks as complete or incomplete.
- **Delete** tasks from the system.

### User Management:
- Users can **sign up, log in, and manage their own tasks**.
- **Authentication** is required for managing tasks, and users can only see their own tasks.
- Supports **JWT token-based authentication** for secure API access.

### Task Categories:
- Users can create and assign tasks to specific categories (e.g., Work, Personal).

### Recurring Tasks:
- Users can create **recurring tasks** that regenerate after completion (e.g., daily, weekly).

### Task Collaboration:
- Tasks can be **shared** with collaborators, allowing multiple users to view or edit the task.

### Task History:
- A history of completed tasks is maintained, and users can track their task completion over time.

### Task Filters & Sorting:
- Filter tasks by **status (pending/completed)**, **priority**, and **due date**.
- Sort tasks by **due date** or **priority level**.