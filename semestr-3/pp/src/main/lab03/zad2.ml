let rec polacz left right = 
  match left, right with
  | [], [] -> []
  | [], hr::tr -> hr :: (polacz [] tr)
  | hl::tl, [] -> hl :: (polacz tl [])
  | hl::tl, hr::tr -> hl :: hr :: (polacz tl tr);;

polacz [5;4;3;2] [1;2;3;4;5;6];;
polacz [] [1;2;3];;
polacz [1;2;3] [];;
polacz [] [];;
polacz [1;2;3;4] [1;2;3;4]


