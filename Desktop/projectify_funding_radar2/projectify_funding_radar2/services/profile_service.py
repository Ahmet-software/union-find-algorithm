"""Aktif kullanıcı profilini kaydeder/yükler. Tek aktif profil tutulur."""
from __future__ import annotations

from typing import Any, Optional, Tuple

from database import ProfileRow, dumps, get_session, loads
from models import AcademicProfile, CompanyProfile, EntrepreneurProfile

_MODEL_BY_TYPE = {
    "company": CompanyProfile,
    "academic": AcademicProfile,
    "entrepreneur": EntrepreneurProfile,
}


def save_profile(user_type: str, profile: Any) -> None:
    with get_session() as s:
        s.query(ProfileRow).delete()  # tek aktif profil
        row = ProfileRow(user_type=user_type, data_json=dumps(profile.model_dump()))
        s.add(row)
        s.commit()


def load_profile() -> Tuple[Optional[str], Optional[Any]]:
    with get_session() as s:
        row = s.query(ProfileRow).order_by(ProfileRow.id.desc()).first()
        if not row:
            return None, None
        model_cls = _MODEL_BY_TYPE.get(row.user_type)
        if not model_cls:
            return row.user_type, None
        data = loads(row.data_json, {})
        return row.user_type, model_cls(**data)


def has_profile() -> bool:
    utype, profile = load_profile()
    return profile is not None
