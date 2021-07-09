from tqdm import tqdm

class ProgressBar:
    def __init__(self,length):
        self.progress = tqdm(range(length))