# MSc Project Report Outline

## Title
Service Desk Ticket Management and SLA Analytics System using Python Django

## Chapter 1 — Introduction
- Background: service teams need a consistent way to record, assign and track requests.
- Problem statement: spreadsheet/email-based tracking can make ownership, ageing and SLA performance difficult to monitor.
- Aim: develop a web application that centralizes ticket management and provides basic SLA reporting.
- Objectives:
  1. Implement authentication.
  2. Create and maintain service tickets.
  3. Assign priorities and support staff.
  4. calculate illustrative SLA due dates and measure SLA outcomes.
  5. Build dashboard charts and CSV reports.
- Scope and limitations.

## Chapter 2 — Literature / Existing System Study
Describe manual spreadsheets, email queues, and typical ticketing systems. Compare them by ownership, traceability, reporting and ease of use. Cite only sources you actually read.

## Chapter 3 — Requirements Analysis
### Functional requirements
Login/logout; ticket CRUD; status and priority; assignment; comments; search/filter; dashboard; CSV export; admin management.

### Non-functional requirements
Usability, data integrity, maintainability, authentication, basic performance and readable reporting.

### User roles
For the current prototype, authenticated users can manage tickets and admins can use Django admin. Explain that a production system would require stricter requester/agent/admin permissions.

## Chapter 4 — System Design
Include:
- Architecture: Browser → Django views/forms → Django ORM → SQLite
- Use-case diagram: User logs in, creates ticket, updates ticket, adds comment, views dashboard, exports report; admin manages users and records.
- ER diagram: User 1—many Tickets as requester; User 0/1—many Tickets as assignee; Ticket 1—many TicketComments; User 1—many TicketComments.
- Data dictionary from the table below.
- UI wireframes and navigation flow.

## Chapter 5 — Implementation
Explain environment setup, models, forms, views, URL routing, templates, authentication, dashboard aggregation, SLA calculation and CSV generation. Add selected code snippets with explanations, not every line of code.

## Chapter 6 — Testing
Document test case ID, scenario, steps/input, expected result, actual result and Pass/Fail. Attach screenshots of actual results. Never claim a test passed unless you ran it.

## Chapter 7 — Results and Discussion
Show dashboard screenshots and sample reports. Use synthetic data. Explain trends observed in the sample dataset and distinguish demo observations from real-world findings.

## Chapter 8 — Conclusion and Future Enhancements
Conclusion against each objective. Future work: role-based permissions, business-hours SLA calendars, email notifications, pagination, audit logs, PostgreSQL, API integration and deployment.

## Data dictionary (main fields)
| Entity | Field | Meaning |
|---|---|---|
| Ticket | id | Unique database key |
| Ticket | title | Short issue summary |
| Ticket | description | Detailed issue description |
| Ticket | category | Type of issue |
| Ticket | priority | Low/Medium/High/Critical |
| Ticket | status | Open/In Progress/Resolved/Closed |
| Ticket | requester_id | User who created the ticket |
| Ticket | assigned_to_id | User responsible for handling it |
| Ticket | created_at | Ticket creation timestamp |
| Ticket | due_at | SLA target timestamp |
| Ticket | resolved_at | Resolution timestamp |
| TicketComment | ticket_id | Ticket associated with the note |
| TicketComment | author_id | User who wrote the note |
| TicketComment | body | Update or resolution note |

## Example test cases
| ID | Test | Expected result |
|---|---|---|
| TC-01 | Open dashboard without login | Redirect to login |
| TC-02 | Login with valid superuser | Dashboard opens |
| TC-03 | Create high-priority ticket | Ticket saved; due date is 8 hours after creation |
| TC-04 | Search for a ticket title | Matching ticket appears |
| TC-05 | Filter by priority | Only matching priority tickets appear |
| TC-06 | Export CSV | Browser downloads CSV with ticket columns |
| TC-07 | Add comment | Comment appears on ticket detail |
| TC-08 | Delete ticket and confirm | Ticket and its comments are removed |

## Suggested appendices
- Installation guide
- Selected source code
- Test evidence screenshots
- Sample CSV report
- User guide
- GitHub repository URL
