to construct main ray b given point O, point A, point B do
  define ray[O, B] as rb
  define ray[O, A] as ra
  with circle[O, A] as a and 
       a ∩ rb as C and
       circle[A, O] as o and
       circle[C, O] as c and
       o ∩1 c as D do
       define ray[O, D] as b
  done
  show
done