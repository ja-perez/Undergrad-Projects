// Program Name: japerez_ShellScript.c
// Author: Javier Perez
// Purpose: To simulate a linux terminal by implementing various system commands that
// are read from the terminal then executed.
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/stat.h>
#include <stdbool.h>

#define MAX_HOST_NAME 253
#define ENVIROMENT "HOME"
#define PATH_MAX 4096  // Directory Path Name Max
#define CLI_MAX 4095 // Command Line Input Max

// Function Prototypes
bool fileRedirect(char* tokens[], char* outputTokens[], bool isRedirect);
void promptUser (bool isBatch);
void printError();
int parseInput(char *input, char *splitWords[]);
char *redirectCommand(char *special, char *line, 
      bool *isRedirect, char *tokens[], char *outputTokens[]);
char *executeCommand(char *cmd, bool *isRedirect,
      char* tokens[], char* outputTokens[], bool *isExits);
bool exitProgram(char *tokens[], int numTokens);
void launchProcesses(char *tokens[], int numTokens, bool isRedirect);
void changeDirectories(char *tokens[], int numTokens);
void printHelp(char *tokens[], int numTokens);

int main(int argc, char *argv[]) {
    bool isBatch;
    char CLI[CLI_MAX];
    char *splitWords[CLI_MAX];
    int numTokens;
    
    // execute_command variables
    bool isRedirect = 0;
    bool isExits = 0;
    char* outputTokens[CLI_MAX];

    if (argc == 2) {
    // Batch Mode
      isBatch = true;
      promptUser(isBatch);
      FILE* batchf = fopen(argv[1], "r");
    // Edge Case - check if batch file exits
      if (batchf == NULL) {
        printError();
        return 1;
      } else {  
      while(fgets(CLI, CLI_MAX, batchf) != NULL) {
          isRedirect = 0;
          isExits = 0;
          printf("%s", executeCommand(CLI, &isRedirect, splitWords, outputTokens, &isExits));
          if (fileRedirect(splitWords, outputTokens, isRedirect) == 1) {
              return 1;
          }         
        }
      fclose(batchf);
      }      
    } else if (argc == 1) {
	// Normal Mode      
      while(true) {
        isRedirect = 0;
        isExits = 0;
        isBatch = false;
        promptUser(isBatch);  
        fgets(CLI, CLI_MAX, stdin);
        char *fileName = executeCommand(CLI, &isRedirect, splitWords, outputTokens, &isExits);
        if (fileRedirect(splitWords, outputTokens, isRedirect) == 1) {
       		return 1;
       	}
        if (isExits == 1) {
        	kill(0, SIGTERM);
        }
    } 
  } else {
    printError();
    return 1;
  } 
}

bool fileRedirect(char* tokens[], char* outputTokens[], bool isRedirect) {

        if (isRedirect == 1) {
          char FileInput[CLI_MAX + 1];
          // output name has |n at end
          char temp[CLI_MAX];
          strncpy(temp, outputTokens[0], strlen(outputTokens[0]) - 1);
          outputTokens[0] = temp;
          FILE *fin = fopen(tokens[0], "r");
          FILE *fout = fopen(outputTokens[0], "w");
          if (fin == NULL) {
            printError();
            return 1;
          } else {
          while(fgets(FileInput, CLI_MAX + 1, fin) != NULL) {
              fputs(FileInput, fout);
            }
          fclose(fout);
          fclose(fin);
          }
        }
        return 0;
}

void promptUser (bool isBatch){
  if (isBatch == false) {
    char* user = getenv(ENVIROMENT);
    user = strrchr(user, '/') + 1;
    char host[MAX_HOST_NAME + 1];
    gethostname(host, MAX_HOST_NAME + 1);
    char cwd[PATH_MAX + 1];
    getcwd(cwd, PATH_MAX + 1);  
    printf("%s@%s:%s$ ", user, host, cwd);
  }
}

void printError(){
    printf("Shell Program Error Encountered\n");
}

int parseInput(char *input, char *splitWords[]){
      int wordInd = 0;
      splitWords[0] = strtok(input, " ");
      while(splitWords[wordInd] != NULL){
      	splitWords[++wordInd] = strtok(NULL, " ");
		}

      return wordInd;
}

