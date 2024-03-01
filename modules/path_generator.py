from path import OUTPUT_DIR
from os.path import join
from os import makedirs

class PathGenerator:
    def __init__(self, directory) -> None:
        self.output_dir = join(OUTPUT_DIR, directory) if directory!='nan' else OUTPUT_DIR
        makedirs(self.output_dir, exist_ok=True)
        self.file_prefix = directory + ' ' if directory!='nan' else ''
    def filename(self, post_id):
        return f'{self.file_prefix}{post_id}'
    def filepath(self, post_id):
        return join(self.output_dir, self.filename(post_id))