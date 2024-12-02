# assumes that NF >= 2

{
  # assume row is safe, then looks to see if condition fails...
  safe++

  direction_known = 0
  is_increasing = 0

  prev = $1
  for (i = 2; i <= NF; i++) {
    # Determine direction of row...
    if (direction_known == 0) {
      if (prev < $i) {
        is_increasing = 1
      } else if (prev > $i) {
        is_increasing = 0
      } else {
        safe--
        break
      }
      direction_known = 1
    }

    # Check conditional...
    if (is_increasing == 1 && (prev >= $i || $i > prev + 3)) {
      safe--
      break
    } else if (is_increasing == 0 && (prev <= $i || $i < prev - 3)) {
      safe--
      break
    }

    prev = $i
  }
}

END {
  print "Safe records:", safe
}
