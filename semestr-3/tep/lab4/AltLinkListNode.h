#ifndef COURSEWORK_WUST_ALT_LINK_LIST_NODE_H
#define COURSEWORK_WUST_ALT_LINK_LIST_NODE_H

template <typename T1, typename T2>
class AltLinkListNode
{
public:
    explicit AltLinkListNode(T1 value);
    AltLinkListNode(const AltLinkListNode& other);
    ~AltLinkListNode();
    T1 get_value() { return _value; }
    bool has_next() { return _next != NULL; }
    AltLinkListNode<T2, T1>* get_next() { return _next; }
    void set_next(AltLinkListNode<T2, T1>* next) { _next = next; }

private:
    T1 _value;
    AltLinkListNode<T2, T1>* _next;
};

template <typename T1, typename T2>
AltLinkListNode<T1, T2>::AltLinkListNode(T1 value) : _value(value), _next(NULL)
{
}

template <typename T1, typename T2>
AltLinkListNode<T1, T2>::AltLinkListNode(const AltLinkListNode& other) :
    _value(other._value),
    _next(NULL)
{
    if (other._next != NULL)
    {
        _next = new AltLinkListNode<T2, T1>(*other._next);
    }
}

template <typename T1, typename T2>
AltLinkListNode<T1, T2>::~AltLinkListNode()
{
    if (_next != NULL)
    {
        delete _next;
    }
}
#endif //COURSEWORK_WUST_ALT_LINK_LIST_NODE_H
