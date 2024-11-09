import random 
from . import Agent

class NamingGame:
	def __init__(self, n: int):
		self.agents = [ Agent(n) for i in range(n) ]
		self.iteration = 0

	def __str__(self) -> str:
		agents_string = '\n  '.join(str(agent) for agent in self.agents)
		return f'<#NamingGame {self.iteration} {self.poll()}\n  {agents_string}\n>'

	def run(self) -> None:
		for agent in self.agents:
			agent.tell(random.choice(self.agents))
		self.iteration+=1
	
	def poll(self) -> bool:
		all_words = set()
		for agent in self.agents:
			for word in agent.words:
				all_words.add(word)
		return (len(all_words) == 1)
	
	def execute(self):
		while (not self.poll()):
			print(self)
			self.run()
		print(self)

__all__ = ["NamingGame"]