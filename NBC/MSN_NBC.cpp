#include<stdio.h> 
int main() 
{
	int i,j,r;
	const int ROUNDS = 32; /* number of rounds */
	const int BRANCH =16;
	int next = 0; /* next unused state variable index */
	int dummy = 0; /* next unused dummy variable index */
	//int inver_dl[BRANCH]={3,0,1,4,7,2,5,6};
	int inver_dl[BRANCH]={7,2,13,4,11,8,3,6,15,0,9,10,1,14,5,12};
	int a[BRANCH];
	for(i = 0; i < BRANCH; i++)
		a[i]=next++;

		
		
	char filename[]={"minimal_number_of_NBC_Sbox.lp"};
	FILE *f =fopen(filename,"w");			
	fprintf(f,"Minimize\n"); /* print objective function */
	for (i = 0; i < ROUNDS*(BRANCH-1)-2; i=i+2) 
		fprintf(f,"x%i + ",i);
	fprintf(f,"x%i\n\n",ROUNDS*(BRANCH-1)-2);
	
	fprintf(f,"Subject To\n"); /* round function constraints */
	
	for (r = 0; r<ROUNDS; r++) 
	{
		int b[BRANCH];
		//下一轮标号 
		for(j=0;j<BRANCH;j++) b[j]=next++;
		for (i = 0; i < BRANCH; i=i+2)  
		{
			int tmp[BRANCH];
		
		
			for(j=0;j<BRANCH;j++) tmp[j]=b[inver_dl[j]];
			fprintf(f,"x%i + x%i + x%i - 2 d%i >= 0\n",a[i],a[i+1],tmp[i+1],dummy);
			fprintf(f,"d%i - x%i >= 0\n",dummy,a[i]);
			fprintf(f,"d%i - x%i >= 0\n",dummy,a[i+1]);
			fprintf(f,"d%i - x%i >= 0\n",dummy,tmp[i+1]);
			//排除1+1->0的情况 
			//fprintf(f,"x%i - x%i >= 0\n",tmp[i+1],a[i]);
			fprintf(f,"x%i - x%i = 0\n",a[i],tmp[i]);
			
			dummy++;
		}
		for(j=0;j<BRANCH;j++) a[j]=b[j];
	
	}
	
	for (i = 0; i < BRANCH-1; i++) 
		fprintf(f,"x%i + ",i);
	fprintf(f,"x%i >= 1\n\n",BRANCH-1);
	fprintf(f,"Binary\n"); /* binary constraints */
	for (i = 0; i < ROUNDS*BRANCH; i++) 
		fprintf(f,"x%i\n",i);
	for (i = 0; i < dummy; i++) 
		fprintf(f,"d%i\n",i);
	fprintf (f,"End\n");
	
	return 0;
}

