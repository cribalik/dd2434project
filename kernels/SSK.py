import subprocess
from subprocess import Popen, PIPE
import os.path

__m_dir = os.path.dirname(os.path.abspath(__file__));


def SSK(n, plambda, str1, str2):
    # Check if the kernel module has been compiled
    # if not os.path.isfile(os.path.join(__m_dir, "kernel-exact.out")):
        # print "calling 'make' to compile SSK kernel module"

    subprocess.call(["make", "--directory=" + __m_dir, "kernel-exact.out"]);
    p = Popen([os.path.join(__m_dir, "kernel-exact.out"), str(n), str(plambda)], stdin=PIPE, stdout=PIPE);

    input = "\n".join([str(len(str1)), str1, str(len(str2)), str2]);
    out, err = p.communicate(input);
    return float(out);


def SSKfile(n, file1, file2, plambda=0.5):
    # Check if the kernel module has been compiled
    # if not os.path.isfile(os.path.join(__m_dir, "kernel-exact.out")):
        # print "calling 'make' to compile SSK kernel module"
    subprocess.call(["make", "--directory=" + __m_dir, "kernel-exact.out"]);

    s = subprocess.check_output([os.path.join(__m_dir, "kernel-exact.out"), str(n), file1, file2, str(plambda)]);
    return float(s);


if __name__ == '__main__':
    print SSK(2, 0.5, "cat", "car");