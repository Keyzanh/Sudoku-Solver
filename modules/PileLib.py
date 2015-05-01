class Pile:

	pile = []
	
	def stack( self, data ):
	
		self.pile.append( data )
		return True
		
	
	
	def unstack( self ):
	
		if not self.pile:
			return False
		
		return self.pile.pop()
	
	
	
	def top( self ):
	
		if not self.pile:
			return False
		
		return self.pile[ -1 ]
		
		
		
	def count( self ):
	
		return self.pile.__len__()
