class Question:
    """Question on a questionnaire."""

    def __init__(self, question, choices=None, allow_text=False):
        """Create question (assume Yes/No for choices."""

        if not choices:
            choices = ["Yes", "No"]

        self.question = question
        self.choices = choices
        self.allow_text = allow_text


class Survey:
    """Questionnaire."""

    def __init__(self, title, slug, instructions, questions):
        """Create questionnaire."""

        self.title = title
        self.slug = slug
        self.instructions = instructions
        self.questions = questions


satisfaction_survey = Survey(
    "Customer Satisfaction Survey",
    "satisfaction",
    "Please fill out a survey about your experience with us.",
    [
        Question("Have you shopped here before?"),
        Question("Did someone else shop with you today?"),
        Question("On average, how much do you spend a month on frisbees?",
                 ["Less than $10,000", "$10,000 or more"]),
        Question("Are you likely to shop here again?"),
    ])

personality_quiz = Survey(
    "Rithm Personality Test",
    "personality",
    "Learn more about yourself with our personality quiz!",
    [
        Question("Do you ever dream about code?"),
        Question("Do you ever have nightmares about code?"),
        Question("Do you prefer porcupines or hedgehogs?",
                 ["Porcupines", "Hedgehogs"]),
        Question("Which is the worst function name, and why?",
                 ["do_stuff()", "run_me()", "wtf()"],
                 allow_text=True),
    ]
)

television_quiz = Survey(
    "Television Preferences Survey",
    "television",
    "Please tell us about your television preferences",
    [
        Question("Have you watched television before?"),
        Question("Do you enjoy television shows that have talking animals?"),
        Question("Which of these television shows do you find most appealing?",["The Office","The Great British Bake Off","It's Always Sunny in Philadelphia","Law & Order: SVU"]),
        Question("Would you enjoy a show about penguins, and what should their names be?",["Yes","Of course!"],allow_text=True)
    ]
)

surveys = {
    'satisfaction': satisfaction_survey,
    'personality': personality_quiz,
    'television': television_quiz,
}