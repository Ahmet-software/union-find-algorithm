"""Clear / Taramaları Sil — doküman bölüm 21 & 29."""
from __future__ import annotations

from database import FundingCallRow, MatchResultRow, get_session

CONFIRM_TEXT = (
    "Tüm tarama sonuçları ve uygunluk skorları silinecek. "
    "Kullanıcı profili ve proje özeti korunacaktır. "
    "Bu işlem geri alınamaz. Devam etmek istiyor musunuz?"
)


def clear_scan_results(db_session=None) -> dict:
    """
    Taranmış çağrıları ve eşleşme sonuçlarını temizler.
    Kullanıcı profili ve proje özetlerini SİLMEZ.
    """
    own = db_session is None
    s = db_session or get_session()
    try:
        calls_deleted = s.query(FundingCallRow).delete()
        results_deleted = s.query(MatchResultRow).delete()
        s.commit()
        return {"calls_deleted": calls_deleted, "results_deleted": results_deleted}
    finally:
        if own:
            s.close()
