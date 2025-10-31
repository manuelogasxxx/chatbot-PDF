#include <iostream>
using namespace std;
void suma(char num1[], char num2[])
{
    //lógica para hacer las sumas
    int a1=0;
    int b1=0;
    int carry=0;
    int res=0;
    int factor=1;
    for(int i=1;i<6;i++){
        a1=num1[5-i]-'0';
        b1=num1[5-i]-'0';
        res+= (a1+b1)*(factor)+carry;
        if(a1+b1 > 10)carry=1;
        else carry=0;

        factor*=10;
    }
    cout<<res;
}

void resta(char num1[], char num2[],bool flag)
{
    //lógica para hacer las sumas
    int a1=0;
    int b1=0;
    int carry=0;
    int res=0;
    int factor=1;
    int prestamo=0;
    for(int i=1;i<6;i++){
        //conversión a decimal
        a1=num1[5-i]-'0';
        b1=num2[5-i]-'0';
        //caso en que es 0
        if(a1<b1){
            a1+=10;
            res+= (a1-b1-prestamo)*(factor);
            prestamo=1;
        }
        else{
            res+= (a1-b1-prestamo)*(factor);
            prestamo=0;        
        }
        factor*=10;
    }
    cout<<res<<"\n";
    cout<<flag;
}


void resta2(char num1[],char num2[])
{
    bool flag=false;
    for (int i = 5; i>=0; i--)
    {
        if(num1[i]<num2[i]){
            flag=true;
            break;
        }
    }
    if(flag)//el primero es menor
    {
        resta(num2,num1,flag);
    }
    else resta (num1,num2,flag);
    
}
//toma en cuenta que el numero ingresado está a reves
void multiplicacion(char num1[],char num2[]){
    int resultado[10]={0};
    for (int i = 5-1; i>=0; i--)
    {
        /* code */
    }
    
}

int main(void){
    
    char a[5]={'1','0','0','0','5'};
    char b[5]={'1','2','3','4','0'};

    resta2(a,b);
}


//funciones para sumar con arreglos

