def dlugosc(list: List[Any]): Int =
  list match  {
    case List() => 0
    case head::tail => 1 + dlugosc(tail)
}

dlugosc(List(5,4,3,2))
dlugosc(List())
dlugosc(List(1,2,3,4,5,6,7,8,9,10))
dlugosc(List(-1,-2,-3))
dlugosc(List('a', 'b', 'c', 'd', 'e', 'f', 'g'))
dlugosc(List('a', 'b', 'c', 1, 2, 3))