// this example creates a tridiagonal matrix of type
//
//     |  2  -1            |
//     | -1   2   -1       | 
// A = |      ...  ... ... |
//     |            -1  2  |

#include "Epetra_ConfigDefs.h"
#ifdef HAVE_MPI
#include "mpi.h"
#include "Epetra_MpiComm.h"
#else
#include "Epetra_SerialComm.h"
#endif
#include "Epetra_Map.h"
#include "Epetra_Vector.h"
#include "Epetra_CrsMatrix.h"

int main(int argc, char *argv[])
{
#ifdef HAVE_MPI
  MPI_Init(&argc, &argv);
  Epetra_MpiComm Comm(MPI_COMM_WORLD);
#else
  Epetra_SerialComm Comm;
#endif

  // set global dimension of the matrix to 5, could be any number
  int NumGlobalElements = 5;
  
  // create a map
  Epetra_Map Map(NumGlobalElements, 0, Comm);
  
  // local number of rows
  int NumMyElements = Map.NumMyElements();
  
  // get update list
  int * MyGlobalElements = Map.MyGlobalElements( );

  // Create an integer vector NumNz that is used to build the Petra Matrix.
  // NumNz[i] is the Number of OFF-DIAGONAL term for the ith global equation 
  // on this processor

  int* NumNz = new int[NumMyElements];

  // We are building a tridiagonal matrix where each row has (-1 2 -1)
  // So we need 2 off-diagonal terms (except for the first and last equation)

  for (int i = 0; i < NumMyElements; i++)
    if (MyGlobalElements[i]==0 || MyGlobalElements[i] == NumGlobalElements-1)
      NumNz[i] = 2;
    else
      NumNz[i] = 3;

  // Create a Epetra_Matrix
  Epetra_CrsMatrix A(Copy,Map,NumNz);
  // (NOTE: constructor `Epetra_CrsMatrix A(Copy,Map,3);' was ok too.)
  
  // Add  rows one-at-a-time
  // Need some vectors to help
  // Off diagonal Values will always be -1, diagonal term 2

  double* Values = new double[2];
  Values[0] = -1.0; Values[1] = -1.0;
  int* Indices = new int[2];
  double two = 2.0;
  int NumEntries;

  for (int i = 0 ; i < NumMyElements; ++i) 
  {
    if (MyGlobalElements[i] == 0) 
    {
      Indices[0] = 1;
      NumEntries = 1;
    } 
    else if (MyGlobalElements[i] == NumGlobalElements-1) 
    {
      Indices[0] = NumGlobalElements - 2;
      NumEntries = 1;
    } 
    else 
    {
      Indices[0] = MyGlobalElements[i] - 1;
      Indices[1] = MyGlobalElements[i] + 1;
      NumEntries = 2;
    }

    A.InsertGlobalValues(MyGlobalElements[i], NumEntries, Values, Indices);
    // Put in the diagonal entry
    A.InsertGlobalValues(MyGlobalElements[i], 1, &two, MyGlobalElements+i);
  }
  
  // Finish up, trasforming the matrix entries into local numbering,
  // to optimize data transfert during matrix-vector products
  A.FillComplete();

  // build up two distributed vectors q and z, and compute
  // q = A * z
  Epetra_Vector q(A.RowMap());
  Epetra_Vector z(A.RowMap());

  // Fill z with 1's
  z.PutScalar(1.0);

  A.Multiply(false, z, q); // Compute q = A*z

  double dotProduct;
  z.Dot(q, &dotProduct);

  if (Comm.MyPID() == 0) 
    std::cout << "q dot z = " << dotProduct << std::endl;

#ifdef HAVE_MPI
  MPI_Finalize();
#endif

  delete NumNz;
  
  return( EXIT_SUCCESS );
} /* main */

