#include <iostream>

#include "AltLinkList.h"


int main()
{
    AltLinkList<int, double> list(1);
    std::cout << list.is_single_elem() << std::endl; // true
    std::cout << list.get_head() << std::endl; // 1
    std::cout << (2.0 + list).is_single_elem() << std::endl; // false
    std::cout << (2.0 + list).get_head() << std::endl; // 2.0
    std::cout << (2.0 + list).get_tail().get_head() << std::endl; // 1
    // true, pod warunkiem przeciążenia operatora == dla równości strukturalnej
    // std::cout << (2.0 + list).get_tail() == list;
    std::cout << (3 + (2.0 + list)).get_head() << std::endl; // 3
    // std::cout << (2 + list); // błąd kompilacji (powinien być dodany double zamiast int)
    list = (3 + (2.0 + list));
    list = (4.0 + (3 + (2.0 + list))).get_tail();
}
