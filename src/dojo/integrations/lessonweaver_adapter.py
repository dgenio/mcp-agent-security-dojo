"""lessonweaver adapter.

LOCAL REFERENCE IMPLEMENTATION — this is NOT the real library. The real
``lessonweaver`` (install from ``git+https://github.com/dgenio/lessonweaver.git``;
not on PyPI) provides ``LessonDetector`` and governance promotion over traces;
this file returns a static list. See ``docs/library-map.md``.

TODO: Replace with real trace-driven lessonweaver pipeline (tracked in #24).
"""

from dojo.lessons.reviewed_lessons import REVIEWED_LESSONS


def get_reviewed_lessons() -> list[str]:
    return REVIEWED_LESSONS
