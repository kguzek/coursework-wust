let rec suma (xs) = 
  if xs = [] then 0.0 
  else List.hd xs +. suma (List.tl xs);;

suma [5.; 3.; 2.];;
suma [0.; 0.; 0.; 0.];;
suma [-1.; 10.; 3.4; 2.1];;
suma [];;