char *redirectCommand(char *special, char *line, 
    bool *isRedirect, char *tokens[], char *outputTokens[]){
    int numTokens = parseInput(line, tokens);
	int numOutput = parseInput(special, outputTokens);
	char* inputF = strtok(line, ">");
	
	if (inputF == NULL || numTokens > 3) {
		*isRedirect = 0;
		printError();
		return outputTokens[0];
	}
	
	if (numOutput == 1) {
		outputTokens[1] = outputTokens[0] + 1;
		outputTokens[0] = ">";
	} else if (numOutput == 2 && strlen(outputTokens[0]) > 1) {
		*isRedirect = 0;
		printError();
		return outputTokens[0];
	}
	int specialLen = strlen(outputTokens[0]);
	char *outputString[CLI_MAX];
	int outputLen = parseInput(outputTokens[1], outputString);
	if (specialLen > 1 || strchr(outputTokens[1], '>') != NULL || outputLen > 1 || numOutput > 2) {
		*isRedirect = 0;
		printError();
		return outputTokens[0];
	}
	outputTokens[0] = outputString[0];
	tokens[0] = inputF;
	tokens[1] = ">";
	tokens[2] = outputString[0];
	*isRedirect = 1;

    return outputTokens[0]; 

}

char *executeCommand(char *cmd, bool *isRedirect,
    char* tokens[], char* outputTokens[], bool *isExits) {  
    int numTokens;
    char* cmdCopy = strdup(cmd);
    char* outFile = "";
    char* redirectSymbol = NULL;
    redirectSymbol = strchr(cmdCopy, '>');

    if (redirectSymbol != NULL) {
      // call redirect command
      outFile = redirectCommand(redirectSymbol, cmd, isRedirect, tokens, outputTokens);
      return (outFile);
    } else {
        numTokens = parseInput(cmd, tokens); 
        if (numTokens == 0) {
            return outFile;
      } 
        *isExits = exitProgram(tokens, numTokens);
        if (*isExits == 1) {
            return outFile;
      }
    }
    changeDirectories(tokens, numTokens);
    printHelp(tokens, numTokens);
    launchProcesses(tokens, numTokens, *isRedirect);
    return outFile;
}

char getLetter(char *str, int index){}
 
bool exitProgram(char *tokens[], int numTokens) {
  if (strcmp(tokens[0], "exit") == 0) {
    if (numTokens > 1) {
        printError();
        return 0;
    } else {
        return 1;
    }
  } else if (strcmp(tokens[0], "exit\n") == 0) {
      return 1;
  } else {
      return 0;
  }
}  

void launchProcesses(char *tokens[], int numTokens, bool isRedirect){
    int process_state;
    char cmd[CLI_MAX] = {0};
	
    if (numTokens == 1) {
    	strncpy(cmd, tokens[0], strlen(tokens[0]) - 1);
    } else if (isRedirect != 1) {
    	strncpy(cmd, tokens[0], strlen(tokens[0]));
    	char temp[CLI_MAX] = {0};
    	strncpy(temp, tokens[numTokens - 1], strlen(tokens[numTokens - 1]) - 1);
    	tokens[numTokens - 1] = temp;
    }
	if (strcmp(tokens[0],"exit\n") != 0 && strcmp(tokens[0],"cd\n") != 0 && strcmp(tokens[0], "help\n") != 0
	&& strcmp(tokens[0],"exit") != 0 && strcmp(tokens[0],"cd") != 0 && strcmp(tokens[0],"help") != 0) {
		if (fork() == 0) {
			process_state = execvp(cmd, tokens);
			if (process_state == -1) {
				wait(NULL);
				printError();
			}			
		} else {
			wait(NULL);
		}
	}
}



void changeDirectories(char *tokens[], int numTokens){
  if (strcmp(tokens[0],"cd") == 0) {
    if (numTokens > 2 || numTokens == 1) {
      printError();
    } else {
      // removing \n for system to read path name
      char path_name[PATH_MAX];
      strncpy(path_name, tokens[1], strlen(tokens[1]) - 1);
      if (chdir(path_name) == -1) {
      	printError();
      }
    }
  } else if (strcmp(tokens[0], "cd\n") == 0) {
      printError(); // cd having \n means it was the only command
  }
}

void printHelp(char *tokens[], int numTokens) {
  if (strcmp(tokens[0],"help") == 0 || strcmp(tokens[0], "help\n") == 0) {
      if (numTokens > 1) {
        printError();
      } else {
        printf("\nJavier's example linux shell.\nThese shell commands are defined interally.\n");
        printf("help -prints this screen so you can see available shell commands.\n");
        printf("cd -changes directories to specified path; if not given, defaults to home.\n");
        printf("exit -closes the example shell.\n[input] > [output] -pipes input file into output file\n");
        printf("\nAnd more! If it's not explicitly defined here (or in the documentation for the assignment),");
        printf(" then the command should try to be executed by launchProcesses.\n");
        printf("That's how we get ls -la to work here!\n\n");
      }
  }
}
