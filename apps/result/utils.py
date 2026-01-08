def score_grade(score):
    if score <= 10:
        return "A"


def get_mention(avg):
    if avg < 8:
        return "Médiocre"
    elif avg < 10:
        return "Passable"
    elif avg < 12:
        return "Assez Bien"
    elif avg < 14:
        return "Bien"
    else:
        return "Très Bien"
