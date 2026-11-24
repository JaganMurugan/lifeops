
CREATE TABLE IF NOT EXISTS meetings (
    meeting_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    attendees TEXT NOT NULL DEFAULT '[]',
    description TEXT,
    location TEXT,
    meeting_url TEXT
);

CREATE TABLE IF NOT EXISTS emails (
    email_id TEXT PRIMARY KEY,
    thread_id TEXT NOT NULL,
    subject TEXT NOT NULL,
    sender TEXT NOT NULL,
    recipients TEXT NOT NULL DEFAULT '[]',
    sent_at TEXT NOT NULL,
    body TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS documents (
    document_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT NOT NULL,
    tags TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    owner TEXT,
    due_date TEXT,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (
            status IN (
                'pending',
                'in_progress',
                'completed',
                'cancelled'
            )
        ),
    source_email_id TEXT,
    created_at TEXT NOT NULL,

    FOREIGN KEY (source_email_id)
        REFERENCES emails(email_id)
        ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_meetings_start_time
    ON meetings(start_time);

CREATE INDEX IF NOT EXISTS idx_emails_thread_id
    ON emails(thread_id);

CREATE INDEX IF NOT EXISTS idx_tasks_status_due_date
    ON tasks(status, due_date);
