import subprocess
from subprocess import Popen, PIPE
import os.path

__m_dir = os.path.dirname(os.path.abspath(__file__));

# Calculate SSK with parameters n and plambda for the strings str1 and str2
def SSK(n, plambda, str1, str2):
    # Check if the kernel module has been compiled
    if not os.path.isfile(os.path.join(__m_dir, "kernel-exact.out")):
        print "calling 'make' to compile SSK kernel module"
        with open(os.devnull, 'w') as devnull:
            subprocess.call(["make", "--directory=" + __m_dir, "kernel-exact.out"], stdout=devnull, stderr=devnull);
    
    p = Popen([os.path.join(__m_dir, "kernel-exact.out"), str(n), str(plambda)], stdin=PIPE, stdout=PIPE);

    input = "\n".join([str(len(str1)), str1, str(len(str2)), str2]);
    out, err = p.communicate(input);
    return float(out);

# Calculates SSK with parameters n and plambda, where file1 och file2 are the two string for which to calculate the kernel for
def SSKfile(n, file1, file2, plambda=0.5):
    # Check if the kernel module has been compiled
    if not os.path.isfile(os.path.join(__m_dir, "kernel-exact.out")):
        print "calling 'make' to compile SSK kernel module"
        with open(os.devnull, 'w') as devnull:
            subprocess.call(["make", "--directory=" + __m_dir, "kernel-exact.out"], stdout=devnull, stderr=devnull);

    s = subprocess.check_output([os.path.join(__m_dir, "kernel-exact.out"), str(n), file1, file2, str(plambda)]);
    return float(s);


if __name__ == '__main__':
    print SSK(2, 0.5, "cat", "car");