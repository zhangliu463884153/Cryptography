

#include <stdio.h>
#include <memory.h>
#include <time.h>
#include <math.h>


typedef unsigned int word32;

int compute_wt(int sbox_size, int quotient)
{
	int result[sbox_size];
    int remainder = 0;
    int i = 0,wt=0;
	while (quotient != 0) 
	{
		 remainder = quotient % 2; //求余数
		 result [i] = remainder;//数组存放每次所得的余数
		 i++;
		 quotient = quotient / 2;//求商
	}	
 	
 	for(int i=0;i<sbox_size;i++)
 	{
 		if (result[i]==1)
 			wt++;
	}
	
	return wt;
} 

int differential_branch_number(word32* s,int N,int sbox_size)
{
	int minize=N;//初始化最小值 
	
	for(int i=0;i<N;i++)
	{
		printf("num=%d\n",i);
		for(int j=0;j<N;j++)
		{
			if(i!=j)
			{
				int temp=compute_wt(sbox_size,i^j)+compute_wt(sbox_size,s[i]^s[j]);
				//printf("temp=%d\n",temp);
				if(temp<minize)
					minize=temp;
			}
			
		}
	}
		
	printf("differential_branch_number=%d\n",minize);
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
	
    word32 num = GetN(inputfile);
    word32 sbox_size=ceil(log10(num)/log10(2));
    printf("sbox_size=%d\n", sbox_size);
    word32 s[num];
	ReadSbox(inputfile, s);
    
    differential_branch_number(s,num,sbox_size);
    return 0;
    
} 
