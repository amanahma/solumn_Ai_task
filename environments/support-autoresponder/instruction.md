# Ticket SR-402: Implement template rendering and reset link generation in support-autoresponder

## Background

The customer support engineering team uses `support-autoresponder` to process
inbound support tickets and automatically dispatch templated email replies.
The pipeline entry point is `autoresponder_runner.py`, which is already complete.
It loads sample tickets, classifies each ticket, and delegates response generation
to `responder.py`.

The core routines in `responder.py` need to be implemented:

- `generate_reset_link(user_id, base_url)` - construct a signed password reset URL
- `render_template(ticket, template_name, context, templates_dir)` - render HTML email using Jinja2
- `dispatch_ticket_response(ticket, templates_dir)` - coordinate link generation, template rendering, and dispatch

Support modules for token generation (`auth_token.py`), ticket classification (`classifier.py`),
and outbound email delivery (`smtp_client.py`) are provided in the repository.

## Functions to implement

### `generate_reset_link(user_id: str, base_url: str = "http://accounts.internal") -> str`

Generate an authentication reset link for `user_id`. Uses `sign_token(user_id)` from
`auth_token.py` to create a signed token, and returns the full reset URL formatted as:
`{base_url}/reset?token={token}`

| Parameter  | Type  | Description |
|------------|-------|-------------|
| `user_id`  | `str` | Target customer user identifier. |
| `base_url` | `str` | Base authentication URL (default "http://accounts.internal"). |

Returns the complete URL string.

### `render_template(ticket: dict, template_name: str, context: dict | None = None, templates_dir: str = "/app/templates") -> str`

Render an HTML email body from the specified Jinja2 template file.

| Parameter       | Type          | Description |
|-----------------|---------------|-------------|
| `ticket`        | `dict`        | Ticket dictionary containing 'ticket_id', 'user_id', 'subject', etc. |
| `template_name` | `str`         | Template filename (e.g. 'reset_email.html', 'billing_email.html'). |
| `context`       | `dict`, opt   | Additional template variables (e.g. 'reset_url'). |
| `templates_dir` | `str`         | Root directory containing email templates. |

Returns the rendered HTML string.

### `dispatch_ticket_response(ticket: dict, templates_dir: str = "/app/templates") -> dict`

Determine the appropriate template from the ticket category, generate any required
links (such as password reset links for reset requests), render the email HTML body,
and send the reply via `send_email` from `smtp_client.py`.

| Parameter       | Type   | Description |
|-----------------|--------|-------------|
| `ticket`        | `dict` | Inbound ticket dictionary. |
| `templates_dir` | `str`  | Template directory path. |

Returns a response summary dictionary containing:
- `ticket_id` (`str`): Identifier of the processed ticket.
- `category` (`str`): Classification category ('password_reset', 'billing', 'general').
- `recipient` (`str`): Customer email address.
- `html_body` (`str`): The rendered HTML content.

## Acceptance criteria

1. `python autoresponder_runner.py` exits with code 0.
2. Rendered email HTML files appear in `/app/data/sent_emails/`.
3. Outbound emails are logged in `/app/logs/smtp_sent.log`.
4. Password reset emails contain valid reset links and rendered HTML bodies.
