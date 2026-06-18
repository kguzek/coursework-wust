#ifndef COURSEWORK_WUST_ALT_LINK_LIST_H
#define COURSEWORK_WUST_ALT_LINK_LIST_H
#include <stddef.h>

#include "AltLinkListNode.h"

template <typename T1, typename T2>
class AltLinkList
{
public:
    AltLinkList();
    explicit AltLinkList(T1 head);
    explicit AltLinkList(AltLinkListNode<T1, T2>* head);
    AltLinkList(const AltLinkList& other);
    AltLinkList& operator=(const AltLinkList& other);
    ~AltLinkList();
    bool is_single_elem();
    T1 get_head() { return _head->get_value(); }
    AltLinkListNode<T1, T2>* get_head_node() const { return _head; }
    AltLinkList<T2, T1> get_tail();
    void set_tail(AltLinkListNode<T2, T1>* tail);

private:
    AltLinkListNode<T1, T2>* _head;
};

template <typename T1, typename T2>
AltLinkList<T1, T2>::AltLinkList()
{
    _head = NULL;
}

template <typename T1, typename T2>
AltLinkList<T1, T2>::AltLinkList(AltLinkListNode<T1, T2>* head) : _head(head)
{
}

template <typename T1, typename T2>
AltLinkList<T1, T2>::AltLinkList(T1 head)
{
    _head = new AltLinkListNode<T1, T2>(head);
}

template <typename T1, typename T2>
AltLinkList<T1, T2>::AltLinkList(const AltLinkList& other)
{
    _head = new AltLinkListNode<T1, T2>(*other._head);
}

template <typename T1, typename T2>
AltLinkList<T1, T2>& AltLinkList<T1, T2>::operator=(const AltLinkList& other)
{
    if (this != &other)
    {
        if (_head != NULL)
        {
            delete _head;
        }
        if (other._head != NULL)
        {
            _head = new AltLinkListNode<T1, T2>(*other._head);
        }
        else
        {
            _head = NULL;
        }
    }
    return *this;
}

template <typename T1, typename T2>
AltLinkList<T1, T2>::~AltLinkList()
{
    if (_head != NULL)
    {
        delete _head;
    }
}

template <typename T1, typename T2>
bool AltLinkList<T1, T2>::is_single_elem()
{
    return _head != NULL && !_head->has_next();
}

template <typename T1, typename T2>
AltLinkList<T2, T1> AltLinkList<T1, T2>::get_tail()
{
    AltLinkListNode<T2, T1>* next = _head->get_next();
    if (next == NULL)
    {
        return AltLinkList<T2, T1>();
    }
    AltLinkListNode<T2, T1>* next_copy = new AltLinkListNode<T2, T1>(*next);
    AltLinkList<T2, T1> list(next_copy);
    return list;
}

template <typename T1, typename T2>
void AltLinkList<T1, T2>::set_tail(AltLinkListNode<T2, T1>* tail)
{
    _head->set_next(tail);
}

template <typename T1, typename T2>
AltLinkList<T2, T1> operator+(T2 lhs, const AltLinkList<T1, T2>& rhs);

template <typename T1, typename T2>
AltLinkList<T2, T1> operator+(T2 lhs, const AltLinkList<T1, T2>& rhs)
{
    AltLinkList<T2, T1> list(lhs);
    const AltLinkListNode<T1, T2> head = *rhs.get_head_node();
    AltLinkListNode<T1, T2>* head_copy = new AltLinkListNode<T1, T2>(head);
    list.set_tail(head_copy);
    return list;
}

#endif //COURSEWORK_WUST_ALT_LINK_LIST_H
