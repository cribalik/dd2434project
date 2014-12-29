/* 
 * Calculate the SSK Kernel between 2 strings s and t;
 * 
 *
 * 	Usage 1: programname n filename1 filename2 [lambda]
 *
 * 		n: kernel parameter, number of letters to consider
 *
 * 		filename1,filename2: paths to files that contain s and t
 *
 * 		lambda: exponental falloff parameter
 *
 *
 *	Usage 2: programname n [lambda]
 *
 * 		n: kernel parameter, number of letters to consider
 *
 * 		lambda: exponental falloff parameter
 *		
 *  	send strings into standard input the following way:
 *
 *			size_of_string_1\n
 *			string_1\n
 *			size_of_string_2\n
 *			string_2\n
 *			
 *
 *
 * 	FIXME: Seems to work for all n except n=1
 */

#include <algorithm>
#include <map>
#include <cstdio>
#include <cstdlib>
#include <tuple>
#include <cassert>

using std::min;
using std::make_tuple;

char *s, *t; // documents/strings s and t
double lambda = 0.5; // parameter lambda; amount of exponental falloff due to string length
int n;

// memoization. TODO: replace with vectors when max values of i, sl, and tl are known
std::map< std::tuple<int,int,int> , double > KPmem;
std::map< std::tuple<int,int,int> , double > KPPmem;

// generic power function using repeated squaring
template<typename T>
T pow (T b, T e) {
	T r = 1;
	while (e){
		if (e&1)
			r *= b;
		e >>= 1;
		b *= b;
	}
	return r;
}

// forward declaration of k''
double kpp (int i, int sl, int tl);

double kp (int i, int sl, int tl) {
	
	// check for boundary values
	if (i == 0)
		return 1;

	if (min(sl,tl) < i)
		return 0;
	
	// check the memoization
	auto key = make_tuple(i,sl,tl);
	auto it = KPmem.find(key);
	if ( it != KPmem.end() ) 
		return it->second;

	// if it has not been saved, calculate it, save it and return it
	double val = lambda*kp(i, sl-1, tl) + kpp(i, sl, tl);
	KPmem[key] = val;
	return val;
}

double kpp (int i, int sl, int tl) {
	
	// check boundary values
	if (min(sl,tl) < i)
		return 0;

	// check memoization
	auto key = make_tuple(i,sl,tl);
	auto it = KPPmem.find(key);
	if ( it != KPPmem.end() )
		return it->second;

	// kpp (sx, tu) = lambda^|u| * kpp (sx,t) if x does not occur in u.
	double c = 1;
	int ul = 0;
	while (s[sl-1] != t[tl-1] && tl != 0) {
		--tl;
		++ul;
	}
	if (tl == 0) return 0;
	c *= pow(lambda, ul);

	// calculate, save and return
	double val = c * lambda * ( kpp(i,sl,tl-1) + lambda*kp(i-1,sl-1,tl-1) );
	KPPmem[key] = val;
	return val;
}

double k (int i, int sl, int tl) {

	// check boundary values
	if (min(sl,tl) < i)
		return 0;

	// See definition 2 in article
	double kpsum = 0;
	char x = s[sl-1];
	for (int j = 0; j < tl; ++j) {
		if (t[j] != x) continue;
		kpsum += kp(i-1, sl-1, j);
	}
	double val = k(i, sl-1, tl) + kpsum*lambda*lambda;
	return val;
}

void readFromFile(int argc, char const *argv[],int& sl, int& tl) {
	
	// parameter n of the Kernel
	n = atoi(argv[1]);
	assert(n >= 1);

	// Open files
	FILE* sf = fopen(argv[2],"r");
	FILE* tf = fopen(argv[3],"r");

	// get length of files
	fseek(sf, 0L, SEEK_END);
	fseek(tf, 0L, SEEK_END);
	sl = ftell(sf);
	tl = ftell(tf);
	fseek(sf, 0L, SEEK_SET);
	fseek(tf, 0L, SEEK_SET);

	// allocate memory
	s = new char[sl + 1];
	t = new char[tl + 1];

	// read files into RAM
	int num_read = fread((void*) s, sizeof(char), sl, sf);
	assert(num_read == sl);
	num_read = fread((void*) t, sizeof(char), tl, tf);
	assert(num_read == tl);

	// add null termination to strings
	s[sl] = '\0';
	t[tl] = '\0';

	// get optional lambda
	if (argc > 4)
		lambda = atof(argv[4]);
	assert(lambda > 0 && lambda < 1);
}

void readFromStdin(int argc, char const* argv[], int& sl, int& tl) {
	// parameter n of the Kernel
	n = atoi(argv[1]);
	assert(n >= 1);

	// get optional lambda
	if (argc == 2)
		lambda = atof(argv[2]);
	assert(lambda > 0 && lambda < 1);

	// get s and t from input
	scanf("%i",&sl); // read string length
	getchar(); // throw endline
	s = new char[sl + 1]; // allocate
	fgets(s, sl + 1 , stdin); // read string

	scanf("%i",&tl); // read string length
	getchar(); // throw endline
	t = new char[tl + 1]; // allocate
	fgets(t, tl + 1, stdin); // read string

	printf("%s\n%s\n", s,t);

}

int main(int argc, char const *argv[])
{

	if (argc == 1) {
		printf("Usage:%s n filename1 filename2 [lambda]\nn: kernel parameter, number of letters to consider\nfilename1,filename2: paths to files to calculate the kernel for\nlambda: exponental falloff parameter, default value is %lf\n\nOr:\nn lambda\nsend strings through standard input as:\nsize_of_string_1\nstring_1\nsize_of_string_2\nstring_2\n",argv[0], lambda);
		exit(1);
	}

	int sl,tl;
	if (argc > 3)
		readFromFile(argc,argv,sl,tl);
	if (argc <= 3)
		readFromStdin(argc,argv,sl,tl);

	// Calculate K(s,t)
	double K = k(n, sl, tl);

	// calculate K(t,t)
	char* s_true = s;
	s = t;
	KPmem.clear(); KPPmem.clear();
	double Kt = k(n,tl,tl);

	// Calculate K(s,s)
	t = s_true;
	s = s_true;
	KPmem.clear(); KPPmem.clear();
	double Ks = k(n,sl,sl);

	// Normalize K with Ks and Kt
	K = K / sqrt( Ks*Kt );
	
	printf("%lf\n", K);

	return 0;
}
