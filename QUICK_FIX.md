# Quick Fix - Database Setup

## The Problem
You're getting "no such table: accounts_user" because migrations haven't been run yet.

## Solution - Run These Commands in Order:

### Step 1: Create Migration Files
```bash
python manage.py makemigrations
```

### Step 2: Apply Migrations (Create Tables)
```bash
python manage.py migrate
```

### Step 3: Create Admin User
```bash
python manage.py createsuperuser
```

### Step 4: Start Server
```bash
python manage.py runserver
```

## What Each Command Does:

1. **makemigrations** - Creates migration files based on your models
2. **migrate** - Actually creates the database tables in SQLite
3. **createsuperuser** - Creates an admin account (only works after tables exist)
4. **runserver** - Starts the development server

## Important Order:
You MUST run `migrate` before `createsuperuser`!

The error happened because you tried to create a user before the database tables existed.
