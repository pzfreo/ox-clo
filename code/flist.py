class FList(list):
    def __init__(self, *args):
        list.__init__(self, *args)
        
    def map(self, f):
    	return FList(map(f, self))
    
    def filter(self, f):
    	return FList(filter(f, self))
    	
    def reduce(self, f):
    	return FList(reduce(f, self))
    	
    def flatten(self):
        return FList(reduce(lambda x,y: x+y,self))
    	
    def flatMap(self, f):
    	return FList(reduce(lambda x,y: x+y,(map(f, self))))
    	

