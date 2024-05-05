from fastapi import APIRouter, status

from app.admin.contact import send_email
from app.models.contact import Contact

router = APIRouter(
    prefix="/contact",
    tags=["contact"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_message(contact: Contact):
    subject = f"New message from {contact.name}"
    body = f"From: {contact.email}\n\n{contact.message}"
    send_email(subject, body)
