NR==FNR { 
  right_seen[$2]++
  next
}

{
  if ($1 in right_seen) {
    s += $1 * right_seen[$1]
    found++
  }
}

END {
  print "Sum:", s, " (found: ", found, ")"
}
