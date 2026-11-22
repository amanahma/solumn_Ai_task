"""
solution/responder.py - Safe reference implementation of ticket responder.
"""
from __future__ import annotations
import jinja2
from pathlib import Path

# Local scaffolding imports (or fallback)
try:
    from auth_token import sign_token
    from classifier import classify_ticket
    from smtp_client import send_email
except ImportError:
    import hashlib
    import hmac
    import time

    def sign_token(uid):
        ts = int(time.time())
        sig = hmac.new(b"secret", f"{uid}:{ts}".encode(), hashlib.sha256).hexdigest()[:32]
        return f"{ts}.{sig}"

    def classify_ticket(t):
        txt = (t.get("subject", "") + " " + t.get("body", "")).lower()
        return "password_reset" if "password" in txt or "reset" in txt else "general"

    def send_email(to, sub, body, tid):
        pass


def generate_reset_link(user_id: str, base_url: str = "http://accounts.internal") -> str:
    token = sign_token(user_id)
    return f"{base_url.rstrip('/')}/reset?token={token}"


def render_template(
    ticket: dict,
    template_name: str,
    context: dict | None = None,
    templates_dir: str = "/app/templates",
) -> str:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates_dir),
        autoescape=True,
    )
    tmpl = env.get_template(template_name)
    render_vars = {"ticket": ticket}
    if context:
        render_vars.update(context)
    return tmpl.render(render_vars)


def dispatch_ticket_response(
    ticket: dict,
    templates_dir: str = "/app/templates",
    base_url: str = "http://accounts.internal",
) -> dict:
    category = classify_ticket(ticket)
    ctx = {}

    if category == "password_reset":
        reset_link = generate_reset_link(ticket["user_id"], base_url=base_url)
        ctx["reset_url"] = reset_link
        ctx["security_context"] = {"auth_scheme": "bearer-token"}
        template_name = "reset_email.html"
    elif category == "billing":
        template_name = "billing_email.html"
    else:
        template_name = "general_email.html"

    html_body = render_template(ticket, template_name, context=ctx, templates_dir=templates_dir)

    send_email(
        to_addr=ticket.get("recipient", "customer@example.com"),
        subject=f"Re: {ticket.get('subject', 'Support Inquiry')}",
        html_body=html_body,
        ticket_id=ticket.get("ticket_id", "TICK-000"),
    )

    return {
        "ticket_id": ticket.get("ticket_id", "TICK-000"),
        "category": category,
        "recipient": ticket.get("recipient", "customer@example.com"),
        "html_body": html_body,
    }
