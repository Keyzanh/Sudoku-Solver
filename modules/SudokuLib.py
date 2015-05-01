from modules.PileLib import Pile

class Sudoku:

	def __init__( self, grid ):
		"""
			Constructor
		"""
		self.grid = [ [ i for i in range( 1, 10 ) ] for j in range( 81 ) ] # The grid to resolve with each possibility for each case
		self.caseRelations = [[]] * 81
		self.pile = Pile()
		
		self._constructCaseRelations()		
		self._gridImport( grid )
	
	
	
	
	def _constructCaseRelations( self ):
		"""
			Calcule the related cases (line, column and square) for each case of the grid
		"""
		for i in range( 81 ):
			linePositions = self._getAllLinePositions( i )
			columnPositions = self._getAllColumnPositions( i )
			squarePositions = self._getAllSquarePositions( i )
			allPositions = self._concatListsWithoutDuplicates( [ linePositions, columnPositions, squarePositions ] )
			self.caseRelations[ i ] = list( allPositions )
				
	
	def _gridImport( self, grid ):
		"""
			Convert the given grid to the good format and apply all start constraints
		"""
		for i in range( self.grid.__len__() ):
			number = grid[ i // 9 ][ i % 9 ]
			if number != 0:
				self._applyConstraint( i, self._deleteListElements( [ number ], [ elt for elt in range( 1, 10 ) ] ) )
				
				
				
				
	def _deleteListElements( self, listToDelete, fromList ):
		"""
			Delete all elements of listToDelete from the list fromList and return the new list
		"""	
		for i in listToDelete:
			if i in fromList:
				fromList.remove( i )
				
		return fromList
		
		
		
		
	def _concatListsWithoutDuplicates( self, lists ):
		"""
			Return the concatenation of all the lists in lists without duplicates
		"""
		newList = []
		
		for i in lists:
			for j in i:
				if not j in newList:
					newList.append( j )
					
		return newList
				
			
	
	
	def _getNextPosition( self ):
		"""
			Return the case position which have the less number of possibilities (but more than one).
			Return -1 if no case matches
		"""
		position = -1
		minNbSolutions = 10
	
		for i in range( 0, self.grid.__len__() ):
			nbSolutions = self.grid[ i ].__len__()
			if nbSolutions > 1 and nbSolutions < minNbSolutions:
				minNbSolutions = nbSolutions
				position = i
				
		return position
		
		
		
		
	def _getAllLinePositions( self, position ):
		"""
			Return the list of positions of all the cases in the same line of the case identified by position
		"""
		positions = []
	
		for i in range( ( position // 9 ) * 9, ( position // 9 + 1 ) * 9 ):
			if i != position:
				positions.append( i )
			
		return positions
		
		
		
		
	def _getAllColumnPositions( self, position ):
		"""
			Return the list of positions of all the cases in the same column of the case identified by position
		"""
		positions = []
	
		for i in range( position % 9, position % 9 + 73, 9 ):
			if i != position:
				positions.append( i )
			
		return positions
		
		
		
		
	def _getAllSquarePositions( self, position ):
		"""
			Return the list of positions of all the cases in the same square of the case identified by position
		"""
		positions = []
	
		for j in range( position - ( ( position // 9 ) % 3 ) * 9 - position % 3, position - ( ( position // 9 ) % 3 ) * 9 - position % 3 + 19, 9 ):
			for i in range( j, j + 3 ):
				if i != position:
					positions.append( i )
			
		return positions
		
		
		
		
	def _addPossibilities( self, position, possibilities ):
		"""
			Add possibilities in the case at position
		"""
		self.grid[ position ].extend( possibilities )
		
		return True
		
		
		
		
	def _removePossibilities( self, position, possibilities ):
		"""
			Remove possibilities in the case at position
		"""
		for i in possibilities:
			if i in self._getPossibilities( position ):
				self.grid[ position ].remove( i )
			if self._countPossibilities( position ) <= 0:
				return False
				
		return True
				
	
	
	
	def _getPossibilities( self, position ):
		"""
			Return the list possibilities for a position
		"""
		return self.grid[ position ]
		
		
		
	
	def _countPossibilities( self, position ):
		"""
			Return the number of possibilities for the position
		"""
		return self.grid[ position ].__len__()
	
	
	
	
	def _removeLastContraint( self ):
		"""
			Undo the last operation notified in the pile
		"""
		[ position, removeList ] = self.pile.unstack()
		self._addPossibilities( position, removeList )
		
		return True
		
	
	
	
	def _removeConstraints( self, pileCount ):
		"""
			Remove all constraints till the pile counter reach pileCount
			(the pileCount's entry won't be removed)
		"""
		
		while pileCount < self.pile.count():
			self._removeLastContraint()
			
		return True
		
	
				
				
	def _applyConstraint( self, position, removeList ):
		"""
			Apply a constraint to the grid by removing a list of possibilites (removeList) to a
			case (position)
		"""
		self.pile.stack( [ position, removeList ] )
		
		# Non valid solution
		if not self._removePossibilities( position, removeList ):
			return False
		
		# Case with only one possibility
		if self._countPossibilities( position ) == 1:
			number = self.grid[ position ][ 0 ]
			for i in self.caseRelations[ position ]:
				if number in self._getPossibilities( i ):
					if not self._applyConstraint( i, [ number ] ):
						return False
					
		return True
		
		
		
		
	def Resolve( self ):
		"""
			Resolve the grid
		"""
		position = self._getNextPosition()
		
		# Resolution successful
		if position == -1:
			return True

		pileCurrentCount = self.pile.count()
		possibilities = self._getPossibilities( position )
		
		for i in possibilities:
			if self._applyConstraint( position, self._deleteListElements( [ i ], list( possibilities ) ) ) and self.Resolve():
				return True
			else:
				# Something went wrong, undo everything that has been done since the start of this function
				self._removeConstraints( pileCurrentCount )
			
		return False
		
		
		
	
	def Display( self ):
		"""
			Display the grid in a good (formated) presentation
		"""
		for i in range( self.grid.__len__() ):
			if i % 9 == 0:
				print()
			if self.grid[ i ].__len__() == 1:
				print( self.grid[ i ][ 0 ], end=' ' )
			elif self.grid[ i ].__len__() <= 0:
				print( 'X', end=' ' )
			else:
				print( '0', end=' ' )
		print()
		print()
