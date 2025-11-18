type eval = Num of float | Add | Sub | Mul | Div;;

let rec eval instructions = 
  let stack = Stack.create() in
  let rec eval_inner instrs =
    match instrs with
    | [] -> (match Stack.length stack with 
              | 0 -> 0.
              | 1 -> Stack.pop stack
              | _ -> failwith "Zbyt wiele wartości")
    | head :: tail ->
        match head with
        | Num n -> 
            Stack.push n stack;
            eval_inner tail
        | Add -> 
            if Stack.length stack < 2 then
              failwith "Zbyt mało wartości przy dodawaniu";
            let b = Stack.pop stack in
            let a = Stack.pop stack in
            Stack.push (a +. b) stack;
            eval_inner tail
        | Sub -> 
            if Stack.length stack < 2 then
              failwith "Zbyt mało wartości przy odejmowaniu";
            let b = Stack.pop stack in
            let a = Stack.pop stack in
            Stack.push (a -. b) stack;
            eval_inner tail
        | Mul -> 
            if Stack.length stack < 2 then
              failwith "Zbyt mało wartości przy mnożeniu";
            let b = Stack.pop stack in
            let a = Stack.pop stack in
            Stack.push (a *. b) stack;
            eval_inner tail
        | Div -> 
            if Stack.length stack < 2 then
              failwith "Zbyt mało wartości przy dzieleniu";
            let b = Stack.pop stack in
            let a = Stack.pop stack in
            Stack.push (a /. b) stack;
            eval_inner tail
        in
        eval_inner instructions
;;


eval [Num 5.; Num 3.; Add; Num 2.; Add];;
eval [Num 5.; Num 3.; Add; Add];;
eval [Num 6.; Num 2.; Mul; Num 8.; Add];;
eval [];;
eval [Mul; Num 5.; Div];;
eval [Num 0.; Num 7.; Sub; Num 10.; Mul];;
eval [Num 1.; Num 2.; Num 3.];;
eval [Num 1.; Num 0.; Div];;
