-- Stage 4: Learn your first SQL by hand
-- Run against tasks.db

-- 1. List every task
SELECT * FROM tasks;
-- Output:
-- 1 | Buy milk | 0
-- 2 | Read FastAPI docs | 1
-- 3 | Build CRUD API assignment | 0

-- 2. Only completed tasks
SELECT * FROM tasks WHERE done = 1;
-- Output:
-- 2 | Read FastAPI docs | 1

-- 3. How many tasks are there?
SELECT COUNT(*) FROM tasks;
-- Output:
-- 3

-- 4. Mark every task completed
UPDATE tasks SET done = 1;
-- Output: Rows updated: 3 (API immediately reflects all tasks done: true)

-- 5. Delete all completed tasks
DELETE FROM tasks WHERE done = 1;
-- Output: Rows deleted: 3 (API immediately reflects [] empty array)
