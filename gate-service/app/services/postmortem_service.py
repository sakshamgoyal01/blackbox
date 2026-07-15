from pathlib import Path

from app.crud.postmortem import (
    get_incident,
    get_timeline,
    save_postmortem,
)

TEMPLATE = (
    Path(__file__)
    .parent.parent
    / "templates"
    / "postmortem_template.md"
)


def draft_postmortem(
    db,
    incident_id,
):

    incident = get_incident(
        db,
        incident_id,
    )

    timeline = get_timeline(
        db,
        incident_id,
    )

    template = TEMPLATE.read_text()

    timeline_md = ""

    detection = "None"

    for entry in timeline:

        timeline_md += (
            f"- {entry.created_at} "
            f"{entry.entry_type.value}: "
            f"{entry.content}\n"
        )

        if detection == "None":
            detection = (
                f"{entry.entry_type.value}: "
                f"{entry.content}"
            )

    markdown = (
        template
        .replace(
            "{{title}}",
            incident.title,
        )
        .replace(
            "{{service}}",
            incident.service or "N/A",
        )
        .replace(
            "{{severity}}",
            incident.severity.value,
        )
        .replace(
            "{{status}}",
            incident.status.value,
        )
        .replace(
            "{{opened_at}}",
            str(incident.opened_at),
        )
        .replace(
            "{{resolved_at}}",
            str(incident.resolved_at),
        )
        .replace(
            "{{summary}}",
            incident.summary or "",
        )
        .replace(
            "{{timeline}}",
            timeline_md,
        )
        .replace(
            "{{detection}}",
            detection,
        )
    )

    save_postmortem(
        db,
        incident,
        markdown,
    )

    return {
        "incident_id": str(
            incident.id,
        ),
        "postmortem": markdown,
    }