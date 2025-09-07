# Python Generators — ALX Backend

This project demonstrates **Python generators** applied to **database operations** using MySQL.

## Tasks

### 0. Stream Users
- `0-stream_users.py`
- Generator that yields users one by one from `user_data`.

### 1. Batch Processing
- `1-batch_processing.py`
- Processes users in batches (filters age > 25).

### 2. Lazy Pagination
- `2-lazy_paginate.py`
- Simulates lazy loading with pagination.

### 3. Stream Ages
- `4-stream_ages.py`
- Streams user ages and computes **average** without loading all rows.

## Setup
1. Install requirements:
   ```bash
   pip install mysql-connector-python
