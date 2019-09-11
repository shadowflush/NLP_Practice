#include <stdio.h>
#include <stdlib.h>

int main(int argc,char* argv[]){
	if(argc == 3){//make sure arg right
		if(strcmp(argv[2],"GB2312") ==0){
			GB_2312(argv[1],"outcome_GB2312");
		}
		else if(strcmp(argv[2],"UTF8") == 0){
			UTF_8(argv[1],"outcome_UTF8");
		}
		else{
			printf("Do not support %s ",argv[2]);		
		}
	}
	else{
		printf(" arg error\n");
	}
	return 0;
}

void GB_2312(char* filePath,char* outcomeFilePath){
	FILE* input =fopen(filePath,"rb");
	FILE* output =fopen(outcomeFilePath,"wb");
	unsigned char buffer[2],save='\0',space =' ';
	int size =0,totalChar =0;
	while((size =fread(buffer,1,2,input))){
		if( size == 2){
			if(buffer[0] <128 && buffer[1] >=128){
				save =buffer[1];
				fwrite(buffer,1,1,output);
				fwrite(&space,1,1,output);
				totalChar+=1;
			}
			else if(buffer[0] <128 && buffer[1] <128){
				fwrite(buffer,1,1,output);
				fwrite(&space,1,1,output);
				fwrite(buffer+1,1,1,output);
				fwrite(&space,1,1,output);
				totalChar+=2;
			}
			else if(buffer[0] >=128 && buffer[1] <128){
				fwrite(&save,1,1,output);
				fwrite(buffer,1,1,output);
				fwrite(&space,1,1,output);
				fwrite(buffer+1,1,1,output);
				fwrite(&space,1,1,output);
				totalChar+=2;
				save ='\0';
			}
			else{
				if(save >=128){
					fwrite(&save,1,1,output);
					fwrite(buffer,1,1,output);
					fwrite(&space,1,1,output);
					save =buffer[1];
				}
				else{
					fwrite(buffer,1,2,output);
					fwrite(&space,1,1,output);
				}
				totalChar+=1;
			}
		}//if size ==2
		else{
			if(buffer[0] <128){
				fwrite(buffer,1,1,output);
				fwrite(&space,1,1,output);
				totalChar+=1;			
			}
			else{
				fwrite(&save,1,1,output);
				fwrite(buffer,1,1,output);
				fwrite(&space,1,1,output);
				totalChar+=1;			
			}		
		}
	}//wile
	printf("totalChar: %d\n",totalChar);
	fclose(input);
	fclose(output);
}

void UTF_8(char* filePath,char* outcomeFilePath){
	FILE* input =fopen(filePath,"rb");
	FILE* output =fopen(outcomeFilePath,"wb");
	
	unsigned char buffer,space =32;

	int totalChar =0,size =0;

	while(fread(&buffer,1,1,input)){
		if (buffer <128){
			fwrite(&buffer,1,1,output);
		
			fwrite(&space,1,1,output);
			totalChar+=1;		
		}
		else if(buffer<224 && buffer >192){
			fwrite(&buffer,1,1,output);
	
			fread(&buffer,1,1,input);
			fwrite(&buffer,1,1,output);

			fwrite(&space,1,1,output);
			totalChar+=1;
		}
		else if(buffer >224 && buffer <240){
			fwrite(&buffer,1,1,output);

			fread(&buffer,1,1,input);
			fwrite(&buffer,1,1,output);

			fread(&buffer,1,1,input);
			fwrite(&buffer,1,1,output);

			fwrite(&space,1,1,output);
			totalChar+=1;
		}
		else{
			fwrite(&buffer,1,1,output);

			fread(&buffer,1,1,input);
			fwrite(&buffer,1,1,output);

			fread(&buffer,1,1,input);
			fwrite(&buffer,1,1,output);
	
			fread(&buffer,1,1,input);
			fwrite(&buffer,1,1,output);

			fwrite(&space,1,1,output);
			totalChar+=1;
		}
	}//while
	printf("totalChar: %d\n",totalChar);
	fclose(input);
	fclose(output);
}
