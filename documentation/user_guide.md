# User Guide

1. Start the Django development server.
2. Sign in with the account created using `createsuperuser`.
3. Use **New ticket** to record a service request.
4. Complete title, description, category, priority and optional assignee.
5. Open a ticket to view its SLA due time, current SLA state and comments.
6. Use **Edit** to update priority, status or assignment.
7. Add updates/resolution notes on the detail page.
8. Use **Tickets** to search and filter.
9. Select **Export CSV** to download a spreadsheet-friendly report.
10. Use the dashboard to review volume, status, priority, category and SLA indicators.

## Demo scenario
Create a user account for an agent in Django admin. Create a High-priority ticket. The default SLA target is eight elapsed hours after ticket creation. Assign it to the agent, add a comment, and move it to Resolved. The SLA result depends on whether it was resolved before the due timestamp.
