import subprocess

def SSK(n,file1,file2,plambda = 0.5):
	s = subprocess.check_output(["./kernel-exact.out", str(n), file1, file2, str(plambda)]);
	return float(s);
