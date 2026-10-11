from src.models import MinimalSource, StudentSearchResults

IOU_THRESHOLD = 0.05


def iou(a_start: int, a_end: int, b_start: int, b_end: int) -> float:
    """Return the IoU between two character ranges."""
    start = max(a_start, b_start)
    end = min(a_end, b_end)
    intersection = max(0, end - start)
    union = max(a_end, b_end) - min(a_start, b_start)

    if union == 0:
        return 0.0
    return intersection/union


def build_results_index(
        results: StudentSearchResults) -> dict[str, list[MinimalSource]]:
    """Map each question_id to its retrieved sources."""
    index = {}
    for r in results.search_results:
        index[r.question_id] = r.retrieved_sources
    return index


def is_match(retrieved: MinimalSource, correct: MinimalSource) -> bool:
    """Returns True if both point to the same file and overlap enough."""
    if retrieved.file_path != correct.file_path:
        return False

    a_start = retrieved.first_character_index
    a_end = retrieved.last_character_index
    b_start = correct.first_character_index
    b_end = correct.last_character_index
    iou_match = iou(a_start, a_end, b_start, b_end)
    if (iou_match >= IOU_THRESHOLD):
        return True
    return False


def hit_at_k(
        retrieved: list[MinimalSource],
        correct: list[MinimalSource], k: int) -> bool:
    """Return True if any of the first k retrieved sources
        matches any correct source."""
    ...
