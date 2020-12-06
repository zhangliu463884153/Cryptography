

#include <stdio.h>
#include <memory.h>
#include <time.h>
#include <math.h>

typedef unsigned int word32;


void DiffSpectrum(word32* s, word32 N,char *outputfile)
{

    word32 ds[N+1] ;
    word32 dt[N];
    word32 ecx = 0;

    memset(ds, 0, sizeof(word32)*(N+1));
    time_t start, end;
    double usted;

    start = clock();

    word32 x, d;
    for (d = 1; d < N; d ++) 
	{
        //printf("d=%d\n",d);
		memset(dt, 0, sizeof(word32)*N);
        for (x = 0; x < N; x ++) {
            dt[s[x]^s[x^d]] ++;
        }
          
        for (x = 0; x < N; x ++) {
            ds[dt[x]] ++;
        }
        
//        FILE *f=fopen("dt.txt","a+");
//		for (x = 0; x < N; x ++)
//		{
//			fprintf(f,"%d\n", dt[x]);
//		} 
    }
    
  
	
    end = clock();
    
    FILE *fp = fopen(outputfile, "a+");
    usted = double(end - start) / CLOCKS_PER_SEC;
    fprintf(fp,"used time = %lf\n", usted);

    for (d = 0; d <= N; d ++) {
        if (ds[d] > 0) {
            fprintf(fp,"%u, %u\n", d, ds[d]);
            ecx ++;
        }
    }
    fprintf(fp,"ecx = %u\n", ecx);
}

//GetN与ReadSbox代码有重复，GetN只是为了获取文件行数，不将文件内容存储。 
int GetN( char* sboxfile) 
{
    int count = 0;
    int temp;//存储临时获取的文件内容 
    FILE* fp = fopen(sboxfile, "r");
    if (fp == NULL) {
        return 0;
    }

    while (fscanf(fp, "%d\n", &temp) != EOF) {
        count ++; 
    }

    fclose(fp);
    
    return count;
}
void ReadSbox(char* sboxfile, word32* sbox)
{
    int count = 0;
    FILE* fp = fopen(sboxfile, "r");
    if (fp == NULL) {
        printf("文件内容为空\n"); 
    }

    while (fscanf(fp, "%d\n", &sbox[count]) != EOF) {
        count ++;
    }
    fclose(fp);

}

int main(int argc, const char * argv[]) {
  

    printf("请输入Sbox文件名:\n");
	char inputfile[100];
	gets(inputfile);

	
	printf("请输入差分分布表结果输出文件名:\n");
	char outputfile[100];
	gets(outputfile);

	
    word32 num = GetN(inputfile);
    word32 N=ceil(log10(num)/log10(2));
    printf("S盒大小N= %d\n", N);
    printf("num=%d\n",num);
    word32 s[num];
	ReadSbox(inputfile, s);
    
    DiffSpectrum(s,num,outputfile);
    return 0;
    
} 
