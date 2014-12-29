import subprocess
from subprocess import Popen, PIPE
import os.path

def SSK(n,plambda,str1,str2):
	# Check if the kernel module has been compiled
	if not os.path.isfile("kernel-exact.out"):
		print "calling 'make' to compile SSK kernel module"
		subprocess.call(["make", "kernel-exact.out"]);

	p = Popen(["./kernel-exact.out", str(n), str(plambda)], stdin=PIPE, stdout=PIPE);
	
	input = "\n".join( [ str(len(str1)), str1, str(len(str2)), str2 ] );
	out,err = p.communicate(input);
	return float(out);

def SSKfile(n,file1,file2,plambda = 0.5):
	# Check if the kernel module has been compiled
	if not os.path.isfile("kernel-exact.out"):
		print "calling 'make' to compile SSK kernel module"
		subprocess.call(["make", "kernel-exact.out"]);

	s = subprocess.check_output(["./kernel-exact.out", str(n), file1, file2, str(plambda)]);
	return float(s);



if __name__ == '__main__':
	print SSK(2,0.5,"cat","car");