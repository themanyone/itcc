//usr/local/bin/tcc $0 -run -- foo bar baz; exit $?
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "math.h"

int main(int argc, char **argv, char **env){
    float a = pow( 5.0, 5.0 );
    printf("pow 5^5 = %.1f\n", a);
    puts(argv[1]);
    return 0;
}
