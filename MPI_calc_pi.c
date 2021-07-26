//mpicc filename
//mpirun -np core_num a.out

#include<stdio.h>
#include<mpi.h>
#include<math.h>


int main(int argc,char* argv[]){
    int total_i;
    int n,rank,length,numprocs,i;
    double pi,width,sum,x,rank_integral;
    char hostname[MPI_MAX_PROCESSOR_NAME];


    MPI_Init(&argc,&argv);
    MPI_Comm_size(MPI_COMM_WORLD,&numprocs);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Get_processor_name(hostname,&length);

    if(rank==0){
        printf("Master node name:  %s\n",hostname);
        scanf("%d",&n);
    }

    MPI_Bcast(&n,1,MPI_INT,0,MPI_COMM_WORLD);

    for(total_i=1;total_i<n;total_i++){
        sum=0.0;
        width=1.0/((double)total_i);
        for(i=rank+1;i<=total_i;i+=numprocs){
            x=width*((double)i-0.5);
            sum+=4.0/(1.0+x*x);
        }

        rank_integral=width*sum;
        MPI_Reduce(&rank_integral,&pi,1,MPI_DOUBLE,MPI_SUM,0,MPI_COMM_WORLD);

    }

    if(rank==0){
        printf("num of processes :%d\n",numprocs);
        printf("cal pi=%.16f\n",pi);
        printf("M_PI=%.16f\n",M_PI);
        printf("Error=%.16f\n",fabs(pi-M_PI));

    }
    MPI_Finalize();
    return 0;
}