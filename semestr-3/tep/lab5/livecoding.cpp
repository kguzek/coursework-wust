#include <map>
#include <vector>

#include "Product.h"
#include "SmartPointer.h"
#include "SingleSmartPointer.h"

std::vector<SingleSmartPointer<Product>> convert_pointers(std::vector<SmartPointer<Product>>& vector)
{
    auto new_vector = std::vector<SingleSmartPointer<Product>>();

    auto reference_counts = std::map<Product*, int>();

    for (auto instruction : vector)
    {
        if (
            Product* pointer = instruction.get();
            reference_counts.contains(pointer)
        )
        {
            reference_counts[pointer]++;
        }
        else
        {
            reference_counts[pointer] = 1;
        }
    }

    while (!vector.empty())
    {
        auto smart_pointer = vector.back();
        if (
            Product* pointer = smart_pointer.get();
            smart_pointer.count() == reference_counts[pointer] &&
            !SingleSmartPointer<Product>::is_invalid(pointer)
        )
        {
            SingleSmartPointer single_smart_pointer(pointer);
            new_vector.push_back(std::move(single_smart_pointer));
        }
        vector.pop_back();
    }

    return new_vector;
}

int main()
{
    return 0;
}
