# assumes that NF >= 2

function check_row(skip_i) {
  direction_known = 0
  is_increasing = 0

  prev = $1
  start_i = 2
  if (skip_i == 0) {
    prev = $2
    start_i++
  }

  for (i = start_i; i <= NF; i++) {
    if (skip_i != i) {
      # Determine direction of row...
      if (direction_known == 0) {
        if (prev < $i) {
          is_increasing = 1
        } else if (prev > $i) {
          is_increasing = 0
        } else {
          return 0
        }
        direction_known = 1
      }

      # Check conditional...
      if (is_increasing == 1 && (prev >= $i || $i > prev + 3)) {
        return 0
      } else if (is_increasing == 0 && (prev <= $i || $i < prev - 3)) {
        return 0
      }

      prev = $i
    }
  }

  return 1
}

{
  for (outer_i = -1; outer_i <= NF; outer_i++) {
    is_safe = check_row(outer_i)
    if (is_safe > 0) {
      safe++
      print NR, "is safe! (while skipping", outer_i, ")"
      break
    }
    print "Unsafe!", NR, "(while skipping", outer_i, "); checking again..."
  }
}

END {
  print "Safe records:", safe
}
