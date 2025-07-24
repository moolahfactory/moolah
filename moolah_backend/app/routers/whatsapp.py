from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging
from datetime import datetime
import os

from .. import crud, schemas
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter()


@router.get("/config")
def get_config():
    phone_number_id = os.getenv("PHONE_NUMBER_ID", "")
    return {"phone_number_id": phone_number_id}


@router.post("/whatsapp", status_code=204)
def receive_whatsapp_webhook(
    webhook: schemas.WhatsAppWebhook,
    db: Session = Depends(get_db),
):
    for entry in webhook.entry:
        for change in entry.get("changes", []):
            value = change.get("value", {})
            for msg in value.get("messages", []):
                body = msg.get("text", {}).get("body", "")
                ts = datetime.fromtimestamp(int(msg.get("timestamp", "0")))
                data = schemas.WhatsAppMessageCreate(
                    id=msg.get("id"),
                    body=body,
                    timestamp=ts,
                    **{"from": msg.get("from")},
                )
                try:
                    crud.create_whatsapp_message(db, data)
                except IntegrityError:
                    db.rollback()
                    logging.info(
                        "Duplicate WhatsApp message ignored: %s", msg.get("id")
                    )
    return None


@router.get("/whatsapp/")
def read_whatsapp_messages(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """Return messages stored from webhook."""
    messages = crud.get_whatsapp_messages(db)
    return [
        {
            "id": msg.id,
            "wa_id": msg.wa_id,
            "from": msg.from_number,
            "body": msg.body,
            "timestamp": msg.timestamp.isoformat(),
        }
        for msg in messages
    ]
