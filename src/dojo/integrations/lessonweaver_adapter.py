"""lessonweaver adapter.

TODO: Replace with real reviewed lesson generation + approval workflows.
"""

from dojo.lessons.reviewed_lessons import REVIEWED_LESSONS


def get_reviewed_lessons() -> list[str]:
    return REVIEWED_LESSONS
