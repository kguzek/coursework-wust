import scala.annotation.tailrec

sealed trait BT[+A]
case object Empty extends BT[Nothing]
case class Node[+A](elem: A, left: BT[A], right: BT[A]) extends BT[A]

val tt = Node(1,
  Node(2,
    Node(4, Empty, Empty),
    Empty
  ),
  Node(3,
    Node(5,
      Empty,
      Node(6, Empty, Empty)
    ),
    Empty
  )
)

val tree_1_10 = Node(10,
  Node(9,
    Node(8,
      Node(7,
        Node(6,
          Node(5,
            Node(4,
              Node(3,
                Node(2,
                  Node(1,
                    Empty,
                    Empty),
                  Empty),
                Empty),
              Empty),
            Empty),
          Empty),
        Empty),
      Empty),
    Empty
  ),
  Empty
)

def tree_my(node: BT[Int]): Int = {
  @tailrec
  def tree_my_inner(nodes: List[BT[Int]], acc: Int): Int = {
    nodes match {
      case List() => acc
      case head::tail => head match {
            case Empty => tree_my_inner(tail, acc)
            case Node(value, left_child, right_child) =>
              tree_my_inner(left_child::right_child::tail, value * acc)
      }
    }
  }
  tree_my_inner(List(node), 1)
}

tree_my(tt)
tree_my(Empty)
tree_my(tree_1_10)
