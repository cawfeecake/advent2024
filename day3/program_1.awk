{
  s += $1 * $2
}

END {
  print "Sum:", s, " (rows: ", FNR, ")"
}
