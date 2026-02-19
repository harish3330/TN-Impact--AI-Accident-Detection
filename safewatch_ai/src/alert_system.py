"""Multi-channel alert manager – snapshots, email, sound."""

import logging
import os
import smtplib
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from pathlib import Path
from typing import Dict, Optional

import cv2
import numpy as np
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class AlertManager:
    """Save snapshots, play sounds, and email alerts for safety incidents."""

    def __init__(self, incident_dir: str = "data/incidents"):
        self.incident_dir = Path(incident_dir)
        self.incident_dir.mkdir(parents=True, exist_ok=True)

        # SMTP settings from .env
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("ALERT_EMAIL", "")
        self.sender_password = os.getenv("ALERT_PASSWORD", "")

        # Cooldown tracking  {alert_key: last_datetime}
        self._last_alert: Dict[str, datetime] = {}
        self.cooldown_seconds = 30

        if self.sender_email and self.sender_password:
            logger.info("Email alerts enabled (%s)", self.sender_email)
        else:
            logger.warning("Email alerts disabled (ALERT_EMAIL / ALERT_PASSWORD missing)")

    # ── public API ──────────────────────────────────────────────────

    def send_alert(self, incident: Dict, frame: np.ndarray,
                   recipient_email: Optional[str] = None) -> bool:
        """Dispatch an alert through all channels. Returns ``True`` on success."""
        if not self._cooldown_ok(incident):
            return False

        snapshot = self._save_snapshot(frame, incident)
        self._log_alert(incident)
        self._beep(incident)

        if self.sender_email and self.sender_password:
            to = recipient_email or os.getenv("DEFAULT_ALERT_EMAIL", "")
            if to:
                self._send_email(incident, snapshot, to)

        logger.info("Alert dispatched: %s", incident.get("type"))
        return True

    def set_cooldown(self, seconds: int) -> None:
        self.cooldown_seconds = seconds

    def get_incident_history(self, limit: int = 50) -> list[str]:
        """Return paths to the most recent snapshot JPEGs."""
        files = sorted(self.incident_dir.glob("*.jpg"),
                       key=lambda p: p.stat().st_ctime, reverse=True)
        return [str(f) for f in files[:limit]]

    # ── internals ───────────────────────────────────────────────────

    def _cooldown_ok(self, incident: Dict) -> bool:
        key = f"{incident['camera_id']}_{incident['type']}"
        now = datetime.now()
        prev = self._last_alert.get(key)
        if prev and (now - prev).total_seconds() < self.cooldown_seconds:
            return False
        self._last_alert[key] = now
        return True

    def _save_snapshot(self, frame: np.ndarray, incident: Dict) -> Optional[Path]:
        """Annotate and save a JPEG snapshot of the incident."""
        try:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            name = f"{incident.get('type', 'UNK')}_{incident.get('camera_id', 'cam')}_{ts}.jpg"
            path = self.incident_dir / name

            img = frame.copy()
            x1, y1, x2, y2 = incident.get("bbox", (0, 0, 0, 0))
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            label = f"{incident.get('type')} – {incident.get('details', '')}"
            cv2.putText(img, label, (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imwrite(str(path), img)
            return path
        except Exception as exc:
            logger.error("Snapshot save failed: %s", exc)
            return None

    def _log_alert(self, incident: Dict) -> None:
        sev = incident.get("severity", "INFO")
        msg = (f"[{sev}] {incident.get('type')} | "
               f"cam={incident.get('camera_id')} | "
               f"{incident.get('details', '')}")
        (logger.critical if sev == "CRITICAL" else logger.warning)(msg)

    @staticmethod
    def _beep(incident: Dict) -> None:
        try:
            n = 3 if incident.get("severity") == "CRITICAL" else 1
            freq = 1000 if n == 3 else 800
            dur = 500 if n == 3 else 300
            for _ in range(n):
                os.system(f'powershell.exe -c "[console]::beep({freq},{dur})"')
        except Exception:
            pass

    def _send_email(self, incident: Dict, snapshot: Optional[Path],
                    recipient: str) -> bool:
        """Compose and send an HTML-free plain-text email with snapshot."""
        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = recipient
            msg["Date"] = formatdate(localtime=True)

            itype = incident.get("type", "UNKNOWN")
            ts = incident.get("timestamp", datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            msg["Subject"] = f"[ALERT] {itype} – {incident.get('camera_id', '?')} – {ts}"

            body = (
                f"Alert Type : {itype}\n"
                f"Severity   : {incident.get('severity', 'INFO')}\n"
                f"Camera     : {incident.get('camera_id', '?')}\n"
                f"Time       : {ts}\n"
                f"Details    : {incident.get('details', '-')}\n"
                f"Confidence : {incident.get('confidence', 0):.0%}\n"
                f"Track ID   : {incident.get('track_id', '-')}\n\n"
                f"-- SafeWatch AI (automated alert)"
            )
            msg.attach(MIMEText(body, "plain"))

            if snapshot and snapshot.exists():
                with open(snapshot, "rb") as fh:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(fh.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition",
                                    f"attachment; filename={snapshot.name}")
                    msg.attach(part)

            server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            logger.info("Email sent to %s", recipient)
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP auth failed – use a Gmail App Password "
                         "(https://myaccount.google.com/apppasswords)")
            return False
        except Exception as exc:
            logger.error("Email send failed: %s", exc)
            return False
