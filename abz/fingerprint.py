has_acoustid = False
try:
    import acoustid
    has_acoustid = True
except ImportError:
    pass

def get_recordingid_for_file(filepath):
    pass
