#ifndef COURSEWORK_WUST_REF_COUNTER_H
#define COURSEWORK_WUST_REF_COUNTER_H


class RefCounter
{
public:
    RefCounter() { _count = 0; }
    int increment() { return ++_count; }
    int decrement() { return --_count; };
    int get() const { return _count; }

private:
    int _count;
};


#endif //COURSEWORK_WUST_REF_COUNTER_H
