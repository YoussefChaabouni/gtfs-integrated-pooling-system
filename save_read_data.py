# FUNCTIONS TO READ AND SAVE DATA IN PICKLE FORMAT
import pickle
def save_data(object,filename):
    with open('data/pickle/'+filename, 'wb') as outp:
        pickle.dump(object, outp, pickle.HIGHEST_PROTOCOL)

def read_data(filename):
    with open('data/pickle/'+filename, 'rb') as inp:
        return(pickle.load(inp))