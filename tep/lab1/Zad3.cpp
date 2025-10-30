// Niepotrzebny jest parametr `cols`
// Można użyć o jeden wskaźnik mniej, bo kopia wskaźnika
// dalej będzie wskazywała w ten sam adres w pamięci
bool dealloc_2d_array(int** array, int cols, int rows)
{
    if (rows < 0)
    {
        return false;
    }
    for (int i = 0; i < rows; i++)
    {
        delete[] array[i];
    }
    delete[] array;
    return true;
}
