class Highscore:
    """Keep track of a single high score.

    Attributes:
        name (str): name of player
        score (int): score
    """

    def __init__(self, name, score):
        """Init the highscore.

        Saves name, score.

        Args:
            name (str): name of player
            score (str): score of this game
        """
        self.name = name
        self.score = float(score)


class Highscores:
    """Manage a list of highscores.

    Attributes:
        fname (str): filename where highscores are stored.
        scores (list): list of previous scores
    """

    def __init__(self, fname=None):
        """Init the list.

        Args:
            fname (str, optional): filename whre previous scores
                                   are/will be stored.
        """
        self.scores = []

        if fname is None:
            fname = "high.txt"
        self.readFile(fname)

    def readFile(self, fname):
        """Read the highscores file.

        Args:
            fname (str): file to read

        Returns:
            None
        """
        self.scores = []
        self.fname = fname
        try:
            with open(fname, 'r') as f:
                for line in f:
                    self.appendScore(line.split(' '))
        except:
            pass

    def appendScore(self, l):
        """Append a highscore to the list.

        Args:
            l (list): list of highscore data (0: name, 1: score)

        Returns:
            None
        """
        score = Highscore(l[0], l[1])
        self.scores.append(score)

    def writeOut(self):
        """Write highscores to file.

        Overwrites old data.

        Returns:
            None
        """
        with open(self.fname, 'w') as f:
            for i in range(10):
                score = self.getNextHighest()
                if score is not None:
                    f.write('%s %s\n' % (score.name,
                                         score.score))
                    pass

    def getNextHighest(self):
        """Get the next highest highscore.

        Return it and delete it.

        Returns:
            int: next highest score
        """
        maxScore = -1
        idx = -1
        for i, s in enumerate(self.scores):
            if s.score > maxScore:
                maxScore = s.score
                idx = i
        if idx != -1:
            score = self.scores[idx]
            del self.scores[idx]
            return score
        else:
            return None

    def isHighscore(self, score):
        """Check if a score is high enough to be a highscore.

        Args:
            score (Highscore): highscore to check

        Returns:
            bool: True if the score is high enough
        """
        score = float(score)
        if len(self.scores) < 10:
            return True

        lowest = float('inf')
        for s in self.scores:
            if s.score < lowest:
                lowest = s.score
        if score > lowest:
            return True
        else:
            return False
