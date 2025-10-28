def mniejsze(list: List[Int], value: Int): Boolean =
  if list == Nil then
    true
  else
    if list.head < value then
      mniejsze(list.tail, value)
    else
      false

mniejsze(List(1, 2, 3), 2)
