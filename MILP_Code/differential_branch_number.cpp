

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
		 remainder = quotient % 2; //������
		 result [i] = remainder;//������ÿ�����õ�����
		 i++;
		 quotient = quotient / 2;//����
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
	int minize=N;//��ʼ����Сֵ 
	
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


//GetN��ReadSbox�������ظ���GetNֻ��Ϊ�˻�ȡ�ļ������������ļ����ݴ洢�� 
int GetN( char* sboxfile) 
{
    int count = 0;
    int temp;//�洢��ʱ��ȡ���ļ����� 
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
        printf("�ļ�����Ϊ��\n"); 
    }

    while (fscanf(fp, "%d\n", &sbox[count]) != EOF) {
        count ++;
    }
    fclose(fp);

}

int main(int argc, const char * argv[]) {
  

    printf("������Sbox�ļ���:\n");
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
