package dsaa.list07;

class IntegerToStringExec implements IExecutor<Integer, String> {
    StringBuffer line = new StringBuffer();

    public static void main(String[] args) throws DuplicateElementException {
        BinarySearchTree<Integer> tree = new BinarySearchTree<>(Integer::compareTo);
        tree.insert(7);
        tree.insert(5);
        tree.insert(2);
        tree.insert(10);
        tree.insert(12);
        IntegerToStringExec exec = new IntegerToStringExec();
        tree.inOrderWalk(exec);
        System.out.println(exec.getResult());
    }

    @Override
    public void execute(Integer elem) {
        line.append(elem).append("; ");
    }

    @Override
    public String getResult() {
        line.delete(line.length() - 2, line.length());
        return line.toString();
    }
}
