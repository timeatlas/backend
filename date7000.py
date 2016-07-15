class Date7000:
	def __init__(self, year, month, date, normal=False):
		object.__setattr__(self, 'month', month)
		object.__setattr__(self, 'date', date)
		if normal:
			object.__setattr__(self, 'normalYear', year)
			if year < 0:
				object.__setattr__(self, 'year', 7001 + year)
			else:
				object.__setattr__(self, 'year', 7000 + year)
		else:
			if year < 7001:
				object.__setattr__(self, 'normalYear', year - 7001)
			else:
				object.__setattr__(self, 'normalYear', year - 7000)
			object.__setattr__(self, 'year', year)

	def __setattr__(self, *ignored):
		raise NotImplementedError('Date7000 is immutable object')

	def __lt__(self, other):
		return self.year < other.year or\
		      (self.year == other.year and self.month < other.month) or\
		      (self.year == other.year and self.month == other.month and self.date < other.date)

	def __gt__(self, other):
		return not self.year < other.year or\
		          (self.year == other.year and self.month < other.month) or\
		          (self.year == other.year and self.month == other.month and self.date < other.date)

	def __eq__(self, other):
		return not (self < other or self > other)

	def __ne__(self, other):
		return not (self == other)

	def __le__(self, other):
		return self < other or self == other

	def __ge__(self, other):
		return self > other or self == other


