class Date7000:
	def __init__(self, year, month, date, normal=False):
		object.__setattr__(self, 'month', month)
		object.__setattr__(self, 'date', date)
		if normal:
			if year < 0:
				object.__setattr__(self, 'year', 7001 + year)
			else:
				object.__setattr__(self, 'year', 7000 + year)
		else:
			object.__setattr__(self, 'year', year)

	def normalYear(self):
		if self.year < 7001:
			return self.year - 7001
		else:
			return self.year - 7000

	def __setattr__(self, *ignored):
		raise NotImplementedError('Date7000 is immutable object')
