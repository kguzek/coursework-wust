def l_wybierz(list: LazyList[Int], step: Int, start: Int): LazyList[Int] = {
  def aux(list_inner: LazyList[Int], counter: Int): LazyList[Int] = {
    if (list_inner.isEmpty) {
      list_inner
    } else {
      counter match {
        case 0 => list_inner.head #:: aux(list_inner.tail, step - 1)
        case _ => aux(list_inner.tail, counter - 1)
      }
    }
  }
  aux(list, start - 1)
}

l_wybierz(LazyList(1, 2, 3, 4, 5, 6, 7), 2, 0).force
l_wybierz(LazyList(1, 2, 3, 4, 5, 6, 7), 1, 0).force
l_wybierz(LazyList(1, 2, 3, 4, 5, 6, 7), 2, 1).force
l_wybierz(LazyList(1, 2, 3, 4, 5, 6, 7), 3, 1).force
l_wybierz(LazyList(), 1, 0).force
l_wybierz(LazyList(5, 6, 3, 2, 1), 2, 1).force
