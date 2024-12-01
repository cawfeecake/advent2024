function abs(x) {
  return ((x < 0.0) ? -x : x) 
}

{
  s += abs($1 - $2)
}

END {
  print "Sum:", s, " (rows: ", FNR, ")"
}
