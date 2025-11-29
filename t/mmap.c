#!/usr/local/bin/tcc -run
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>

int copy_file(const char *in, const char *out)
{
	int ret = 0;
	int fin, fout;
	char *bi;
	struct stat st;

	if ((fin  = open(in,  O_RDONLY)) == -1) return 0;
	if (fstat(fin, &st)) goto bail;

	fout = open(out, O_WRONLY|O_CREAT|O_TRUNC, st.st_mode & 0777);
	if (fout == -1) goto bail;

	bi = mmap(0, st.st_size, PROT_READ, MAP_PRIVATE, fin,  0);

	ret = (bi == (void*)-1)
		? 0 : (write(fout, bi, st.st_size) == st.st_size);

bail:	if (fin != -1)  close(fin);
	if (fout != -1) close(fout);
	if (bi != (void*)-1) munmap(bi, st.st_size);
	return ret;
}

int main(int argc, char **argv, char **env){
    if (argc < 3){
        puts("Usage: fcopy [infile] [outfile]\n");
    }
    return copy_file(argv[1], argv[2]);
}
