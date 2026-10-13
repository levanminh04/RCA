import os,pathlib,runpy
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[key]='1'
runpy.run_path(str(pathlib.Path(__file__).with_name('backend_status.py')),run_name='__main__')
