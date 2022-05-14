to construct nthpoint point P_n given point P_0, point P_1 do
  define ray[P_(n-2), P_(n-1)] ∩1 circle[P_(n-1), P_(n-2)] as P_n 
done

to construct nthsegment segment s_n given segment s_0, point V, point H do
  define segment[V_(10-n), H_n] as s_n
done

to construct nthintersect point I_n given point I_0, segment s do
  define s_(n-1) ∩ s_n as I_n
done

to construct main given point O, point V, point H do

  with nthpoint(O, V) as Vi and nthpoint(O, H) as Hi and 
       nthsegment(segment[O, Vi_10], Vi, Hi) as ti and
       nthintersect(O, ti) as Ii do

      define ti as tt upto 10
      define Ii as ii upto 10

  done
  show
done