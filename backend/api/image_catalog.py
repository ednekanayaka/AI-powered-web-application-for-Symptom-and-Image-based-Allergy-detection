MEAL_DEFAULT_IMAGE = "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=1200&q=80"
EXERCISE_DEFAULT_IMAGE = "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=1200&q=80"

MEAL_IMAGE_RULES = [
    (("oat", "oatmeal", "granola"), "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?auto=format&fit=crop&w=1200&q=80"),
    (("yogurt", "parfait"), "https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=1200&q=80"),
    (("smoothie",), "https://images.unsplash.com/photo-1502741224143-90386d7f8c82?auto=format&fit=crop&w=1200&q=80"),
    (("egg", "omelette", "scramble"), "https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=1200&q=80"),
    (("toast", "bread", "sandwich", "wrap"), "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=1200&q=80"),
    (("salad", "quinoa", "chickpea"), "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1200&q=80"),
    (("chicken", "turkey"), "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1200&q=80"),
    (("fish", "salmon", "cod", "tilapia", "shrimp", "tuna", "seafood"), "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=1200&q=80"),
    (("beef", "steak", "lamb", "pork"), "https://images.unsplash.com/photo-1600891964599-f61ba0e24092?auto=format&fit=crop&w=1200&q=80"),
    (("pasta", "noodle"), "https://images.unsplash.com/photo-1473093226795-af9932fe5856?auto=format&fit=crop&w=1200&q=80"),
    (("pancake", "waffle"), "https://images.unsplash.com/photo-1528207776546-365bb710ee93?auto=format&fit=crop&w=1200&q=80"),
    (("pizza", "taco", "burrito"), "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1200&q=80"),
    (("soup", "stew"), "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1200&q=80"),
]

EXERCISE_IMAGE_RULES = [
    (("yoga", "stretch"), "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=1200&q=80"),
    (("walk", "jog", "run", "cardio", "treadmill", "cycle", "cycling", "swim"), "https://images.unsplash.com/photo-1538805060514-97d9cc17730c?auto=format&fit=crop&w=1200&q=80"),
    (("rope", "jump"), "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=1200&q=80"),
    (("plank", "core", "abs"), "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=1200&q=80"),
    (("squat", "leg"), "https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?auto=format&fit=crop&w=1200&q=80"),
    (("bench", "press", "deadlift", "pull", "push", "row", "burpee", "hiit"), "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1200&q=80"),
]


def get_image_url_for_title(title, kind="meal"):
    normalized = (title or "").lower()
    rules = MEAL_IMAGE_RULES if kind == "meal" else EXERCISE_IMAGE_RULES
    default = MEAL_DEFAULT_IMAGE if kind == "meal" else EXERCISE_DEFAULT_IMAGE

    for keywords, url in rules:
        if any(keyword in normalized for keyword in keywords):
            return url

    return default
