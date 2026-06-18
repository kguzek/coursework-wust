import scala.annotation.tailrec

@tailrec
def polacz_ogon(first: List[Any], second: List[Any]): List[Any] =
  second match {
    case List() => first
    case head::tail => polacz_ogon(first:+head, tail)
  }

def polacz_nie_ogon(first: List[Any], second: List[Any]): List[Any] = {
  if second.nonEmpty then
    polacz_ogon(first :+ second.head, second.tail)
  else
    first
}

polacz_ogon(List(5,4,3,2), List(1,0))
polacz_ogon(List(), List())
polacz_ogon(List(1,2,3), List())
polacz_ogon(List(), List(4,5,6))
polacz_ogon(List(1,2,3,4,5), List(1,2,3,4,5))

polacz_nie_ogon(List(5,4,3,2), List(1,0))
polacz_nie_ogon(List(), List())
polacz_nie_ogon(List(1,2,3), List())
polacz_nie_ogon(List(), List(4,5,6))
polacz_nie_ogon(List(1,2,3,4,5), List(1,2,3,4,5))
