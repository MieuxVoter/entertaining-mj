from jm_utils import JMResults

JM_RESULTS = dict(
    michel=(10.5, 20.5, 30.5, 38.5),
    marcel=(8, 18, 40, 34),
    rosalie=(12, 22, 32, 34),
)

DEFAULT_VOTE = JMResults(JM_RESULTS, (1, 2, 0), grades=["Excellent", "Bien", "Passable", "Insuffisant"])

SAME_REJECT_VOTE = JMResults(JM_RESULTS, (1, 2, 0), grades=["Excellent", "Bien", "Passable", "Insuffisant"])

JM_RESULTS = dict(
    michel=(55, 20, 5, 20),
    marcel=(20, 10, 30, 40),
    rosalie=(30, 30, 6, 34),
)

EASY_VOTE = JMResults(JM_RESULTS, (0, 2, 1), grades=["Excellent", "Bien", "Passable", "Insuffisant"])

JM_RESULTS = dict(
    michel=(5, 50, 20, 5, 20),
    marcel=(7, 13, 10, 30, 40),
    rosalie=(28, 10, 22, 6, 34),
)

EASY_VOTE_2 = JMResults(JM_RESULTS, (0, 2, 1), grades=["Excellent", "Très bien", "Bien", "Passable", "Insuffisant"])

JM_RESULTS = dict(
    michel=(5, 50, 20, 5, 20),
    marcel=(9, 43, 10, 28, 10),
    rosalie=(28, 10, 22, 6, 34),
)

EASY_VOTE_SECOND_GRADE = JMResults(
    JM_RESULTS, (0, 2, 1), grades=["Excellent", "Très bien", "Bien", "Passable", "Insuffisant"]
)


JM_RESULTS = dict(
    michel=(15, 45, 5, 20),
    marcel=(20, 45, 15, 20),
    rosalie=(25, 40, 20, 15),
)

SAME_REJECT_VOTE_AGAIN = JMResults(JM_RESULTS, (1, 2, 0), grades=["Excellent", "Bien", "Passable", "Insuffisant"])
