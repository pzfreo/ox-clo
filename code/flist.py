class FList(list):
    def __init__(self, *args):
        list.__init__(self, *args)
        
    def map(self, f):
    	return FList(map(f, self))
    
    def filter(self, f):
    	return FList(filter(f, self))
    	
    def reduce(self, f):
    	res = reduce(f, self)
    	return FList(res) if hasattr(res, '__iter__') else res
    	
    def flatten(self):
    	res = reduce(lambda x,y: x+y,self)
    	return FList(res) if hasattr(res, '__iter__') else res
    	
    def flatMap(self, f):
    	res =reduce(lambda x,y: x+y,(map(f, self)))
    	return FList(res) if hasattr(res, '__iter__') else res
    	

