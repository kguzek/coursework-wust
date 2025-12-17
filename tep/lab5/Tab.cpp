#include "Tab.h"

Tab create_tab()
{
    Tab result;
    result.set_size(5);
    // return result;
    return std::move(result);
}

int main()
{
    const Tab tab = create_tab();
}
