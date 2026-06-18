import java.util.Arrays;

public class zad1 {
    public static int[] insert(int[] array, int item) {
        int length = array.length;
        int[] result = new int[length + 1];

        int insertAt;
        for (insertAt = 0; insertAt < length && array[insertAt] < item; insertAt++) {
            result[insertAt] = array[insertAt];
        }

        result[insertAt] = item;

        if (length >= insertAt) {
            System.arraycopy(array, insertAt, result, insertAt + 1, length - insertAt);
        }

        return result;
    }
    
    private static void insertAndPrint(int[] array, int item) {
        int[] newArray =  insert(array, item);
        System.out.println(Arrays.toString(newArray));
    }

    public static void main(String[] args) {
        insertAndPrint(new int[]{1, 2, 3, 4, 5}, 3);
        insertAndPrint(new int[]{1, 2, 3, 4, 5}, 4);
        insertAndPrint(new int[]{1, 2, 3, 4, 5}, 5);
        insertAndPrint(new int[]{1, 2, 3, 4, 5}, 6);
        insertAndPrint(new int[]{}, 0);
        insertAndPrint(new int[]{}, 10);
    }
}
