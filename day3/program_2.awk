{
  if ($1 == "do()") {
    ignore = 0
  } else if ($1 == "don't()") {
    ignore = 1
  } else {
    if (ignore == 0) {
      s += $1 * $2
    }
  }
}

END {
  print "Sum:", s, " (rows: ", FNR, ")"
}
