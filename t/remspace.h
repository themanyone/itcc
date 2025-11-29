#ifndef __REMSPACE_H
#define __REMSPACE_H

extern "C"
void remove_spaces(char*s)
{char*d=s;do{while(*d==' ')++d;}while(*s++=*d++);}

#endif
