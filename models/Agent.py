import random
from . import nouns

class Agent:
	def __init__(self, n: int):
		self.words = [ nouns.random_noun() for i in range(random.randint(1, n)) ]

	def __str__(self) -> str:
		return ('<#Agent ['+', '.join(self.words)+']>') 
	
	def hear(self, s: str) -> bool:
		if s in self.words:
			self.words = [ s ]
			return True
		else:
			self.words.append(s)
			return False

	def tell(self, agent: object) -> None:
		s = random.choice(self.words)
		if agent.hear(s):
			self.words = [ s ]

__all__ = ['Agent']