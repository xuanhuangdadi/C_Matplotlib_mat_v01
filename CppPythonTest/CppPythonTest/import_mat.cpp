#include "iostream"
#include "import_mat.h"
#include "mat.h"
#include <string.h> 
using namespace std;
MATFile* pmatfile_w = nullptr;
mxArray* pMxArray_w = nullptr;
mxArray* pMxString_w = nullptr;
uint16 row = 0, col = 0;
const char* file = "mattest.mat"; // name the file

void mat_init(uint16 row_local, uint16 col_local)
{
	row = row_local; // set the mat.matrix row
	col = col_local; // set the mat.matrix column
	pmatfile_w = matOpen(file, "w");		// open file on write
	if (!pmatfile_w)		// open file error
		printf("open pmatfile_w error!\n");
}


// import double array data and string data
void import_data_array(double* data, char* str, uint16 num)
{
		pMxArray_w = mxCreateDoubleMatrix(row, col, mxREAL);		// the first is row£¬the first is column£¬mxREAL expands the array of real numbers
		memcpy((void*)(mxGetPr(pMxArray_w)), (void*)data, sizeof(double) * num);	// copy the data to pMxArray_w
		if (!pMxArray_w)
			cout << "pMxArray_w error!\n" << endl;
		pMxString_w = mxCreateString(str);
		if (!pMxString_w)
			cout << "pMxString_w error!\n" << endl;
		int status = matPutVariableAsGlobal(pmatfile_w, "GlobalDouble", pMxArray_w);	// write matrix into files
		if (status != 0)
			cout << "pmatfile_w_matrix error!\n" << endl;
		status = matPutVariable(pmatfile_w, "LocalString", pMxString_w); // write string into files
		if (status != 0)
			cout << "pmatfile_w_string !\n" << endl;

}


// close file
void mat_exit()
{
	matClose(pmatfile_w); 
}
