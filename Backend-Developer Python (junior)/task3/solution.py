def intersect_intervals(intervals):
    """Находит пересечение множества интервалов."""
    if not intervals:
        return []

    # Начинаем с первого интервала
    result = intervals[0]
    for interval in intervals[1:]:
        # Находим пересечение двух интервалов
        start = max(result[0], interval[0])
        end = min(result[1], interval[1])
        if start < end:
            result = [start, end]
        else:
            return []  # Если нет пересечения, возвращаем пустой результат

    return result

def merge_intervals(intervals):
    """Объединяет пересекающиеся или соприкасающиеся интервалы."""
    if not intervals:
        return []

    sorted_intervals = sorted(intervals)
    merged = [sorted_intervals[0]]

    for start, end in sorted_intervals[1:]:
        last_end = merged[-1][1]
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])

    return merged

def calculate_overlap(intervals_a, intervals_b):
    """Вычисляет пересечение двух множеств интервалов и их суммарную длину."""
    overlaps = []
    for a_start, a_end in intervals_a:
        for b_start, b_end in intervals_b:
            start = max(a_start, b_start)
            end = min(a_end, b_end)
            if start < end:
                overlaps.append([start, end])
    return overlaps

def appearance(intervals: dict[str, list[int]]) -> int:
    # Формируем интервалы урока, ученика и учителя
    lesson = [[intervals['lesson'][0], intervals['lesson'][1]]]
    pupil_intervals = [[intervals['pupil'][i], intervals['pupil'][i+1]] for i in range(0, len(intervals['pupil']), 2)]
    tutor_intervals = [[intervals['tutor'][i], intervals['tutor'][i+1]] for i in range(0, len(intervals['tutor']), 2)]

    # Объединяем пересекающиеся интервалы
    pupil_merged = merge_intervals(pupil_intervals)
    tutor_merged = merge_intervals(tutor_intervals)

    # Находим пересечения ученика и учителя
    pupil_tutor_overlap = calculate_overlap(pupil_merged, tutor_merged)

    # Находим пересечения с уроком
    lesson_overlap = calculate_overlap(pupil_tutor_overlap, lesson)

    # Вычисляем общую длительность пересечений
    total_time = sum(end - start for start, end in lesson_overlap)
    return total_time

# Тесты
tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]


if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
       print(f'Test case {i}: Total overlap time = {test_answer} seconds')
   print("All tests passed!")
