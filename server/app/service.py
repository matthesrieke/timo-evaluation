import papermill as pm
from papermill.exceptions import PapermillExecutionError
import uuid

import pathlib
import datetime

def create_evaluation(start, end, sessionId):
    out_file = "/tmp/%s_%s.xlsx" % (start, end)
    
    try:
        pm.execute_notebook(
            '/home/jovyan/allprojects.ipynb',
            '/tmp/output_%s.ipynb' % uuid.uuid4(),
            parameters = dict(start_date=start, end_date=end, JSESSIONID=sessionId, output=out_file)
        )
    except PapermillExecutionError as e:
        raise ValueError(e)

    return out_file


def create_performance_record(start, end, sessionId):
    out_file = "/tmp/%s_%s.xlsx" % (start, end)
    
    try:
        pm.execute_notebook(
            '/home/jovyan/performance_record.ipynb',
            '/tmp/output_%s.ipynb' % uuid.uuid4(),
            parameters = dict(start_date=start, end_date=end, JSESSIONID=sessionId, output=out_file)
        )
    except PapermillExecutionError as e:
        raise ValueError(e)

    return out_file
        
def check_file_up_to_date(graph_file):
    fname = pathlib.Path(graph_file)
    if fname.exists():
        mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
        now = datetime.datetime.now()
        return (now - mtime).seconds < (20 * 60)
    else:
        return False