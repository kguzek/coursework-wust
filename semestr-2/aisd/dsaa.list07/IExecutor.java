package dsaa.list07;

public interface IExecutor<T,R> {
    void execute(T elem);
    R getResult();
}
